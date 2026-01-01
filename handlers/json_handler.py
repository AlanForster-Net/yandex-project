import json


def reader(path):
    with open(path, mode='r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def writer(path, screen, num):
    data = dict()
    data["screenNum"] = num
    data["screenName"] = screen.get_monitor_name()
    data["screenWidth"] = screen.width
    data["screenHeight"] = screen.height
    with open(path, mode = 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)