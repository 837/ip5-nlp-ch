from algorithms import align
from algorithms import bleu_score

from algorithms import alignment_score
from util import options, util

try:
    import networkx as nx
except ImportError:
    util.install_missing_dependencies("networkx")
    import networkx as nx


def calculate_alignment_score(gs_graph, alignment_graph, should_print=False):
    alignment_score.calculate_alignment_score(gs_graph, alignment_graph, should_print)


def print_graph_with_edges(G):
    util.print_graph_with_edges(G)


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


def create_graph_over_list_of_groups(list_of_groups, allTaskByID, aligner, filtervalue,
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
