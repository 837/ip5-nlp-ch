import itertools

import nltk
import util

allTaskByID = util.loadDataFromCSVFile('../data/transcribe-2017-07-08.CSV')


def filterTasksLesserOrEqualThan(n, tasks):
    return list(filter(lambda x: len(tasks[x][0]) > n, tasks))


def pairing1(texts):
    scores = []
    for (t1, index) in zip(texts, itertools.count()):
        scores.append(0)
        for t2 in texts:
            scores[index] += nltk.translate.bleu_score.sentence_bleu([t1], t2)
        scores[index] /= len(texts)

    return scores


def pairing2(texts):
    scores = []
    for t in texts:
        result = nltk.translate.bleu_score.sentence_bleu(list(filter(lambda x: x != t, texts)), t)
        scores.append(result)
    return scores


print(pairing1(allTaskByID[2048][0]))
print(pairing2(allTaskByID[2048][0]))

for taskID in filterTasksLesserOrEqualThan(2, allTaskByID):
    print(pairing1(allTaskByID[taskID][0]))
    print(pairing2(allTaskByID[taskID][0]))
