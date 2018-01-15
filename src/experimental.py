from util import util

try:
    import networkx as nx
except ImportError:
    util.install_missing_dependencies("networkx")
    import networkx as nx

import levenshtein

from util.doublemetaphone import dm as doublemetaphone


def score_words_dm(words):
    if len(words) <= 1:
        return 0
    score = []
    for word1 in words:
        for word2 in words:
            if word1 != word2:
                score.append(doublemetaphone(word1) == doublemetaphone(word2))
    combinations = len(words) * (len(words) - 1)
    return sum(score) / combinations


def bad_word_detection(complete_alignment, bad_words, upper_filter=0.6):
    for group in list(map((lambda group: list(group)), nx.connected_components(complete_alignment))):
        if levenshtein.score_words(group) < upper_filter and score_words_dm(group) < upper_filter:
            bad_words.append(levenshtein.worst_word(group))
