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
print(df['INFO'][0])
