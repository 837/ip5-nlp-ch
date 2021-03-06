import subprocess
from functools import reduce

from util.util import convert_to_lower, remove_punctuation, normalized_dl_distance, install_missing_dependencies

try:
    import networkx as nx
except ImportError:
    install_missing_dependencies("networkx")
    import networkx as nx

from algorithms import experimental, bleu_score, levenshtein
from util.doublemetaphone import dm as doublemetaphone

ALIGNER_BLEUALIGN = "bleualign/bleu-champ.exe -s tmp/swg1.txt -t tmp/swg2.txt -q"
ALIGNER_HUNALIGN = "Hunalign/hunalign.exe -text -realign -utf Hunalign/null.dict tmp/swg1.txt tmp/swg2.txt"


# Splits texts to characters, removes punctuation and makes everything lower case
def prepare(texts, alignment_remove_punctuation, alignment_all_lower_case):
    sentences = []
    for sentence in texts:
        sentences.append(reduce((lambda x, y: x + " " + y), list(
            sentence)).replace("   ", " ~~~\n"))

    if alignment_remove_punctuation:
        sentences = remove_punctuation(sentences)

    if alignment_all_lower_case:
        sentences = convert_to_lower(sentences)

    return list(sentences)


def align(sentences, graph, aligner, alignment_filter_value):
    for sentence2 in sentences:
        f2 = open('tmp/swg2.txt', 'wb')
        f2.write(sentence2.encode("utf8"))
        f2.flush()

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        create_aligned_word_dict(
            subprocess.Popen(aligner,
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, startupinfo=startupinfo).communicate()[
                0].decode("utf8").split(
                "\n"), graph, alignment_filter_value)

    return graph


def create_aligned_word_dict(aligned_sentence, graph, alignment_filter_value):
    for sentence in aligned_sentence:
        words = sentence.replace("\r", "").split("\t")
        if len(words) >= 2:
            key = words[0].replace(" ", "").replace("~~~", " ").replace("  ", " ").strip()
            value = words[1].replace(" ", "").replace("~~~", " ").replace("  ", " ").strip()
            lv = normalized_dl_distance(key, value) > alignment_filter_value
            meta = doublemetaphone(key) == doublemetaphone(value)
            if "" is key or "" is value:
                continue
            if lv and not meta:
                continue
            if not graph.has_node(key):
                graph.add_node(key)
            if not graph.has_node(value):
                graph.add_node(value)
            weight = round(normalized_dl_distance(key, value), 2)

            graph.add_edge(key, value, weight=weight)

    return graph


def align_one_sentence_to_the_others(texts, graph, aligner,
                                     alignment_filter_value=0.25,
                                     alignment_remove_punctuation=True, alignment_all_lower_case=True,
                                     id_of_sentence_to_be_aligned_to=-1):
    if id_of_sentence_to_be_aligned_to == -1:
        id_of_sentence_to_be_aligned_to = bleu_score.max_index(bleu_score.bleu_ratings(texts))

    sentences = prepare(texts, alignment_remove_punctuation, alignment_all_lower_case)
    with open('tmp/swg1.txt', 'wb') as f1:
        f1.write(sentences[id_of_sentence_to_be_aligned_to].encode("utf8"))

    return align(sentences, graph, aligner, alignment_filter_value)


def align_every_sentence_to_the_others(texts, graph, aligner, alignment_filter_value=0.25,
                                       alignment_remove_punctuation=True,
                                       alignment_all_lower_case=True):
    sentences = prepare(texts, alignment_remove_punctuation, alignment_all_lower_case)

    for sentence1 in sentences:
        with open('tmp/swg1.txt', 'wb') as f1:
            f1.write(sentence1.encode("utf8"))

        align(sentences, graph, aligner, alignment_filter_value)

    return graph


def improve(texts, base_sentence_id, aligner, experimental_improve=True):
    graph = nx.Graph()
    align_one_sentence_to_the_others(texts, graph, aligner, alignment_filter_value=1,
                                     alignment_remove_punctuation=False,
                                     id_of_sentence_to_be_aligned_to=base_sentence_id)

    words = texts[base_sentence_id].split(" ")
    bad_words = ["**", "***", "****", "??", "???"]

    if experimental_improve:
        experimental.bad_word_detection(graph, bad_words)
    print(bad_words)
    for i, word in enumerate(words):
        if word in bad_words:
            for group in list(map((lambda group: list(group)), nx.connected_components(graph))):
                if word in group:
                    words[i] = levenshtein.best_word(group)
                    break
    return reduce((lambda x, y: x + " " + y), words)
