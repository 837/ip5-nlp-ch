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
    temp_sentence_dict = dict()
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
                "\n"), temp_sentence_dict)

    print(temp_sentence_dict)
    for key in temp_sentence_dict:
        if "***" == key:
            if "***" != temp_sentence_dict[key][0] and not "" == temp_sentence_dict[key][0]:
                newKey = temp_sentence_dict[key][0]
                if newKey in temp_sentence_dict:
                    temp_sentence_dict[newKey].extend(temp_sentence_dict.pop(key))
                else:
                    temp_sentence_dict[newKey] = temp_sentence_dict.pop(key)
            elif len(temp_sentence_dict[key]) >= 2:
                if "***" != temp_sentence_dict[key][1] and not "" == temp_sentence_dict[key][1]:
                    newKey = temp_sentence_dict[key][1]
                    if newKey in temp_sentence_dict:
                        temp_sentence_dict[newKey].extend(temp_sentence_dict.pop(key))
                    else:
                        temp_sentence_dict[newKey] = temp_sentence_dict.pop(key)
    print(temp_sentence_dict)

    return dict_to_use


def create_aligned_word_dict(aligned_sentence, dict_to_use):
    for sentence in aligned_sentence:
        words = sentence.replace("\r", "").split("\t")
        if len(words) >= 2:
            key = words[0].replace(" ", "").replace("~~~", " ")
            value = words[1].replace(" ", "").replace("~~~", " ")
            if key in dict_to_use:
                if not value in dict_to_use[key]:
                    dict_to_use[key].append(value)
            else:
                dict_to_use[key] = [value]
    return dict_to_use


def align_one_sentence_to_the_others(texts, id_of_sentence_to_be_aligned_to, dict_to_use, aligner):
    sentences = remove_punctuation(texts)

    f1 = open('swg1.txt', 'wb')
    f1.write(sentences[id_of_sentence_to_be_aligned_to].encode("utf8"))
    f1.flush()

    util.dump_dict_to_json(align(sentences, dict_to_use, aligner),
                           "align_one_sentence_to_the_others.json")


def align_every_sentence_to_the_others(texts, dict_to_use, aligner):
    sentences = remove_punctuation(texts)

    for sentence1 in sentences:
        f1 = open('swg1.txt', 'wb')
        f1.write(sentence1.encode("utf8"))
        f1.flush()

        util.dump_dict_to_json(align(sentences, dict_to_use, aligner),
                               "align_every_sentence_to_the_others.json")
