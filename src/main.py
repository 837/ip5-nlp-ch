import string
from functools import reduce
import matplotlib.pyplot as plt
import fizzle
import options
import util
import bleu_score
import align
import levenshtein
import pprint

allTaskByID = util.loadDataFromCSVFile('../data/transcribe-2017-07-08.CSV')

# CREATE ALIGNMENTS AND DUMP TO JSON FILE
iterationCount = 1
allAlignments = []
hun1toN = []
bleu1toN = []
hunNtoN = []
bleuNtoN = []
for taskID in options.GOLD_STANDARD_SET:
    util.print_progress(iterationCount, len(options.GOLD_STANDARD_SET), prefix='Progress:', suffix='Complete')
    group = allTaskByID[taskID][0]

    align.align_one_sentence_to_the_others(group, hun1toN, align.ALIGNER_HUNALIGN)
    align.align_one_sentence_to_the_others(group, bleu1toN, align.ALIGNER_BLEUALIGN)

    align.align_every_sentence_to_the_others(group, hunNtoN, align.ALIGNER_HUNALIGN)
    align.align_every_sentence_to_the_others(group, bleuNtoN, align.ALIGNER_BLEUALIGN)

    iterationCount += 1

util.dump_dict_to_json(hun1toN, "hun1toN.json")
util.dump_dict_to_json(bleu1toN, "bleu1toN.json")
util.dump_dict_to_json(hunNtoN, "hunNtoN.json")
util.dump_dict_to_json(bleuNtoN, "bleuNtoN.json")

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
