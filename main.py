import arcade

# Constants


# Classes
class Level:
  pass


class Player:
  pass


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
