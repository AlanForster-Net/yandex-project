import arcade
from arcade.experimental.query_demo import SCREEN_HEIGHT, SCREEN_WIDTH

# Constants
SCREEN_HEIGHT = 1980
SCREEN_WIDTH = 1080

# Classes
class Level:
  pass


class Player(arcade.Sprite):
    def __init__(self, x, y, scale=0.1):
        super().__init__(x, y)


class Game(arcade.Window):
  def __init__(self):
    super().__init__(title="Game", fullscreen=True)

  def setup(self):
    pass


def setup_game():
  win = Game()
  win.setup()
  arcade.run()


if __name__ == "__main__":
  setup_game()
