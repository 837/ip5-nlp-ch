import spacy
en_nlp = spacy.load('en')
de_nlp = spacy.load('de')
en_doc = en_nlp(u'Hello, world. Here are two sentences.')
de_doc = de_nlp(u'ich bin ein Berliner.')
print(spacy)
print(de_doc)
print(en_doc)


import pandas as pd
df = pd.read_csv('../data/swg2g.CSV', delimiter=';')


unique_sentences_id = set()
for id in df['TASK_ID']:
    unique_sentences_id.add(id)

df = df[['TASK_ID','INFO']].groupby(['TASK_ID'])

texts_grouped_by_id = []
for id in unique_sentences_id:
    texts_grouped_by_id.append(df.get_group(id))


for texts in texts_grouped_by_id:
    print(texts)
