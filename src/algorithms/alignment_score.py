from util import util
try:
    import networkx as nx
except ImportError:
    util.install_missing_dependencies("networkx")
    import networkx as nx

def calculate_alignment_score(gs_graph, alignment_graph, should_print=False):
    goldstandardList = list(
        map((lambda group: list(group)), nx.connected_components(gs_graph)))
    createdAlignmentList = list(
        map((lambda group: list(group)), nx.connected_components(alignment_graph)))

    goldstandardWordCount = 0
    words_in_gs_not_in_alignment_counter = 0
    numberOfAlignedGroupes = len(createdAlignmentList)
    numberOfGSGroupes = len(goldstandardList)
    alignedWordCount = 0

    for alignments in createdAlignmentList:
        alignedWordCount += len(alignments)

    words_in_alignment_not_in_gs_counter_dict = {}
    for alignments in goldstandardList:
        goldstandardWordCount += len(alignments)
        words_in_alignment_not_in_gs_counter_dict[str(alignments)] = []
        for word in alignments:
            if alignment_graph.has_node(word):
                found = nx.node_connected_component(alignment_graph, word)
                words_in_alignment_not_in_gs_counter_dict[str(alignments)].append(
                    sum(word not in alignments for word in found))
            else:
                # print("missing: " + word)
                words_in_gs_not_in_alignment_counter += 1

    words_in_alignment_not_in_gs_counter = sum(
        arr[0] for arr in words_in_alignment_not_in_gs_counter_dict.values() if len(arr) > 0)

    if should_print:
        print("Goldstandard Word Count: " + str(goldstandardWordCount))
        print("Alignment Word Count: " + str(alignedWordCount))
        print("Difference Word Count: " + str(abs(goldstandardWordCount - alignedWordCount)))
        print("Words from Goldstandard not found in Alignment: " + str(words_in_gs_not_in_alignment_counter))
        print("Words from Alignment not found in Goldstandard: " + str(words_in_alignment_not_in_gs_counter))
        print("Goldstandard Group Count: " + str(numberOfGSGroupes))
        print("Alignment Group Count: " + str(numberOfAlignedGroupes))
        print("Difference Group Count: " + str(abs(numberOfGSGroupes - numberOfAlignedGroupes)))