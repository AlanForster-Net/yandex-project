import arcade
from handlers.json_handler import reader, generate


JSONPATH = 'data/cfg.json'


def check_screen():
    generate(JSONPATH)
    data = reader(JSONPATH)
    try:
        num = data["screenNum"]
        name_from_file = data["screenName"]
        width_from_file = data["screenWidth"]
        height_from_file = data["screenHeight"]
        screen_data = arcade.get_screens()[num]
    except KeyError:
        return 1
    if (name_from_file != screen_data.get_monitor_name() or
        width_from_file != screen_data.width or
        height_from_file != screen_data.height):
        return 1
    return 0


def get_screen_data(typ):
    try:
        data = reader(JSONPATH)
        return data[typ]
    except KeyError:
        return 0
