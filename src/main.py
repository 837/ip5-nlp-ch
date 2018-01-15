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
    print("Creating Graph to display, might take a long time.")
    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True, font_weight='bold', pos=pos)
    edge_labels = dict([((u, v,), d['weight'])
                        for u, v, d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    pylab.show()


def rate_sentence_group(group):
    return bleu_score.bleu_ratings(group)


def load_data_from_csv(path):
    return util.loadDataFromCSVFile(path)


def get_good_transcriptions(group):
    return bleu_score.getGoodTranscriptions(group)


def align_a_sentence_to_the_others(group, aligner, filtervalue, id_of_sentence_to_be_aligned_to,
                                   graph_to_use=nx.Graph()):
    return align.align_one_sentence_to_the_others(group, graph_to_use, aligner, filtervalue,
                                                  id_of_sentence_to_be_aligned_to=id_of_sentence_to_be_aligned_to)


def align_every_sentence_to_the_others(group, aligner, filtervalue, graph_to_use=nx.Graph()):
    return align.align_every_sentence_to_the_others(group, graph_to_use, aligner, filtervalue)


def export_as_graph(graph, filename):
    util.dump_data_to_json(nx.node_link_data(graph), filename)


def export_as_list(graph, filename):
    util.dump_data_to_json(list(map((lambda group: list(group)), nx.connected_components(graph))), filename)


def import_as_graph(filename):
    return nx.json_graph.node_link_graph(util.load_json(filename))


def create_graph_over_list_of_groups(list_of_groups, aligner, filtervalue,
                                     graph_to_use=nx.Graph()):
    iterationCount = 1
    for taskID in list_of_groups:
        util.print_progress(iterationCount, len(list_of_groups), prefix='Progress:', suffix='Complete')
        group = allTaskByID[taskID][0]
        align.align_every_sentence_to_the_others(group, aligner=aligner,
                                                 alignment_filter_value=filtervalue, graph=graph_to_use)
        iterationCount += 1
    return graph_to_use


def improve_sentence(group, sentence_to_improve, aligner=align.ALIGNER_HUNALIGN, experimental_improve=False):
    return align.improve(group, group.index(sentence_to_improve), aligner, experimental_improve=experimental_improve)


# Load Data
allTaskByID = load_data_from_csv('../data/transcribe-2017-07-08.CSV')
group = allTaskByID[2048][0]
good_transcriptions = get_good_transcriptions(group)
aligned_graph = align_every_sentence_to_the_others(group, aligner=align.ALIGNER_BLEUALIGN, filtervalue=0.25)
export_as_list(aligned_graph, "dumpedList.json")
export_as_graph(aligned_graph, "dumpedGraph.json")
imported_graph = import_as_graph("dumpedGraph.json")
#
# aligned_graph = create_graph_over_list_of_groups(allTaskByID, aligner=align.ALIGNER_BLEUALIGN, filtervalue=0.25)
# export_as_list(aligned_graph, "dumpedList.json")
# export_as_graph(aligned_graph, "dumpedGraph.json")


aligned_graph = align_a_sentence_to_the_others(group, id_of_sentence_to_be_aligned_to=3,
                                               aligner=align.ALIGNER_HUNALIGN, filtervalue=1)
print_graph_with_edges(aligned_graph)
export_as_list(aligned_graph, "dumpedList.json")
export_as_graph(aligned_graph, "dumpedGraph.json")

print(group)
improved = improve_sentence(group, group[3], experimental_improve=False)
print(group[3])
print(improved)

improved = improve_sentence(group, group[3], experimental_improve=True)
print(group[3])
print(improved)

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
