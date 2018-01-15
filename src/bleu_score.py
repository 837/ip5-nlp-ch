import numpy as np
import nltk


# Define filter_tasks_lesser_or_equal_than(): Filters out all transcription groups which have less or equal to n transcriptions in it
def filter_tasks_lesser_or_equal_than(n, tasks):
    return list(filter(lambda x: len(tasks[x][0]) > n, tasks))


smoothFunction = nltk.translate.bleu_score.SmoothingFunction()


# Define bleu_ratings(): returns a list of nubers given a list of string, where each number represents the BLEU score of one sentence
# For Example: You give it an array with 4 transcriptions
# ["De Herdöpfel isch sehr fein","** Hertöpfel ** sehr **","Dä Härdöpfel ish sehr fein","Dä Häärdapfel isch sehr fein"]
# it then return an array containing the scores of each sentence like this: [0.8, 0.2, 0.78, 0.9]
# With these scores we can filter out outliers and get an estimate of how good the transcriptions in the group are.
# We also use a smoothing function to increase the likelihood of good ratings.
def bleu_ratings(texts):
    texts = list(map(lambda x: x.lower(), texts))
    scores = []
    for t in texts:
        result = nltk.translate.bleu(list(filter(lambda x: x != t, texts)), t,
                                     smoothing_function=smoothFunction.method7)
        scores.append(result)
    return scores


# Define reject_outliers(): Reject outliers returns a reduced list of data,
# given a list of data and a corresponding list of scores, based on a filtervalue
# It will return all sentences which scored above the indicated minscore.
def reject_outliers(data, values, minscore=0.5):
    values = np.array(values)
    return np.array(data)[values > minscore].tolist(), values[values > minscore].tolist()


# Define getGoodTranscriptions(): This takes texts from one transcription group and returns the same text, but with filtered out outliers
def getGoodTranscriptions(texts):
    r = bleu_ratings(texts)
    return reject_outliers(texts, r)


# Define max_index(): Returns the index of the highest number in a list
def max_index(values):
    return values.index(max(values))


# Define min_index(): Returns the index of the lowest number in a list
def min_index(values):
    return values.index(min(values))
