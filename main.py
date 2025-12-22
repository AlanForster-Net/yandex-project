import arcade
import sqlite3
from pyglet.graphics import Batch
from arcade.experimental.query_demo import SCREEN_HEIGHT, SCREEN_WIDTH
from pyglet.event import EVENT_HANDLE_STATE

# Constants
SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 900

GRAVITY = 1.0
MAX_LEVEL = 10

# Classes
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
        super().update()

    def jump(self):
        pass
#? Андрей
class WallOfDeath(arcade.Sprite):
    pass


class Game(arcade.Window):
    def __init__(self, n, title="game"):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, title=title, fullscreen=True)
        self.player = None
        self.player_list = None
        self.background_color = arcade.color.BLACK  # Устанавливаем фон
        self.tilemap = arcade.load_tilemap(f"tilemaps/tilemap_{n}.tmx")
        self.n = n

    def init_scene(self, tilemap):
        self.walls = self.tilemap.sprite_lists["wall"]
        self.collisions = self.tilemap.sprite_lists["collision"]
        self.traps = self.tilemap.sprite_lists["trap"]
        self.bugs = self.tilemap.sprite_lists["bug"]
        self.end = self.tilemap.sprite_lists["end"]

    def setup(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 1)
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        self.bug_count = 0
        # Sprites
        self.wall_of_death = WallOfDeath()
        self.enemy_list = arcade.SpriteList()
        self.enemy_list.append(self.wall_of_death)
        # Camera
        self.player_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()
        # Physics engine
        self.pp_eng = arcade.PhysicsEnginePlatformer(player_sprite=self.player_list[0],
                                                     platforms=self.walls,
                                                     gravity_constant=GRAVITY)

    def on_draw(self):
        self.clear()
        self.init_scene(self.tilemap)
        self.clear()
        #? arcade.start_render()
        self.player_list.draw()
        self.walls.draw()
        self.traps.draw()
        self.end.draw()
        self.player_camera.use()
        self.player_list.draw()
        self.gui_camera.use()
        self.gui_draw()

    def on_update(self, delta_time=1 / 60):
        self.pp_eng.update()
        self.player_list.update()
        self.enemy_list.update()
        #? self.traps.update()
        # Test for "bugs"
        c_bugs = arcade.check_for_collision_with_list(self.player, self.bugs)
        for bug in c_bugs:
            bug.remove_from_sprite_lists() #? Syntax error ?
            self.bug_count += 1
        # Test for death
        if arcade.check_for_collision(self.player, self.wall_of_death):
            self.end_game()
        if len(arcade.check_for_collision_with_list(self.player, self.traps)) != 0:
            self.end_game()
        # Test for success
        if len(arcade.check_for_collision_with_list(self.player, self.end)) != 0:
            self.scores_and_results()
            self.write_data_in_database()
            self.next_level()

    def next_level(self):
        if self.n == MAX_LEVEL:
            self.win_game()
        else:
            self.n += 1
            self.tilemap = arcade.load_tilemap(f"tilemaps/tilemap{self.n}.tmx")
            self.init_scene(self.tilemap)

    def gui_draw(self):
        pass

    def end_game(self):
        pass

    def scores_and_results(self):
        pass
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

    def write_data_in_database(self):
        pass

def setup_game():
    win = Game(1)
    win.setup()
    arcade.run()


if __name__ == "__main__":
    setup_game()
