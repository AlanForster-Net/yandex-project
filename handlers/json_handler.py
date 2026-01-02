import json


def generate(path):
    try:
        with open(path, mode='r', encoding='utf-8') as f:
            lines = f.readlines()
        first, last = lines[0], lines[-1]
        if first[0] != '{' or last[-1] != '}':
            with open(path, mode='w', encoding='utf-8') as f:
                f.write("{}")
    except OSError:
        with open(path, mode='w', encoding='utf-8') as f:
            f.write("{}")


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
    print(path)
    with open(path, mode = 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
