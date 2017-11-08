import pandas as pd
import json


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
    with open(filename, 'r') as fp:
        data = json.load(fp)
    return data
