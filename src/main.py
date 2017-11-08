import util
import bleu_score
import align

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
# texts, ratings = bleu_score.getGoodTransscriptions(allTaskByID[2047][0])
# align.align_every_sentence_to_the_others(texts, util.load_dict_from_json("align_every_sentence_to_the_others.json"))
# align.align_one_sentence_to_the_others(texts, 0, util.load_dict_from_json("align_one_sentence_to_the_others.json"))
#
# texts, ratings = bleu_score.getGoodTransscriptions(allTaskByID[2046][0])
# align.align_every_sentence_to_the_others(texts, util.load_dict_from_json("align_every_sentence_to_the_others.json"))
# align.align_one_sentence_to_the_others(texts, 0, util.load_dict_from_json("align_one_sentence_to_the_others.json"))
#
# texts, ratings = bleu_score.getGoodTransscriptions(allTaskByID[2045][0])
# align.align_every_sentence_to_the_others(texts, util.load_dict_from_json("align_every_sentence_to_the_others.json"))
# align.align_one_sentence_to_the_others(texts, 0, util.load_dict_from_json("align_one_sentence_to_the_others.json"))

for taskID in bleu_score.filter_tasks_lesser_or_equal_than(2, allTaskByID):
    texts, ratings = bleu_score.getGoodTransscriptions(allTaskByID[taskID][0])
    align.align_every_sentence_to_the_others(texts, util.load_dict_from_json("align_every_sentence_to_the_others.json"))
    align.align_one_sentence_to_the_others(texts, 0, util.load_dict_from_json("align_one_sentence_to_the_others.json"))