import align
import bleu_score
from util import options, util
try:
    import networkx as nx
except ImportError:
    util.install_missing_dependencies("networkx")
    import networkx as nx

def print_graph_with_edges(G):
    import pylab

    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True, font_weight='bold', pos=pos)
    edge_labels = dict([((u, v,), d['weight'])
                        for u, v, d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    pylab.show()


def calculate_alignment_score(gs_graph, alignment_graph, additional_Text="", should_print=False):
    goldstandardList = list(
        map((lambda group: list(group)), nx.connected_components(gs_graph)))
    createdAlignmentList = list(
        map((lambda group: list(group)), nx.connected_components(alignment_graph)))
    print("Gold List")
    print(goldstandardList)
    print("Alignment List")
    print(createdAlignmentList)

    goldstandardWordCount = 0
    words_in_gs_not_in_alignment_counter = 0
    foundWords = 0
    numberOfAlignedGroupes = len(createdAlignmentList)
    numberOfGSGroupes = len(goldstandardList)
    alignedWordCount = 0

    for alignments in createdAlignmentList:
        alignedWordCount += len(alignments)

    # additional_word_counter_dict = {}
    words_in_alignment_not_in_gs_counter_dict = {}
    for alignments in goldstandardList:
        goldstandardWordCount += len(alignments)
        words_in_alignment_not_in_gs_counter_dict[str(alignments)] = []
        for word in alignments:
            if alignment_graph.has_node(word):
                foundWords += 1
                found = nx.node_connected_component(alignment_graph, word)
                # additional_word_counter_dict[word] = sum(word not in alignments for word in found)
                # if additional_word_counter_dict[word] > 0:
                #     print(additional_word_counter_dict[word], word, alignments, found,
                #           list(word not in alignments for word in found))
                words_in_alignment_not_in_gs_counter_dict[str(alignments)].append(
                    sum(word not in alignments for word in found))
            else:
                print("missing: " + word)
                words_in_gs_not_in_alignment_counter += 1

                ##########################PLEASE REDO :D ###################################
    # print(words_in_alignment_not_in_gs_counter_dict)
    words_in_alignment_not_in_gs_counter = sum(
        arr[0] for arr in words_in_alignment_not_in_gs_counter_dict.values() if len(arr) > 0)
    word_count_score = (foundWords / goldstandardWordCount) * 100

    score_groups = (abs(numberOfGSGroupes - numberOfAlignedGroupes) / (
        numberOfGSGroupes + numberOfAlignedGroupes)) * 100
    words_not_in_gs_percentage = (words_in_alignment_not_in_gs_counter / alignedWordCount) * 100
    words_not_in_alignment_percentage = (words_in_gs_not_in_alignment_counter / goldstandardWordCount) * 100

    score_words = (word_count_score - words_not_in_gs_percentage - words_not_in_alignment_percentage)

    total_score = score_words - score_groups
    ##########################PLEASE REDO :D ###################################

    if should_print:
        print("goldstandardWordCount: " + str(goldstandardWordCount))
        print("alignedWordCount: " + str(alignedWordCount))
        print("foundWords: " + str(foundWords))
        print("missing: " + str(abs(goldstandardWordCount - alignedWordCount)))
        print("words_in_gs_not_in_alignment_counter: " + str(words_in_gs_not_in_alignment_counter))
        print("words_in_alignment_not_in_gs_counter: " + str(words_in_alignment_not_in_gs_counter))
        print("words_not_in_alignment_percentage: " + str(words_not_in_alignment_percentage))
        print("words_not_in_gs_percentage: " + str(words_not_in_gs_percentage))
        print("numberOfAlignedGroupes: " + str(numberOfAlignedGroupes))
        print("numberOfGSGroupes: " + str(numberOfGSGroupes))
        print("difference(abs(numberOfGSGroupes-numberOfAlignedGroupes)): " + str(
            abs(numberOfGSGroupes - numberOfAlignedGroupes)))

        print("word_count_score: " + str(word_count_score))
        print("score_words: " + str(score_words))
        print("score_groups: " + str(score_groups))
        print("total_score(higher is better): " + str(total_score))

    print(str(additional_Text) + " scored: " + str(total_score))
    return total_score


def rate_sentence_group(group):
    return bleu_score.bleu_ratings(group)


def load_data_from_csv(path):
    return util.loadDataFromCSVFile(path)


def get_good_transcriptions(group):
    return bleu_score.getGoodTranscriptions(group)


def align_a_sentence_to_the_others(group, aligner, filtervalue, id_of_sentence_to_be_aligned_to):
    return align.align_one_sentence_to_the_others(group, nx.Graph(), aligner, filtervalue,
                                                  id_of_sentence_to_be_aligned_to=id_of_sentence_to_be_aligned_to)


def align_every_sentence_to_the_others(group, aligner, filtervalue):
    return align.align_every_sentence_to_the_others(group, nx.Graph(), aligner, filtervalue)


def export_as_graph(graph, filename):
    util.dump_data_to_json(nx.node_link_data(graph), filename)


def export_as_list(graph, filename):
    util.dump_data_to_json(list(map((lambda group: list(group)), nx.connected_components(graph))), filename)


def import_as_graph(filename):
    return nx.json_graph.node_link_graph(util.load_json(filename))

# Load Data
allTaskByID = load_data_from_csv('../data/transcribe-2017-07-08.CSV')
group = allTaskByID[2048][0]
good_transcriptions = get_good_transcriptions(group)
aligned_graph = align_every_sentence_to_the_others(group, aligner=align.ALIGNER_BLEUALIGN, filtervalue=0.25)
export_as_list(aligned_graph, "dumpedList.json")
export_as_graph(aligned_graph, "dumpedGraph.json")
imported_graph = import_as_graph("dumpedGraph.json")
print_graph_with_edges(imported_graph)
# #
# # gs_graph = nx.json_graph.node_link_graph(
# #     util.load_json("GoldStandard/gs_graph.json"))  # LOAD GOLDSTANDARD_GRAPH FROM JSON
#
# # alignedGraph = nx.json_graph.node_link_graph(
# #     util.load_json("dumpedGraph.json"))
# gs_graph = nx.json_graph.node_link_graph(
#     util.load_json("GoldStandard/gs_graph.json"))
# params = [nx.Graph(), align.ALIGNER_BLEUALIGN, 0.25]
#
#
#
# alignedGraph = ()
# iterationCount = 1
# for taskID in options.GOLD_STANDARD_SET:
#     util.print_progress(iterationCount, len(options.GOLD_STANDARD_SET), prefix='Progress:', suffix='Complete')
#     group = allTaskByID[taskID][0]
#     alignedGraph = align.align_every_sentence_to_the_others(group, params[0], params[1], params[2])
#     iterationCount += 1
# # # util.dump_dict_to_json(nx.node_link_data(alignedGraph), "dumpedGraph.json")
# #
# score = calculate_alignment_score(gs_graph, alignedGraph, "With params[" + str(params) + "]", True)
# #
# print_graph_with_edges(alignedGraph)




# iterative_testing(20, 1, params, gs_graph)

# group = allTaskByID[2048][0]
# graph = alignGraph.align_every_sentence_to_the_others(group, params[0], params[1], params[2])
# print_graph_with_edges(graph)

# util.dump_dict_to_json(nx.node_link_data(G), "nodeLinkData.json")
# util.dump_dict_to_json(nx.adjacency_data(G), "adjacencyData.json")
# util.dump_dict_to_json(list(map((lambda group: list(map((lambda node: node), group))), nx.connected_components(G))),
#                        "connectedComponents.json")



# util.dump_dict_to_json(list(map((lambda group: list(map((lambda node: node), group))), nx.connected_components(GS))),
#                        "connectedComponentsGS.json")


# print_graph_with_edges(G)






# CREATE ALIGNMENTS AND DUMP TO JSON FILE
# iterationCount = 1
# allAlignments = []
# hun1toN = []
# bleu1toN = []
# hunNtoN = []
# bleuNtoN = []
# for taskID in options.GOLD_STANDARD_SET:
#     util.print_progress(iterationCount, len(options.GOLD_STANDARD_SET), prefix='Progress:', suffix='Complete')
#     group = allTaskByID[taskID][0]
#
#     align.align_one_sentence_to_the_others(group, hun1toN, align.ALIGNER_HUNALIGN)
#     align.align_one_sentence_to_the_others(group, bleu1toN, align.ALIGNER_BLEUALIGN)
#
#     align.align_every_sentence_to_the_others(group, hunNtoN, align.ALIGNER_HUNALIGN)
#     align.align_every_sentence_to_the_others(group, bleuNtoN, align.ALIGNER_BLEUALIGN)
#
#     iterationCount += 1
#
# util.dump_dict_to_json(hun1toN, "hun1toN.json")
# util.dump_dict_to_json(bleu1toN, "bleu1toN.json")
# util.dump_dict_to_json(hunNtoN, "hunNtoN.json")
# util.dump_dict_to_json(bleuNtoN, "bleuNtoN.json")

# alldata = []
# iterationCount = 1
# for id in options.GOLD_STANDARD_SET:
#     util.print_progress(iterationCount, len(options.GOLD_STANDARD_SET), prefix='Progress:', suffix='Complete')
#     currentData = []
#     group = allTaskByID[id][0]
#     if len(group) < 2:
#         iterationCount += 1
#         continue
#     print(group)
#     print("Group Nr.: " + str(id))
#     currentData.append("Group Nr.: " + str(id))
#
#     print("good sentence:")
#     goodTranscriptions = bleu_score.getGoodTranscriptions(group)
#     group = goodTranscriptions[0]
#     scores = goodTranscriptions[1]
#     best_index = bleu_score.max_index(scores)
#     print(group[best_index])
#     currentData.append(("good sentence:", group[best_index]))
#
#     print("\nbad sentence:")
#     improve_index = bleu_score.min_index(scores)
#     print(group[improve_index])
#     currentData.append(("bad sentence:", group[improve_index]))
#
#     print("\nimproved sentence:")
#     improved = align.improve(group, improve_index, align.ALIGNER_HUNALIGN, experimental_improve=True)
#     print(improved)
#     currentData.append(("improved sentence:", improved))
#
#     print("\nimproved sentence(with additional word filter):")
#     improved = align.improve(group, improve_index, align.ALIGNER_HUNALIGN)
#     print(improved)
#     currentData.append(("improved sentence(with additional word filter):", improved))
#     alldata.append(currentData)
#     iterationCount += 1
#     print()
#     print()
#
# util.dump_dict_to_json(alldata, "BadSentenceCorrectionTest.json")
