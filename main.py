import arcade
import sqlite3
from pyglet.graphics import Batch
from arcade.experimental.query_demo import SCREEN_HEIGHT, SCREEN_WIDTH
from pyglet.event import EVENT_HANDLE_STATE

# Constants
SCREEN_HEIGHT = 1024
SCREEN_WIDTH = 960
# Андрею: подумай над скоростью, а то в тесте это молния маквин получается
# И поработай с прыжком
PLAYER_SPEED = 2.5
GRAVITY = 1.0
MAX_LEVEL = 1
TILE_SCALE = 2.5

# classes
class Player(arcade.Sprite):
    def __init__(self, x, y, scale=0.1):
        super().__init__('заглушка.jpeg', scale=scale)
        self.center_x = x
        self.scale = scale
        self.center_y = y
        self.change_x = 0
        self.change_y = 0

    def update(self, delta_time=1/60):
        self.center_x += self.change_x
        super().update()

    def jump(self):
        pass


#? Андрей
class WallOfDeath(arcade.Sprite):
    pass


class Game(arcade.Window):
    def __init__(self, n=1, title="game"):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, title=title, fullscreen=True)
        arcade.set_background_color(arcade.color.PINK)
        self.player = None
        self.player_list = None
        self.background_color = arcade.color.BLACK  # Устанавливаем фон
        self.tilemap = arcade.load_tilemap(f"tilemaps/tilemap{n}.tmx", scaling=TILE_SCALE)
        self.n = n
        self.walls = arcade.SpriteList()
        self.collisions = arcade.SpriteList()
        self.traps = arcade.SpriteList()
        self.bugs = arcade.SpriteList()
        self.end = arcade.SpriteList()
        self.init_scene(self.tilemap)

    def init_scene(self, tilemap):
        self.walls = self.tilemap.sprite_lists["wall"]
        self.collisions = self.tilemap.sprite_lists["collision"]
        self.traps = self.tilemap.sprite_lists["trap"]
        self.bugs = self.tilemap.sprite_lists["bug"]
        self.end = self.tilemap.sprite_lists["end"]

    def setup(self):
        self.player = Player(100, 100 // 2, 0.5)
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
        self.pp_eng = arcade.PhysicsEnginePlatformer(player_sprite=self.player,
                                                     platforms=self.collisions,
                                                     gravity_constant=GRAVITY,)

    def on_draw(self):
        self.clear()
        # Player camera
        self.player_camera.use()
        self.walls.draw()
        self.traps.draw()
        self.end.draw()
        self.bugs.draw()
        self.player_list.draw()
        # GUI camera
        self.gui_camera.use()
        self.gui_draw()

    def on_update(self, delta_time=1 / 60):
        pos = (self.player.center_x, self.player.center_y)
        self.player_camera.position = arcade.math.lerp_2d(self.player_camera.position,
                                                          pos,
                                                          0.14)
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
        self.pp_eng.update()

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

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE: #использовать Escape, для закрытия игры(заглушка, в будушем будет меню)
            arcade.close_window()
        if key == arcade.key.D:
            self.player.change_x = PLAYER_SPEED #завивсит от динамики игры, надо обсудить будет
        if key == arcade.key.A:
            self.player.change_x = -PLAYER_SPEED

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
