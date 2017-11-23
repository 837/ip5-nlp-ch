import string
from functools import reduce

import fizzle
import util
import bleu_score
import align
import levenshtein

allTaskByID = util.loadDataFromCSVFile('../data/transcribe-2017-07-08.CSV')
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
texts, ratings = bleu_score.getGoodTransscriptions(allTaskByID[2047][0])

hun1toN = align.align_one_sentence_to_the_others(texts, 0, [], align.HUNALIGN)
hunNtoN = align.align_every_sentence_to_the_others(texts, [], align.HUNALIGN)
bleu1toN = align.align_one_sentence_to_the_others(texts, 0, [], align.BLEUALIGN)
bleuNtoN = align.align_every_sentence_to_the_others(texts, [], align.BLEUALIGN)

print("hun1toN: " + str(levenshtein.score_alignment(hun1toN)))
print("hunNtoN: " + str(levenshtein.score_alignment(hunNtoN)))
print("bleu1toN: " + str(levenshtein.score_alignment(bleu1toN)))
print("bleuNtoN: " + str(levenshtein.score_alignment(bleuNtoN)))
print(hun1toN)
print(bleu1toN)


#
# texts, ratings = bleu_score.getGoodTransscriptions(allTaskByID[2046][0])
# align.align_every_sentence_to_the_others(texts, util.load_dict_from_json("align_every_sentence_to_the_others.json"))
# align.align_one_sentence_to_the_others(texts, 0, util.load_dict_from_json("align_one_sentence_to_the_others.json"))
#
# texts, ratings = bleu_score.getGoodTransscriptions(allTaskByID[2045][0])
# align.align_every_sentence_to_the_others(texts, util.load_dict_from_json("align_every_sentence_to_the_others.json"))
# align.align_one_sentence_to_the_others(texts, 0, util.load_dict_from_json("align_one_sentence_to_the_others.json"))

# iterationCount = 0
# util.print_progress(iterationCount, len(allTaskByID), prefix='Progress:', suffix='Complete')
# for taskID in bleu_score.filter_tasks_lesser_or_equal_than(2, allTaskByID):
#     util.print_progress(iterationCount, len(allTaskByID), prefix='Progress:', suffix='Complete')
#     texts, ratings = bleu_score.getGoodTransscriptions(allTaskByID[taskID][0])
#     align.align_every_sentence_to_the_others(texts, util.load_dict_from_json("align_every_sentence_to_the_others.json"))
#     align.align_one_sentence_to_the_others(texts, 0, util.load_dict_from_json("align_one_sentence_to_the_others.json"))
#     iterationCount += 1

