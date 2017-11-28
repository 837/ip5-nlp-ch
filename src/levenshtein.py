from pyxdameraulevenshtein import damerau_levenshtein_distance, normalized_damerau_levenshtein_distance

import util


def score_words(words):
    if len(words) <= 1:
        return 0
    score = 0
    for word1 in words:
        for word2 in words:
            if word1 != word2:
                score += util.normalized_dl_distance(word1, word2)
    combinations = len(words) * (len(words) - 1)
    return score / combinations


def score_alignment(alignment):
    if len(alignment) == 0:
        return 0
    score = 0
    for words in alignment:
        score += score_words(words)
    return score / len(alignment)
