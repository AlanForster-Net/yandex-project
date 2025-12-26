import json


def reader(path):
    with open(path, mode='r', encoding='utf-8') as f:
        data = json.load(f)
    return data