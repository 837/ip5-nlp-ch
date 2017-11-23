import string
import subprocess
from functools import reduce
import util


def remove_punctuation(texts):
    sentences = []
    for sentence in texts:
        sentences.append(reduce((lambda x, y: x + " " + y), list(
            sentence.replace(",", '').replace(".", '').replace(":", '').replace("!", ''))).replace("   ", "\n"))
    return sentences


BLEUALIGN = "bleualign/bleu-champ.exe -s swg1.txt -t swg2.txt -q"
HUNALIGN = "Hunalign/hunalign.exe -text -realign -utf Hunalign/null.dict swg1.txt swg2.txt"


def align(sentences, dict_to_use, aligner):
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
                "\n"), dict_to_use)

    return dict_to_use


from pyxdameraulevenshtein import damerau_levenshtein_distance, normalized_damerau_levenshtein_distance


def create_aligned_word_dict(aligned_sentence, dict_to_use):
    for sentence in aligned_sentence:
        words = sentence.replace("\r", "").split("\t")
        if len(words) >= 2:
            key = words[0].replace(" ", "").replace("~~~", " ")
            value = words[1].replace(" ", "").replace("~~~", " ")
            if normalized_damerau_levenshtein_distance(key, value) > 0.8:
                continue

            found = False
            for wordgroup in dict_to_use:
                if key in wordgroup or value in wordgroup:
                    if key not in wordgroup:
                        wordgroup.append(key)
                    if value not in wordgroup:
                        wordgroup.append(value)
                    found = True
            if not found:
                if (key != value):
                    dict_to_use.append([key, value])
                else:
                    dict_to_use.append([key])
    return dict_to_use


def align_one_sentence_to_the_others(texts, id_of_sentence_to_be_aligned_to, dict_to_use, aligner):
    sentences = remove_punctuation(texts)

    with open('swg1.txt', 'wb') as f1:
        f1.write(sentences[id_of_sentence_to_be_aligned_to].encode("utf8"))

    return align(sentences, dict_to_use, aligner)


def align_every_sentence_to_the_others(texts, dict_to_use, aligner):
    sentences = remove_punctuation(texts)

    for sentence1 in sentences:
        with open('swg1.txt', 'wb') as f1:
            f1.write(sentence1.encode("utf8"))

        align(sentences, dict_to_use, aligner)

    return dict_to_use
