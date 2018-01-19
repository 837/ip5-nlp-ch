import json
import sys
from string import ascii_lowercase, ascii_uppercase

import subprocess

import networkx as nx


def install_missing_dependencies(dependency):
    print("Installing missing dependency ["+str(dependency)+"]")
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    print(subprocess.Popen("python -m pip install " + dependency, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                     startupinfo=startupinfo).communicate()[0])

try:
    import pandas as pd
except ImportError:
    install_missing_dependencies("pandas")
    import pandas as pd

from util.fizzle import *


# Define loadDataFromCSVFile(): With this function we load only the to us necessary data from the provided files.
# It will return an array where you can look up transcription groups by their task_ID.
# mit allTaskByID[TASK_ID] bekommt man ein array mit allen INFO Saetzen
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

    # print(allTaskByID)  # mit allTaskByID[TASK_ID] bekommt man ein array mit allen INFO Saetzen
    return allTaskByID


# Define dump_data_to_json(): With this function you can dump any data to a json file
def dump_data_to_json(data, filename):
    with open(filename, 'w') as fp:
        json.dump(data, fp, sort_keys=True, indent=4, ensure_ascii=False)


# Define load_json(): With this function you can load a json file to data
def load_json(filename):
    with open(filename, 'r') as fp:
        data = json.load(fp)
    return data


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


editCosts = []  # default edit costs are 1


# Our custom edit cost for weighted levenshtein. where we define custom substitution costs.
def cost(a, b, score):
    editCosts.append((a, b, score))
    editCosts.append((b, a, score))


cost('i', 'y', 0.1)
cost('e', 'ä', 0.2)
cost('e', 'é', 0.2)
cost('e', 'è', 0.2)
cost('e', 'a', 0.5)
cost('ä', 'é', 0.2)
cost('ä', 'é', 0.2)
cost('ä', 'ë', 0.2)
cost('e', 'ë', 0.2)
cost('a', 'ë', 0.2)
cost('é', 'ë', 0.2)
cost('b', 'p', 0.8)
cost('n', 'm', 0.8)
cost('d', 't', 0.8)
cost('g', 'k', 0.8)
cost('Ä', 'ä', 0.1)
cost('Ü', 'ü', 0.1)
cost('Ö', 'ö', 0.1)

for (l, u) in zip(ascii_lowercase, ascii_uppercase):
    editCosts.append((l, u, 0.1))
    editCosts.append((u, l, 0.1))


# Define normalized_dl_distance() function: We use fizzles (https://github.com/nadvornix/python-fizzle) levenshtein distance implementation.
#  But to improve it, we added our modified editcosts to it. Further we normalize it to always get a value between 0 and 1.
# This function will therefore return a value between 0 and 1,
# where 0 means the words are identical and 1 means the words are completely different.
def normalized_dl_distance(word1, word2):
    try:
        return dl_distance(word1, word2, substitutions=editCosts, symetric=False) / max(len(word1), len(word2))
    except ZeroDivisionError:
        return 1


# Define flatten() function: As the name states, helper function to flatten a [[],[],...].
def flatten(li):
    return [item for sublist in li for item in sublist]


# Define convert_to_lower() function: As the name states, helper function to make text lowercase.
def convert_to_lower(texts):
    return map(str.lower, texts)


# Define remove_punctuation() function: With this function you can strip , . : ! - from text, all the
# other symbols that appear in the text are used to indicate missing words or letters, so we don't remove
def remove_punctuation(texts):
    return map((lambda t: t.replace(",", ' ').replace(".", ' ').replace(":", ' ').replace("!", ' ').replace("-", ' ')),
               texts)

def print_graph_with_edges(G):
    import pylab
    print("Creating Graph to display, might take a long time.")
    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True, font_weight='bold', pos=pos)
    edge_labels = dict([((u, v,), d['weight'])
                        for u, v, d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    pylab.show()

