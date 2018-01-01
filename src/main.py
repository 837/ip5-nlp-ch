from util import options, util
import networkx as nx

import alignGraph


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

    goldstandardWordCount = 0
    missingWords = 0
    foundWords = 0
    numberOfAlignedGroupes = len(createdAlignmentList)
    numberOfGSGroupes = len(goldstandardList)
    alignedWordCount = 0
    for alignments in createdAlignmentList:
        alignedWordCount += len(alignments)

    for alignments in goldstandardList:
        goldstandardWordCount += len(alignments)
        for word in alignments:
            if alignment_graph.has_node(word):
                foundWords += 1
            else:
                print("missing " + word)
                missingWords += 1

    scoreWords = (foundWords / goldstandardWordCount) * 100
    scoreGroups = (abs(numberOfGSGroupes - numberOfAlignedGroupes) / (
        numberOfGSGroupes + numberOfAlignedGroupes)) * 100
    totalScore = scoreWords - scoreGroups

    if should_print:
        print("goldstandardWordCount: " + str(goldstandardWordCount))
        print("alignedWordCount: " + str(alignedWordCount))
        print("missingWords: " + str(missingWords))
        print("foundWords: " + str(foundWords))
        print("numberOfAlignedGroupes: " + str(numberOfAlignedGroupes))
        print("numberOfGSGroupes: " + str(numberOfGSGroupes))
        print("difference(abs(numberOfGSGroupes-numberOfAlignedGroupes)): " + str(
            abs(numberOfGSGroupes - numberOfAlignedGroupes)))
        print("scoreWords: " + str(scoreWords))
        print("scoreGroups: " + str(scoreGroups))
        print("totalScore(higher is better): " + str(totalScore))

    print(str(additional_Text) + " scored: " + str(totalScore))
    return totalScore


def iterative_testing(total_iterations, current_iteration, current_params, gs_graph):
    print("####Iteration[" + str(current_iteration) + "]####")
    graph = ()
    iterationCount = 1
    for taskID in options.GOLD_STANDARD_SET:
        util.print_progress(iterationCount, len(options.GOLD_STANDARD_SET), prefix='Progress:', suffix='Complete')
        group = allTaskByID[taskID][0]
        graph = alignGraph.align_every_sentence_to_the_others(group, current_params[0], current_params[1],
                                                              current_params[2])

        iterationCount += 1
    score = calculate_alignment_score(gs_graph, graph, "With params[" + str(current_params) + "]", True)

    if current_iteration >= total_iterations:
        return
    else:
        current_params = [current_params[0], current_params[1], round(current_params[2] - 0.05, 2)]
        iterative_testing(total_iterations, current_iteration + 1, current_params, gs_graph)


allTaskByID = util.loadDataFromCSVFile('../data/transcribe-2017-07-08.CSV')

gs_graph = nx.json_graph.node_link_graph(
    util.load_json("GoldStandard/gs_graph.json"))  # LOAD GOLDSTANDARD_GRAPH FROM JSON

params = [nx.Graph(), alignGraph.ALIGNER_BLEUALIGN, 0.9]
iterative_testing(20, 1, params, gs_graph)

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
# for id in GOLD_STANDARD_SET:
#     util.print_progress(iterationCount, len(GOLD_STANDARD_SET), prefix='Progress:', suffix='Complete')
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
#     improved = align.improve(group, improve_index, align.HUNALIGN)
#     print(improved)
#     currentData.append(("improved sentence:", improved))
#
#     print("\nimproved sentence(with additional word filter):")
#     improved = align.improve(group, improve_index, align.HUNALIGN, use_bad_word_detection=True,
#                              group_score_for_filter_lower=0.6, group_score_for_filter_upper=0.91)
#     print(improved)
#     currentData.append(("improved sentence(with additional word filter):", improved))
#     alldata.append(currentData)
#     iterationCount += 1
#     print()
#     print()
#
# util.dump_dict_to_json(alldata, "BadSentenceCorrectionTest.json")
