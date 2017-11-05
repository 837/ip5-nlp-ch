import os
import string
import spacy_test
import subprocess
from functools import reduce

import util

allTaskByID = util.loadDataFromCSVFile('../data/transcribe-2017-07-08.CSV')

texts, ratings = spacy_test.getGoodTransscriptions(allTaskByID[2048][0])
#
# swg1 = "mä hätt denn all zämegläseni lüt was mä hätt chöne zämetriibe allz was chopf und loch hewi müessi jetzt höwe, hetts allwe ghese".translate(
#     {ord(c): None for c in string.punctuation})
# swg2 = "ma hät denn alz zämeglääseni Lüt wasme het chäne zäämetriibe alz was chopf u loch hiigi müessi jetze höre hets alube gshiise".translate(
#     {ord(c): None for c in string.punctuation})
# swg3 = "Ma het dénn alz zäme glääseni Lüt was me hät chöne zämetriibe allz was Chopf u Loch hégi müessi ez höwe héts aube ghéésse".translate(
#     {ord(c): None for c in string.punctuation})
# swg4 = "ma het denn allz zäme glääsenei lüt was mer het chöne zämetribe alts was chopf u loch heegi müesi ez höve hets aube gheesse".translate(
#     {ord(c): None for c in string.punctuation})
#
# swg1 = reduce((lambda x, y: x + " " + y), list(swg1)).replace("   ", "\n")
# swg2 = reduce((lambda x, y: x + " " + y), list(swg2)).replace("   ", "\n")
# swg3 = reduce((lambda x, y: x + " " + y), list(swg3)).replace("   ", "\n")
# swg4 = reduce((lambda x, y: x + " " + y), list(swg4)).replace("   ", "\n")
sentences = []

for sentence in texts:
    sentences.append(reduce((lambda x, y: x + " " + y), list(sentence)).replace("   ", "\n"))

f1 = open('swg1.txt', 'wb')
f1.write(sentences[0].encode("utf8"))
f1.flush()

alignDict = dict()

for sentence in sentences:
    f2 = open('swg2.txt', 'wb')
    f2.write(sentence.encode("utf8"))
    f2.flush()

    output = subprocess.Popen(
        "Hunalign/hunalign.exe -text -realign -utf Hunalign/null.dict swg1.txt swg2.txt",
        stdout=subprocess.PIPE).communicate()[0]

    splitSentence = output.decode("utf8").split("\n")

    for sentence in splitSentence:
        words = sentence.split("\t")
        if len(words) >= 2:
            key = words[0].replace(" ", "").replace("~~~", " ")
            value = words[1].replace(" ", "").replace("~~~", " ")
            if key in alignDict:
                if not value in alignDict[key]:
                    alignDict[key].append(value)
            else:
                alignDict[key] = [value]

# print(alignDict)
print(alignDict["tänglet"])
print(spacy_test.getGoodTransscriptions(alignDict["tänglet"]))