import arcade
from menu.menu import gameGUI
from handlers.json_handler import reader
from menu.screen_dialog import Dialog

JSONPATH = 'data/cfg.json'


def check_chosen_screen():
    data = reader(JSONPATH)
    if "screen" in data.keys():
        return 0
    return 1


def get_screen():
    _ = Dialog()
    arcade.run()


def run():
    if check_chosen_screen():
        get_screen()
    _ = gameGUI()
    arcade.run()


if __name__ == "__main__":
    run()