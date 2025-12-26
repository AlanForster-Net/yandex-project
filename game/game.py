import arcade
import sqlite3

from arcade.examples.camera_platform import JUMP_SPEED
from pyglet.graphics import Batch
from arcade.experimental.query_demo import SCREEN_HEIGHT, SCREEN_WIDTH
from pyglet.event import EVENT_HANDLE_STATE
from screeninfo import get_monitors

# Constants
TITLE = "Run from antivirus! — Idle"
MONITOR = get_monitors()[0]
SCREEN_HEIGHT = MONITOR.height
SCREEN_WIDTH = MONITOR.width

# Player const
PLAYER_SPEED = 1.5
JUMP_SPEED = 10
MAX_JUMPS = 2
DASH_GAP = 60
SHIFT_SPEED = 3
SPEED_OF_USING_STAMINA = 0.12
STAMINA_REFRESH_SPEED = 0.5
STAMINA_USING_VALUE = 1.0

# Physic const
GRAVITY = 0.8
MAX_LEVEL = 1
TILE_SCALE = 2.5


# classes
class Player(arcade.Sprite):
    def __init__(self, x, y, scale=0.1):
        super().__init__('resources/img/Заглушка2.jpeg', scale=scale)
        self.scale = 0.05
        self.center_x = x
        self.center_y = y
        self.change_x = 0
        self.change_y = 0
        self.jumps_remaining = MAX_JUMPS
        self.max_jumps = MAX_JUMPS
        self.double_jump = False
        self.was_on_ground = False
        self.stamina = 3.0
        self.stamina_refresh_speed = STAMINA_REFRESH_SPEED
        self.stamina_using_speed = SPEED_OF_USING_STAMINA
        self.stamina_using_value = STAMINA_USING_VALUE

    def update(self, delta_time=1 / 60):
        super().update()


# ? Андрей
class WallOfDeath(arcade.Sprite):
    pass


