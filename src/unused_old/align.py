import subprocess
from functools import reduce

import bleu_score
import experimental
import levenshtein
from util import options, util, doublemetaphone

ALIGNER_BLEUALIGN = "bleualign/bleu-champ.exe -s swg1.txt -t swg2.txt -q"
ALIGNER_HUNALIGN = "Hunalign/hunalign.exe -text -realign -utf Hunalign/null.dict swg1.txt swg2.txt"


# Splits texts to characters, removes punctuation and makes everything lower case
def prepare(texts, alignment_remove_punctuation, alignment_all_lower_case):
    sentences = []
    for sentence in texts:
        sentences.append(reduce((lambda x, y: x + " " + y), list(
            sentence)).replace("   ", "\n"))

    if alignment_remove_punctuation:
        sentences = util.remove_punctuation(sentences)

    if alignment_all_lower_case:
        sentences = util.convert_to_lower(sentences)

    return list(sentences)


def align(sentences, dict_to_use, aligner, alignment_filter_value):
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
                "\n"), dict_to_use, alignment_filter_value)

    return dict_to_use


def create_aligned_word_dict(aligned_sentence, dict_to_use, alignment_filter_value):
    for sentence in aligned_sentence:
        words = sentence.replace("\r", "").split("\t")
        if len(words) >= 2:
            key = words[0].replace(" ", "").replace("~~~", " ")
            value = words[1].replace(" ", "").replace("~~~", " ")
            if util.normalized_dl_distance(key, value) > alignment_filter_value:
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


# def merge(dict_to_use):
#     newarr=[]
#     for wordgroup in dict_to_use:
#         for item in wordgroup:
#             if item in newarr:


def align_one_sentence_to_the_others(texts, dict_to_use, aligner,
                                     alignment_filter_value=0.5,
                                     alignment_remove_punctuation=True, alignment_all_lower_case=True,
                                     id_of_sentence_to_be_aligned_to=-1):
    if id_of_sentence_to_be_aligned_to == -1:
        id_of_sentence_to_be_aligned_to = bleu_score.max_index(bleu_score.bleu_ratings(texts))

    sentences = prepare(texts, alignment_remove_punctuation, alignment_all_lower_case)
    with open('swg1.txt', 'wb') as f1:
        f1.write(sentences[id_of_sentence_to_be_aligned_to].encode("utf8"))

    return align(sentences, dict_to_use, aligner, alignment_filter_value)


def align_every_sentence_to_the_others(texts, dict_to_use, aligner, alignment_filter_value=0.5,
                                       alignment_remove_punctuation=True,
                                       alignment_all_lower_case=True):
    sentences = prepare(texts, alignment_remove_punctuation, alignment_all_lower_case)

    for sentence1 in sentences:
        with open('swg1.txt', 'wb') as f1:
            f1.write(sentence1.encode("utf8"))

        align(sentences, dict_to_use, aligner, alignment_filter_value)

    return dict_to_use


def improve(texts, base_sentence_id, aligner):
    complete_alignment = []
    align_one_sentence_to_the_others(texts, complete_alignment, aligner, alignment_filter_value=1,
                                     alignment_remove_punctuation=False,
                                     id_of_sentence_to_be_aligned_to=base_sentence_id)

    words = texts[base_sentence_id].split(" ")
    bad_words = ["**", "***", "****", "??", "???"]

    if options.EXPERIMENTAL_ACTIVATE_EXPERIMENTAL:
        if options.EXPERIMENTAL_USE_BAD_WORD_DETECTION:
            experimental.bad_word_detection(complete_alignment, bad_words)

    for i, word in enumerate(words):
        if word in bad_words:
            for group in complete_alignment:
                if word in group:
                    words[i] = levenshtein.best_word(group)
                    break
    return reduce((lambda x, y: x + " " + y), words)
