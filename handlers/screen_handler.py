#import dependencies
import arcade
from handlers.json_handler import reader, generate


#check correction of screen in file
def check_screen():
    generate()
    data = reader()
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


#get info about screen from file
def get_screen_data(typ):
    try:
        data = reader()
        return data[typ]
    except KeyError:
        return 0