class Game(arcade.Window):
    def __init__(self, n=1):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, title=TITLE, fullscreen=True)
        arcade.set_background_color(arcade.color.PINK)
        self.player = None
        self.player_list = None
        self.background_color = arcade.color.BLACK  # Устанавливаем фон
        self.tilemap = arcade.load_tilemap(f"resources/tile/tilemaps/tilemap{n}.tmx", scaling=TILE_SCALE)
        self.n = n
        self.walls = arcade.SpriteList()
        self.collisions = arcade.SpriteList()
        self.traps = arcade.SpriteList()
        self.bugs = arcade.SpriteList()
        self.end = arcade.SpriteList()
        self.init_scene(self.tilemap)
        self.left_pressed = False
        self.right_pressed = False
        self.space_pressed = False
        self.space_just_pressed = False
        self.shift_pressed = False
        self.dash_button = False
        self.timer_running = 0
        self.main_theme = arcade.load_sound("resources/sound/soundtrack.mp3")
        self.music_player = None

    def init_scene(self, tilemap):
        self.walls = self.tilemap.sprite_lists["wall"]
        self.collisions = self.tilemap.sprite_lists["collision"]
        self.traps = self.tilemap.sprite_lists["trap"]
        self.bugs = self.tilemap.sprite_lists["bug"]
        self.end = self.tilemap.sprite_lists["end"]

    def setup(self):
        self.music_player = self.main_theme.play(volume=0.3, loop=True)
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
                                                     gravity_constant=GRAVITY, )
        arcade.schedule(self.update_timer, 1.0)
        # Setup of databases
        # self.setup_players_database()


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
        # движение по горизонтале через физ движок
        if self.left_pressed and not self.right_pressed:
            self.player.change_x = -PLAYER_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x = PLAYER_SPEED
        elif not self.left_pressed and not self.right_pressed:
            self.player.change_x = 0

        # прыжок
        is_on_ground = self.pp_eng.can_jump()
        if is_on_ground:
            if not self.player.was_on_ground:
                self.player.jumps_remaining = self.player.max_jumps
                self.player.was_on_ground = True
        else:
            self.player.was_on_ground = False

        if self.space_just_pressed and self.player.jumps_remaining > 0 and self.player.stamina >= 1:
            self.player.change_y = JUMP_SPEED
            self.player.jumps_remaining -= 1
            self.space_just_pressed = False

        if not self.space_pressed:
            self.space_just_pressed = False

        # running (только если есть стамина)
        if self.shift_pressed and self.right_pressed and self.player.stamina > 0:
            self.player.change_x = SHIFT_SPEED
            self.player.stamina -= self.player.stamina_using_speed * delta_time
            if self.player.stamina < 0:
                self.player.stamina = 0
        elif self.shift_pressed and self.left_pressed and self.player.stamina > 0:
            self.player.stamina -= self.player.stamina_using_speed * delta_time
            self.player.change_x = -SHIFT_SPEED
            if self.player.stamina < 0:
                self.player.stamina = 0
        elif self.shift_pressed and self.right_pressed:
            self.player.change_x = PLAYER_SPEED
        elif self.shift_pressed and self.left_pressed:
            self.player.change_x = -PLAYER_SPEED

        # Dash
        if self.dash_button and self.right_pressed and self.player.stamina >= 1:
            self.player.stamina -= self.player.stamina_using_value
            self.player.change_x = 0
            self.player.center_x += DASH_GAP
            self.dash_button = False
        elif self.dash_button and self.left_pressed and self.player.stamina >= 1:
            self.player.stamina -= self.player.stamina_using_value
            self.player.change_x = 0
            self.player.center_x -= DASH_GAP
            self.dash_button = False

        pos = (self.player.center_x, self.player.center_y)
        self.player_camera.position = arcade.math.lerp_2d(self.player_camera.position,
                                                          pos,
                                                          0.14)
        self.player_list.update()
        self.enemy_list.update()

        # Test for "bugs"
        c_bugs = arcade.check_for_collision_with_list(self.player, self.bugs)
        for bug in c_bugs:
            bug.remove_from_sprite_lists()
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

    def update_timer(self, delta_time):
        self.timer_running += 1
        if self.player.stamina < 3.0:
            self.player.stamina += self.player.stamina_refresh_speed
            if self.player.stamina > 3.0:
                self.player.stamina = 3.0

    def next_level(self):
        if self.n == MAX_LEVEL:
            self.win_game()
        else:
            self.n += 1
            self.tilemap = arcade.load_tilemap(f"resources/tile/tilemaps/tilemap{self.n}.tmx")
            self.init_scene(self.tilemap)

    def gui_draw(self):
        pass

    def end_game(self):
        arcade.close_window()

    def win_game(self):
        arcade.close_window()

    def scores_and_results(self):
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:  # использовать Escape, для закрытия игры(заглушка, в будушем будет меню)
            arcade.close_window()
        if key == arcade.key.D:
            self.right_pressed = True
        if key == arcade.key.A:
            self.left_pressed = True
        if key == arcade.key.SPACE:
            self.space_pressed = True
            self.space_just_pressed = True
        if key == arcade.key.LSHIFT:
            self.shift_pressed = True
        if key == arcade.key.Q:
            self.dash_button = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.SPACE:
            self.space_pressed = False
        elif key == arcade.key.LSHIFT:
            self.shift_pressed = False
        elif key == arcade.key.Q:
            self.dash_button = False

    # def setup_players_database(self):
    #     con = sqlite3.connect("database_for_stats.sqlite")
    #     cur = con.cursor()
    #
    #     cur.execute("""CREATE TABLE IF NOT EXISTS players_infromation(
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     speed INTEGER,
    #     speed_of_jump INTEGER,
    #     max_jumps INTEGER,
    #     dash_gap INTEGER,
    #     shift_speed INTEGER,
    #     speed_of_using_stamina INTEGER,
    #     stamina_refresh_speed INTEGER,
    #     stamina_using_value INTEGER
    #     )""")
    #
    #     con.commit()
    #
    #     cur.execute(
    #         """INSERT INTO players_infromation(speed, speed_of_jump, max_jumps, dash_gap, shift_speed,
    #          speed_of_using_stamina, stamina_refresh_speed, stamina_using_value) VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", (
    #             PLAYER_SPEED,
    #             JUMP_SPEED,
    #             MAX_JUMPS,
    #             DASH_GAP,
    #             SHIFT_SPEED,
    #             SPEED_OF_USING_STAMINA,
    #             STAMINA_REFRESH_SPEED,
    #             STAMINA_USING_VALUE
    #         ))
    #     con.commit()
    #     con.close()

    def write_data_in_database(self):
        pass


def setup_game():
    win = Game(1)
    win.setup()
    arcade.run()


if __name__ == "__main__":
    setup_game()