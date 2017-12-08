import string
from functools import reduce
import matplotlib.pyplot as plt
import fizzle
import util
import bleu_score
import align
import levenshtein
import pprint

allTaskByID = util.loadDataFromCSVFile('../data/transcribe-2017-07-08.CSV')

GOLD_STANDARD_SET = [2358]  # [2048, 2095, 2080, 2358, 2374]  # , 1842, 1851, 1930, 1934, 1967]

# allTaskByID = {k: allTaskByID[k] for k in list(allTaskByID)[:100]}
#
# texts, ratings = bleu_score.getGoodTransscriptions(allTaskByID[2048][0])
#
# align.align_one_sentence_to_the_others(texts, 0, util.load_dict_from_json("emptydict.json"))
#
# align.align_every_sentence_to_the_others(texts, util.load_dict_from_json("emptydict.json"))

# print("###############align_one_sentence_to_the_others###############")
# print(util.load_dict_from_json("align_one_sentence_to_the_others.json"))
# print()
# print("###############################################################")
# print("###############################################################")
# print("###############################################################")
# print()
# print("###############align_every_sentence_to_the_others###############")
# print(util.load_dict_from_json("align_every_sentence_to_the_others.json"))
# #
# texts, ratings = bleu_score.getGoodTransscriptions(allTaskByID[2047][0])
#
# hun1toN = align.align_one_sentence_to_the_others(texts, 0, [], align.HUNALIGN)
# hunNtoN = align.align_every_sentence_to_the_others(texts, [], align.HUNALIGN)
# bleu1toN = align.align_one_sentence_to_the_others(texts, 0, [], align.BLEUALIGN)
# bleuNtoN = align.align_every_sentence_to_the_others(texts, [], align.BLEUALIGN)
#
#
# pp = pprint.PrettyPrinter(indent=2)
#
# print("hun1toN: " + str(levenshtein.score_alignment(hun1toN)))
# print("hunNtoN: " + str(levenshtein.score_alignment(hunNtoN)))
# print("bleu1toN: " + str(levenshtein.score_alignment(bleu1toN)))
# print("bleuNtoN: " + str(levenshtein.score_alignment(bleuNtoN)))
# pp.pprint(hun1toN)
# print("================================================")
# pp.pprint(bleu1toN)


#
# texts, ratings = bleu_score.getGoodTransscriptions(allTaskByID[2046][0])
# align.align_every_sentence_to_the_others(texts, util.load_dict_from_json("align_every_sentence_to_the_others.json"))
# align.align_one_sentence_to_the_others(texts, 0, util.load_dict_from_json("align_one_sentence_to_the_others.json"))
#
# texts, ratings = bleu_score.getGoodTransscriptions(allTaskByID[2045][0])
# align.align_every_sentence_to_the_others(texts, util.load_dict_from_json("align_every_sentence_to_the_others.json"))
# align.align_one_sentence_to_the_others(texts, 0, util.load_dict_from_json("align_one_sentence_to_the_others.json"))

# iterationCount = 1
# hunNtoN = []
# bleuNtoN = []
# filtered = bleu_score.filter_tasks_lesser_or_equal_than(2, allTaskByID)
# for taskID in filtered:
#     util.print_progress(iterationCount, len(filtered), prefix='Progress:', suffix='Complete')
#     texts, ratings = bleu_score.getGoodTransscriptions(allTaskByID[taskID][0])
#     align.align_every_sentence_to_the_others(texts, hunNtoN, align.HUNALIGN)
#     align.align_every_sentence_to_the_others(texts, bleuNtoN, align.BLEUALIGN)
#     iterationCount += 1
#
# util.dump_dict_to_json(hunNtoN, "hunNtoN.json")
# util.dump_dict_to_json(bleuNtoN, "bleuNtoN.json")
# pp = pprint.PrettyPrinter(indent=2)

# print("\nhun1toN: " + str(levenshtein.score_alignment(hun1toN)))
# pp.pprint(hun1toN)
# print("================================================\n")
# print("bleu1toN: " + str(levenshtein.score_alignment(bleu1toN)))
# pp.pprint(bleu1toN)

# plt.hist(align.distances, 100)
# plt.show()


# CREATE ALIGNMENTS AND DUMP TO JSON FILE
# iterationCount = 1
# allAlignments = []
# for taskID in GOLD_STANDARD_SET:
#     util.print_progress(iterationCount, len(GOLD_STANDARD_SET), prefix='Progress:', suffix='Complete')
#     allAlignments.append(taskID)
#     hun1toN = []
#     bleu1toN = []
#     hunNtoN = []
#     bleuNtoN = []
#     group = allTaskByID[taskID][0]
#     best_index = bleu_score.max_index(bleu_score.bleu_ratings(group))
#     # print(group)
#     # print(group[best_index])
#     # print(best_index)
#     align.align_one_sentence_to_the_others(group, best_index, hun1toN, align.HUNALIGN, 1)
#     align.align_one_sentence_to_the_others(group, best_index, bleu1toN, align.BLEUALIGN, 1)
#     align.align_every_sentence_to_the_others(group, hunNtoN, align.HUNALIGN, 1)
#     align.align_every_sentence_to_the_others(group, bleuNtoN, align.BLEUALIGN, 1)
#     allAlignments.append(hun1toN)
#     allAlignments.append(bleu1toN)
#     allAlignments.append(hunNtoN)
#     allAlignments.append(bleuNtoN)
#     iterationCount += 1
#
# util.dump_dict_to_json(allAlignments, "allAlignments.json")

alldata = []
iterationCount = 1
for id in GOLD_STANDARD_SET:
    util.print_progress(iterationCount, len(GOLD_STANDARD_SET), prefix='Progress:', suffix='Complete')
    currentData = []
    group = allTaskByID[id][0]
    if len(group) < 2:
        iterationCount += 1
        continue
    print(group)
    print("Group Nr.: " + str(id))
    currentData.append("Group Nr.: " + str(id))

    print("good sentence:")
    goodTranscriptions = bleu_score.getGoodTranscriptions(group)
    group = goodTranscriptions[0]
    scores = goodTranscriptions[1]
    best_index = bleu_score.max_index(scores)
    print(group[best_index])
    currentData.append(("good sentence:", group[best_index]))

    print("\nbad sentence:")
    improve_index = bleu_score.min_index(scores)
    print(group[improve_index])
    currentData.append(("bad sentence:", group[improve_index]))

    print("\nimproved sentence:")
    improved = align.improve(group, improve_index, align.HUNALIGN)
    print(improved)
    currentData.append(("improved sentence:", improved))

    print("\nimproved sentence(with additional word filter):")
    improved = align.improve(group, improve_index, align.HUNALIGN, use_bad_word_detection=True,
                             group_score_for_filter_lower=0.6, group_score_for_filter_upper=0.91)
    print(improved)
    currentData.append(("improved sentence(with additional word filter):", improved))
    alldata.append(currentData)
    iterationCount += 1
    print()
    print()

util.dump_dict_to_json(alldata, "BadSentenceCorrectionTest.json")
