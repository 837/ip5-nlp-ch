import string
from functools import reduce

import fizzle
import util
import bleu_score
import align
import levenshtein
import pprint

allTaskByID = util.loadDataFromCSVFile('../data/transcribe-2017-07-08.CSV')
allTaskByID = {k: allTaskByID[k] for k in list(allTaskByID)[:10]}
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

iterationCount = 0
hun1toN = []
bleu1toN = []
util.print_progress(iterationCount, len(allTaskByID), prefix='Progress:', suffix='Complete')
for taskID in bleu_score.filter_tasks_lesser_or_equal_than(2, allTaskByID):
    util.print_progress(iterationCount, len(allTaskByID), prefix='Progress:', suffix='Complete')
    texts, ratings = bleu_score.getGoodTransscriptions(allTaskByID[taskID][0])
    align.align_one_sentence_to_the_others(texts, 0, hun1toN, align.HUNALIGN)
    align.align_one_sentence_to_the_others(texts, 0, bleu1toN, align.BLEUALIGN)
    iterationCount += 1


pp = pprint.PrettyPrinter(indent=2)

print("hun1toN: " + str(levenshtein.score_alignment(hun1toN)))
print("bleu1toN: " + str(levenshtein.score_alignment(bleu1toN)))
pp.pprint(hun1toN)
print("================================================")
pp.pprint(bleu1toN)
