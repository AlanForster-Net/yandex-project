import arcade
import sys
import fnmatch

from menu.menu import GameGUI
from handlers.screen_handler import check_screen, get_screen_data
from menu.screen_dialog import run_dialog
from handlers.json_handler import writer, cleaner
from game.game import Game
from menu.end_game import EndGame


class EmptyArgsError(Exception):
    pass


def run():
    screen = arcade.get_screens()[get_screen_data("screenNum")]
    window = arcade.Window(width=screen.width, height=screen.height, fullscreen=False, screen=screen)
    window.set_caption("Run from antivirus! — Idle")
    view = GameGUI(Game, cleaner, EndGame, window)
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    typ = str()
    for ar in sys.argv:
        if fnmatch.fnmatch(ar, 'type=*'):
            typ = ar.split('=')[1]
    if typ == 'dialog':
        if check_screen():
            run_dialog(writer)
    elif typ == 'run':
        run()
    else:
        raise EmptyArgsError('No args found')