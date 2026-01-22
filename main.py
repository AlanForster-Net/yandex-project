#Run from antivirus! copyright Konzhin, Seleznev, Nefedov. 2025-2026
#import of dependencies
import arcade
import sys
import fnmatch
import pyglet
#import funcs and classes
from menu.menu import GameGUI
from handlers.screen_handler import check_screen, get_screen_data
from menu.screen_dialog import run_dialog
from handlers.json_handler import writer, cleaner
import handlers.bd_handler as bd_handler
from game.game import Game
from menu.end_game import EndGame
from menu.statistics import Statistics

#class of error
class EmptyArgsError(Exception):
    pass

#icon consts
ICON_F = 'resources/img/icon.png'
ICON = pyglet.image.load(ICON_F)

#running of main game window
def run():
    screen = arcade.get_screens()[get_screen_data("screenNum")]
    window = arcade.Window(width=screen.width, height=screen.height, fullscreen=False, screen=screen)
    window.set_icon(ICON)
    view = GameGUI(Game, cleaner, EndGame, window, ICON_F, bd_handler, Statistics)
    window.show_view(view)
    arcade.run()

#function to work with sys args and run game
#entry point of game
if __name__ == "__main__":
    typ = str()
    for ar in sys.argv:
        if fnmatch.fnmatch(ar, 'type=*'):
            typ = ar.split('=')[1]
    if typ == 'dialog':
        if check_screen():
            run_dialog(writer, ICON)
    elif typ == 'run':
        run()
    else:
        raise EmptyArgsError('No args found. Please read readme before starting the game')