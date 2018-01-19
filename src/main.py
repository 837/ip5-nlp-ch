import align
import bleu_score
from util import options, util

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


def align_a_sentence_to_the_others(group, aligner, filtervalue, id_of_sentence_to_be_aligned_to=-1,
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
print("Load Data")
allTaskByID = load_data_from_csv('../data/transcribe-2017-07-08.CSV')

print("Get group with ID 2048")
group = allTaskByID[2048][0]

print("Get good transcriptions")
good_transcriptions = get_good_transcriptions(group)

print("Align group")
aligned_graph = align_every_sentence_to_the_others(group, aligner=align.ALIGNER_BLEUALIGN, filtervalue=0.25)

print("Export as List")
export_as_list(aligned_graph, "dumpedList.json")

print("Export as Graph")
export_as_graph(aligned_graph, "dumpedGraph.json")

print("Print Graph")
print_graph_with_edges(aligned_graph)

print("Improve sentence")
improved = improve_sentence(group, group[3], aligner=align.ALIGNER_HUNALIGN, experimental_improve=False)
print(group[3])
print(improved)

improved = improve_sentence(group, group[3], aligner=align.ALIGNER_HUNALIGN, experimental_improve=True)
print(group[3])
print(improved)

print("Load Goldstandard")
gs_graph = nx.json_graph.node_link_graph(util.load_json("GoldStandard/gs_graph.json"))

print("Align Goldstandard Group")
aligned_graph = create_graph_over_list_of_groups(options.GOLD_STANDARD_SET, aligner=align.ALIGNER_BLEUALIGN,
                                                 filtervalue=0.25)

print("Export as List")
export_as_list(aligned_graph, "dumpedList.json")

print("Export as Graph")
export_as_graph(aligned_graph, "dumpedGraph.json")

print("Calculate Scores and print them")
calculate_alignment_score(gs_graph, aligned_graph, True)
