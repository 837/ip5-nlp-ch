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


def reject_outliers(data, values, m = 2.):
    values = np.array(values)
    d = np.abs(values - np.median(values))
    mdev = np.median(d)
    s = d/(mdev if mdev else 1.)
    return np.array(data)[s < m].tolist()


def getGoodTransscriptions(texts):
    r = pairing2(texts)
    return reject_outliers(texts, r)


print(getGoodTransscriptions(allTaskByID[2048][0]))


