import spacy

en_nlp = spacy.load('en')
de_nlp = spacy.load('de')

import pandas as pd

df = pd.read_csv('../data/swg2g_test.CSV', delimiter=';')
print(df['INFO'][0])

unique_sentences_id = set()
for id in df['TASK_ID']:
    unique_sentences_id.add(id)

allTextByTaskID = {}
for id in unique_sentences_id:
    allTextByTaskID[id]=[]

for i in range(len(df)):
    allTextByTaskID[df['TASK_ID'][i]].append(df['INFO'][i])

print(allTextByTaskID) #mit allTextByTaskID[TASK_ID] bekommt man ein array mit allen INFO Saetzen

for task in allTextByTaskID:
    allTextByTaskID[task] = [x for x in allTextByTaskID[task] if len(x.split()) >= 3 ]

print(allTextByTaskID)