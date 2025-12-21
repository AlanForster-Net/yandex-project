import arcade
from arcade.experimental.query_demo import SCREEN_HEIGHT, SCREEN_WIDTH
from pyglet.event import EVENT_HANDLE_STATE

# Constants
SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 900


# Classes
class Level:
    pass


class Player(arcade.Sprite):
    def __init__(self, x, y, scale=1.0):
        super().__init__('заглушка.jpeg', scale=scale)
        self.center_x = x
        self.scale = scale
        self.center_y = y
        self.change_x = 0
        self.change_y = 0

    def update(self, delta_time):
        self.center_x += self.change_x

    def jump(self):
        pass


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Game", fullscreen=True)
        self.player = None
        self.player_list = None
        self.background_color = arcade.color.BLACK  # Устанавливаем фон

    def setup(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 1)
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

    def on_draw(self):
        self.clear()
        self.player_list.draw()

    def on_update(self, delta_time):
        self.player.update(delta_time)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE: #использовать Escape, для закрытия игры(заглушка, в будушем будет меню)
            arcade.close_window()
        if key == arcade.key.D:
            self.player.change_x = 10 #завивсит от динамики игры, надо обсудить будет
        if key == arcade.key.A:
            self.player.change_x = -10

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A and self.player.change_x < 0:
            self.player.change_x = 0
        elif key == arcade.key.D and self.player.change_x > 0:
            self.player.change_x = 0

def setup_game():
    win = Game()
    win.setup()
    arcade.run()


if __name__ == "__main__":
    setup_game()
