import matplotlib.pyplot as plt
import numpy as np
import nltk




def filter_tasks_lesser_or_equal_than(n, tasks):
    return list(filter(lambda x: len(tasks[x][0]) > n, tasks))


def bleu_ratings(texts):
    texts = list(map(lambda x: x.lower(), texts))
    scores = []
    for t in texts:
        result = nltk.translate.bleu(list(filter(lambda x: x != t, texts)), t)
        scores.append(result)
    return scores


def reject_outliers(data, values, minscore=0.5):
    values = np.array(values)
    return np.array(data)[values > minscore].tolist(), values[values > minscore].tolist()


def getGoodTransscriptions(texts):
    r = bleu_ratings(texts)
    return reject_outliers(texts, r)


# texts, ratings = getGoodTransscriptions(allTaskByID[2048][0])
# print(texts, ratings)


# for taskID in filterTasksLesserOrEqualThan(2, allTaskByID):
#    texts, ratings = getGoodTransscriptions(allTaskByID[taskID][0])
#    print(ratings)

# print(ratings)
# print(bleu_ratings(allTaskByID[2096][0]))

# def histoStuff():
#     all = []
#     for taskID in filter_tasks_lesser_or_equal_than(2, allTaskByID):
#         # texts, ratings = getGoodTransscriptions(allTaskByID[taskID][0])
#         ratings = bleu_ratings(allTaskByID[taskID][0])
#         # if len(texts) > 0:
#         #     print(taskID)
#         #     print(texts)
#         for r in ratings:
#             all.append(r)
#
#     plt.hist(all, 200)
#     plt.show()
#     # print(np.sort(mins))
