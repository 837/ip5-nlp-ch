from util import util
try:
    import networkx as nx
except ImportError:
    util.install_missing_dependencies("networkx")
    import networkx as nx


import levenshtein


def bad_word_detection(complete_alignment, bad_words, experimental_filter_lower=0.8, experimental_filter_upper=0.9):
    for group in list(map((lambda group: list(group)), nx.connected_components(complete_alignment))):
        if experimental_filter_lower < levenshtein.score_alignment(group) < experimental_filter_upper:
            # print(levenshtein.score_alignment(group), group)
            bad_words.append(levenshtein.worst_word(group))
