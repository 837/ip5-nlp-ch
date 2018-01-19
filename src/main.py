from function_interface import *

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
export_as_list(aligned_graph, "tmp/dumpedList.json")

print("Export as Graph")
export_as_graph(aligned_graph, "tmp/dumpedGraph.json")

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
aligned_graph = create_graph_over_list_of_groups(options.GOLD_STANDARD_SET, allTaskByID,
                                                 aligner=align.ALIGNER_BLEUALIGN,
                                                 filtervalue=0.25)

print("Calculate Scores and print them")
calculate_alignment_score(gs_graph, aligned_graph, True)

print("Export as List")
export_as_list(aligned_graph, "tmp/dumpedList.json")

print("Export as Graph")
export_as_graph(aligned_graph, "tmp/dumpedGraph.json")
