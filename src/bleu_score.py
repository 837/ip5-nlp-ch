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


def getGoodTranscriptions(texts):
    r = bleu_ratings(texts)
    return reject_outliers(texts, r)


def max_index(values):
    return values.index(max(values))

def min_index(values):
    return values.index(min(values))