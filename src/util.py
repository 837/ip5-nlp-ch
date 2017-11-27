import pandas as pd
import json
import sys
from fizzle import *
from string import ascii_lowercase, ascii_uppercase

def loadDataFromCSVFile(filePath):
    df = pd.read_csv(filePath, delimiter=';')
    unique_sentences_id = set()
    for id in df['TASK_ID']:
        unique_sentences_id.add(id)

    allTaskByID = {}
    for id in unique_sentences_id:
        allTaskByID[id] = [[], []]
    for i in range(len(df)):
        allTaskByID[df['TASK_ID'][i]][0].append(df['INFO'][i])
        allTaskByID[df['TASK_ID'][i]][1].append(df['REF'][i])

    # print(allTaskByID)  # mit allTextByTaskID[TASK_ID] bekommt man ein array mit allen INFO Saetzen
    return allTaskByID


def dump_dict_to_json(data, filename):
    with open(filename, 'w') as fp:
        json.dump(data, fp, sort_keys=True, indent=4, ensure_ascii=False)


def load_dict_from_json(filename):
    try:
        with open(filename, 'r') as fp:
            data = json.load(fp)
        return data
    except FileNotFoundError:
        # create empty dict in file, try again
        dump_dict_to_json(dict(), filename)
        return load_dict_from_json(filename)


# Print iterations progress
# Props to: https://gist.github.com/aubricus/f91fb55dc6ba5557fbab06119420dd6a
def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


editCosts = [('ä', 'e', 0.2),  # default edit costs are 1
             ('e', 'ä', 0.2),
             ('i', 'y', 0.1),
             ('y', 'i', 0.1),
             ('e', 'é', 0.3),
             ('é', 'e', 0.3),
             ('b', 'p', 0.8),
             ('p', 'b', 0.8),
             ('n', 'm', 0.8),
             ('m', 'n', 0.8),
             ('d', 't', 0.8),
             ('t', 'd', 0.8),
             ]

for (l, u) in zip(ascii_lowercase, ascii_uppercase):
    editCosts.append((l, u, 0.1))
    editCosts.append((u, l, 0.1))


def nomalized_dl_distance(word1, word2):
    try:
        return dl_distance(word1, word2, substitutions=editCosts, symetric=False) / max(len(word1), len(word2))
    except ZeroDivisionError:
        return 1
