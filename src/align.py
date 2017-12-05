import string
import subprocess
from functools import reduce
import util
import levenshtein


def remove_punctuation(texts):
    return map((lambda t: t.replace(",", '').replace(".", '').replace(":", '').replace("!", '')), texts)


def prepare(texts):
    sentences = []
    for sentence in texts:
        sentences.append(reduce((lambda x, y: x + " " + y), list(
            sentence)).replace("   ", "\n"))
    return sentences


BLEUALIGN = "bleualign/bleu-champ.exe -s swg1.txt -t swg2.txt -q"
HUNALIGN = "Hunalign/hunalign.exe -text -realign -utf Hunalign/null.dict swg1.txt swg2.txt"


def align(sentences, dict_to_use, aligner, filter_value):
    for sentence2 in sentences:
        f2 = open('swg2.txt', 'wb')
        f2.write(sentence2.encode("utf8"))
        f2.flush()

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        create_aligned_word_dict(
            subprocess.Popen(aligner,
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, startupinfo=startupinfo).communicate()[
                0].decode("utf8").split(
                "\n"), dict_to_use, filter_value)

    return dict_to_use


def create_aligned_word_dict(aligned_sentence, dict_to_use, filter_value=0.333):
    for sentence in aligned_sentence:
        words = sentence.replace("\r", "").split("\t")
        if len(words) >= 2:
            key = words[0].replace(" ", "").replace("~~~", " ")
            value = words[1].replace(" ", "").replace("~~~", " ")
            if util.normalized_dl_distance(key, value) > filter_value:  # should be between 0.333 and 0.55
                continue

            found = False
            for wordgroup in dict_to_use:
                if key in wordgroup or value in wordgroup:
                    if key not in wordgroup:
                        wordgroup.append(key)
                    if value not in wordgroup:
                        wordgroup.append(value)
                    found = True
                    break
            if not found:
                if key != value:
                    dict_to_use.append([key, value])
                else:
                    dict_to_use.append([key])
    return dict_to_use


def align_one_sentence_to_the_others(texts, id_of_sentence_to_be_aligned_to, dict_to_use, aligner, filter_value=0.333,
                                     ignore_punctuation=False):
    sentences = prepare(texts)
    if ignore_punctuation:
        sentences = remove_punctuation(sentences)

    with open('swg1.txt', 'wb') as f1:
        f1.write(sentences[id_of_sentence_to_be_aligned_to].encode("utf8"))

    return align(sentences, dict_to_use, aligner, filter_value)


def align_every_sentence_to_the_others(texts, dict_to_use, aligner, filter_value=0.333):
    sentences = prepare(remove_punctuation(texts))

    for sentence1 in sentences:
        with open('swg1.txt', 'wb') as f1:
            f1.write(sentence1.encode("utf8"))

        align(sentences, dict_to_use, aligner, filter_value)

    return dict_to_use


def improve(texts, base_sentence_id, aligner, use_bad_word_detection=False, group_score_for_filter_lower=0.8,
            group_score_for_filter_upper=0.9):
    complete_alignment = []
    align_one_sentence_to_the_others(texts, base_sentence_id, complete_alignment, aligner, 1, False)

    words = texts[base_sentence_id].split(" ")
    bad_words = ["**", "***", "****", "??", "???"]

    if use_bad_word_detection:
        for group in complete_alignment:
            if group_score_for_filter_lower < levenshtein.score_alignment(group) < group_score_for_filter_upper:
                # print(levenshtein.score_alignment(group), group)
                bad_words.append(levenshtein.worst_word(group))

        print(bad_words)

    for i, word in enumerate(words):
        if word in bad_words:
            for group in complete_alignment:
                # if group_score_for_filter_lower < levenshtein.score_alignment(group) < group_score_for_filter_upper:
                if word in group:
                    print(group)
                    words[i] = levenshtein.best_word(group)
                    break
    return reduce((lambda x, y: x + " " + y), words)
