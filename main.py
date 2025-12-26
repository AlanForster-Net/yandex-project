import arcade
from menu.menu import gameGUI


def run():
    win = gameGUI()
    arcade.run()


if __name__ == "__main__":
    run()