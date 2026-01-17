import arcade

from menu.menu import GameGUI
from handlers.screen_handler import check_screen, get_screen_data
from menu.screen_dialog import run_dialog
from menu.end_game import run_end_screen
from handlers.json_handler import writer, cleaner
from game.game import Game


def run():
    if check_screen():
        run_dialog(writer)
    _ = GameGUI(Game, cleaner, get_screen_data, run_end_screen)
    arcade.run()

if __name__ == "__main__":
    run()