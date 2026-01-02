import arcade
from menu.menu import gameGUI
from handlers.screen_handler import check_screen
from menu.screen_dialog import run_dialog


def run():
    if check_screen():
        run_dialog()
    _ = gameGUI()
    arcade.run()


if __name__ == "__main__":
    run()