#import dependencies
import json
import os


#path constant
JSONPATH = 'data/cfg.json'


#generate empty file
def generate():
    try:
        with open(JSONPATH, mode='r', encoding='utf-8') as f:
            lines = f.readlines()
        first, last = lines[0], lines[-1]
        if first[0] != '{' or last[-1] != '}':
            with open(JSONPATH, mode='w', encoding='utf-8') as f:
                f.write("{}")
    except (OSError, IndexError):
        with open(JSONPATH, mode='w', encoding='utf-8') as f:
            f.write("{}")


#read from db
def reader():
    with open(JSONPATH, mode='r', encoding='utf-8') as f:
        data = json.load(f)
    return data


#write to db
def writer(screen, num):
    data = dict()
    data["screenNum"] = num
    data["screenName"] = screen.get_monitor_name()
    data["screenWidth"] = screen.width
    data["screenHeight"] = screen.height
    with open(JSONPATH, mode = 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
        f.flush()
        os.fsync(f.fileno())


#clean db file
def cleaner():
    with open(JSONPATH, mode='w', encoding='UTF-8') as f:
        pass
    generate()
