from nltk.translate.bleu_score import SmoothingFunction

import util
import nltk

allTaskByID = util.loadDataFromCSVFile('../data/swg2g.CSV')


def filterTasksLesserOrEqualThan(n, tasks):
    return list(filter(lambda x: len(tasks[x][0]) > n, tasks))


def bleu_ratings(task):
    scores = []

    cc = SmoothingFunction()
    print(task[0])
    print(task[1])
    for t in task[0]:
        result = nltk.translate.bleu_score.sentence_bleu(task[1][0], t, smoothing_function=SmoothingFunction().method0)
        scores.append(result)
    return scores


print(bleu_ratings(allTaskByID[2540]))
