import itertools
import spacy

en_nlp = spacy.load('en')
de_nlp = spacy.load('de')

import pandas as pd

df = pd.read_csv('../data/transcribe-2017-07-08.CSV', delimiter=';')
print(df['INFO'][0])

unique_sentences_id = set()
for id in df['TASK_ID']:
    unique_sentences_id.add(id)

allTextByTaskID = {}
for id in unique_sentences_id:
    allTextByTaskID[id] = []

for i in range(len(df)):
    allTextByTaskID[df['TASK_ID'][i]].append(df['INFO'][i])

# print(allTextByTaskID)  # mit allTextByTaskID[TASK_ID] bekommt man ein array mit allen INFO Saetzen



import nltk


def filterTasksLesserOrEqualThan(n, tasks):
    return list(filter(lambda x: len(tasks[x]) > n, tasks))


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


for taskID in filterTasksLesserOrEqualThan(2, allTextByTaskID):
    print(pairing1(allTextByTaskID[taskID]))
    print(pairing2(allTextByTaskID[taskID]))
