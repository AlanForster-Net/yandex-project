import arcade
import sqlite3

from arcade.examples.camera_platform import JUMP_SPEED
from pyglet.graphics import Batch
from arcade.experimental.query_demo import SCREEN_HEIGHT, SCREEN_WIDTH
from pyglet.event import EVENT_HANDLE_STATE
from handlers.screen_handler import get_screen_data


# Constants
TITLE = "Run from antivirus! — Level 1"
SCREEN = arcade.get_screens()[get_screen_data("screenNum")]

# Player const
PLAYER_SPEED = 1.5
LADDER_SPEED = 2
JUMP_SPEED = 10
MAX_JUMPS = 2
DASH_GAP = 60
SHIFT_SPEED = 3
SPEED_OF_USING_STAMINA = 0.2
STAMINA_REFRESH_SPEED = 0.5
STAMINA_USING_VALUE = 1.0

# Enemy const
ENEMY_SPEED = 150
# Physic const
GRAVITY = 0.8
MAX_LEVEL = 5
TILE_SCALE = 2.5


# classes
class Player(arcade.Sprite):
    def __init__(self, x, y, scale=2):
        super().__init__('resources/players_frames/pack1/idle.png', scale=scale)
        #some attributes
        self.live = True
        self.pack_of_skin = 1
        #posiotion of player
        self.center_x = x
        self.center_y = y
        self.change_x = 0
        self.change_y = 0
        #movement things
        self.jumps_remaining = MAX_JUMPS
        self.max_jumps = MAX_JUMPS
        self.double_jump = False
        self.was_on_ground = False
        self.stamina = 3.0
        self.stamina_refresh_speed = STAMINA_REFRESH_SPEED
        self.stamina_using_speed = SPEED_OF_USING_STAMINA
        self.stamina_using_value = STAMINA_USING_VALUE
        #textures
        self.frames = dict()
        self.frames["running_right"] = list()
        self.frames["running_left"] = list()
        self.frames["running_jump"] = list()
        self.frames["die"] = None
        self.frames["idle"] = None
        self.frames["jump"] = None
        #base skin
        self.frames["die"] = arcade.load_texture("resources/players_frames/pack1/die.png")
        self.frames["idle"] = arcade.load_texture("resources/players_frames/pack1/idle.png")
        self.frames["jump"] = arcade.load_texture("resources/players_frames/pack1/jump.png")
        for i in range(1, 5):
            self.frames["running_right"].append(arcade.load_texture(f"resources/players_frames/pack1/run_r_{i}.png"))

        for i in range(1, 5):
            self.frames["running_left"].append(arcade.load_texture(f"resources/players_frames/pack1/run_l_{i}.png"))

        #animation
        self.current_frame = 0
        self.animation_speed = 0.0
        self.animation_timer = 0

    def update(self, delta_time=1 / 60):
        super().update()
        #easter with "капустка"
        if self.pack_of_skin == "easter_pack":
            self.texture = arcade.load_texture("resources/players_frames/easter_pack/капустка.jpg")
            return
        #checking for alive and change texture
        if not self.live:
            self.texture = self.frames["die"]
            return
        #animation
        self.animation_timer += delta_time
        if self.change_y != 0:
            self.texture = self.frames["jump"]
        if abs(self.change_x) == PLAYER_SPEED:
            self.animation_speed = 0.2
            if self.change_x > 0:
                if self.animation_timer >= self.animation_speed:
                    self.animation_timer = 0
                    self.current_frame = (self.current_frame + 1) % 4
                    self.texture = self.frames["running_right"][self.current_frame]
            elif self.change_x < 0:
                if self.animation_timer >= self.animation_speed:
                    self.animation_timer = 0
                    self.current_frame = (self.current_frame + 1) % 4
                    self.texture = self.frames["running_left"][self.current_frame]
        elif abs(self.change_x) == 2 * PLAYER_SPEED:
            self.animation_speed = 0.1
            if self.change_x > 0:
                if self.animation_timer >= self.animation_speed:
                    self.animation_timer = 0
                    self.current_frame = (self.current_frame + 1) % 4
                    self.texture = self.frames["running_right"][self.current_frame]

            elif self.change_x < 0:
                if self.animation_timer >= self.animation_speed:
                    self.animation_timer = 0
                    self.current_frame = (self.current_frame + 1) % 4
                    self.texture = self.frames["running_left"][self.current_frame]

        elif abs(self.change_x) == 0:
            self.texture = self.frames["idle"]
            self.animation_timer = 0

    def update_skin(self, pack_of_skin):
        self.pack_of_skin = pack_of_skin
        #easter pack
        if self.pack_of_skin == "easter_pack":
            self.scale = 0.05
            self.center_y = 150
            return
        #texture from normal packs
        self.frames["die"] = arcade.load_texture(f"resources/players_frames/pack{pack_of_skin}/die.png")
        self.frames["idle"] = arcade.load_texture(f"resources/players_frames/pack{pack_of_skin}/idle.png")
        self.frames["jump"] = arcade.load_texture(f"resources/players_frames/pack{pack_of_skin}/jump.png")
        self.frames["running_right"].clear()
        self.frames["running_left"].clear()
        for i in range(1, 5):
            self.frames["running_right"].append(arcade.load_texture(f"resources/players_frames/pack{pack_of_skin}/run_r_{i}.png"))

        for i in range(1, 5):
            self.frames["running_left"].append(arcade.load_texture(f"resources/players_frames/pack{pack_of_skin}/run_l_{i}.png"))

class WallOfDeath(arcade.Sprite):
    def __init__(self, x, y, scale=1.25):
        super().__init__('resources/img/variant_for_wall.png', scale=scale)
        self.center_x = x
        self.center_y = y

        self.frames = [arcade.load_texture("resources/img/variant_for_wall.png"),
                       arcade.load_texture("resources/img/variant_for_wall_2.png")]
        self.animation_speed = 5.0
        self.current_frame = 0
        self.animation_timer = 0

        self.expending_speed = ENEMY_SPEED
        self.width = self.width // 8
        self.height *= 2

    def update(self, delta_time):
        # self.width += delta_time * self.expending_speed
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % 2
            self.texture = self.frames[self.current_frame]

class Game(arcade.Window):
    def __init__(self, n=1, title="game"):
        super().__init__(get_screen_data("screenWidth"), get_screen_data("screenHeight"), title=title, fullscreen=True,
                         screen=SCREEN)
        arcade.set_background_color(arcade.color.PINK)
        self.player = None
        self.player_list = None
        self.background_color = arcade.color.BLACK
        self.n = 1
        self.tilemap = arcade.load_tilemap(f"resources/tile/tilemaps/tilemap{self.n}.tmx", scaling=TILE_SCALE)
        self.walls = arcade.SpriteList()
        self.collisions = arcade.SpriteList()
        self.traps = arcade.SpriteList()
        self.bugs = arcade.SpriteList()
        self.end = arcade.SpriteList()
        self.walls = self.tilemap.sprite_lists["wall"]
        self.collisions = self.tilemap.sprite_lists["collision"]
        self.traps = self.tilemap.sprite_lists["trap"]
        self.bugs = self.tilemap.sprite_lists["bug"]
        self.end = self.tilemap.sprite_lists["end"]
        self.left_pressed = False
        self.right_pressed = False
        self.space_pressed = False
        self.space_just_pressed = False
        self.shift_pressed = False
        self.dash_button = False
        self.w_pressed = False
        self.s_pressed = False
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
        self.player = Player(100, 100 // 2, 4)
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        self.bug_count = 0
        self.wall_of_death = WallOfDeath(-100, 230)
        self.enemy_list = arcade.SpriteList()
        self.enemy_list.append(self.wall_of_death)
        self.player_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()
        self.pp_eng = arcade.PhysicsEnginePlatformer(player_sprite=self.player,
                                                     platforms=self.collisions,
                                                     gravity_constant=GRAVITY)
        arcade.schedule(self.update_timer, 1.0)
        self.setup_players_database()

    def on_draw(self):
        self.clear()
        self.player_camera.use()
        self.walls.draw()
        self.traps.draw()
        self.end.draw()
        self.bugs.draw()
        self.player_list.draw()
        self.enemy_list.draw()
        self.gui_camera.use()
        self.gui_draw()

    def gui_draw(self):
        arcade.draw_lbwh_rectangle_filled(SCREEN_WIDTH - 275, 25, 305, 50, arcade.color.WHITE)
        if self.player.stamina >= 1:
            arcade.draw_lbwh_rectangle_filled(SCREEN_WIDTH - 270, 28, 95, 44, arcade.color.BLACK)
        if self.player.stamina >= 2:
            arcade.draw_lbwh_rectangle_filled(SCREEN_WIDTH - 170, 28, 95, 44, arcade.color.BLACK)
        if self.player.stamina >= 3:
            arcade.draw_lbwh_rectangle_filled(SCREEN_WIDTH - 70, 28, 95, 44, arcade.color.BLACK)

    def on_update(self, delta_time=1 / 60):
        self.pp_eng.update()
        if self.left_pressed and not self.right_pressed:
            self.player.change_x = -PLAYER_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x = PLAYER_SPEED
        elif not self.left_pressed and not self.right_pressed:
            self.player.change_x = 0
        #climbing on ladder
        is_on_ladder = self.pp_eng.is_on_ladder()
        if is_on_ladder:
            # По лестнице вверх/вниз
            if self.w_pressed and not self.s_pressed:
                self.player.change_y = LADDER_SPEED
            elif self.s_pressed and not self.w_pressed:
                self.player.change_y = -LADDER_SPEED
            else:
                self.player.change_y = 0
        #jump
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
        #running
        if self.shift_pressed and self.right_pressed and self.player.stamina > 0:
            self.player.change_x = SHIFT_SPEED
            self.player.stamina -= self.player.stamina_using_speed * delta_time
            self.player.running_right = True
            if self.player.stamina < 0:
                self.player.stamina = 0
        elif self.shift_pressed and self.left_pressed and self.player.stamina > 0:
            self.player.stamina -= self.player.stamina_using_speed * delta_time
            self.player.change_x = -SHIFT_SPEED
            self.player.running_left = True
            if self.player.stamina < 0:
                self.player.stamina = 0
        elif self.shift_pressed and self.right_pressed:
            self.player.change_x = PLAYER_SPEED
        elif self.shift_pressed and self.left_pressed:
            self.player.change_x = -PLAYER_SPEED
        #dash
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
        self.enemy_list.update()
        self.player_list.update()
        self.wall_of_death.update(delta_time)
        dead_player = arcade.check_for_collision(self.wall_of_death, self.player)
        #chacking for alive and here game will stop
        if dead_player:
            self.player.live = False
            self.end_game()
        c_bugs = arcade.check_for_collision_with_list(self.player, self.bugs)
        for bug in c_bugs:
            bug.remove_from_sprite_lists()
            self.bug_count += 1
        if arcade.check_for_collision(self.player, self.wall_of_death):
            self.end_game()
        if len(arcade.check_for_collision_with_list(self.player, self.traps)) != 0:
            self.end_game()
        if len(arcade.check_for_collision_with_list(self.player, self.end)) != 0:
            self.scores_and_results()
            self.write_data_in_database()
            self.next_level()

    def update_timer(self, delta_time):
        self.timer_running += 1
        if self.player.stamina < 3.0:
            self.player.stamina += self.player.stamina_refresh_speed
            if self.player.stamina > 3.0:
                self.player.stamina = 3.0

    def next_level(self):
        self.n += 1
        if self.n > MAX_LEVEL:
            self.win_game()
        else:
            self.tilemap = arcade.load_tilemap(f"resources/tile/tilemaps/tilemap{self.n}.tmx", scaling=TILE_SCALE)
            self.walls = self.tilemap.sprite_lists["wall"]
            self.collisions = self.tilemap.sprite_lists["collision"]
            self.traps = self.tilemap.sprite_lists["trap"]
            self.bugs = self.tilemap.sprite_lists["bug"]
            self.end = self.tilemap.sprite_lists["end"]
            self.pp_eng = arcade.PhysicsEnginePlatformer(player_sprite=self.player,
                                                         platforms=self.collisions,
                                                         gravity_constant=GRAVITY)
            self.player.center_x = 100
            self.player.center_y = 100

    def scores_and_results(self):
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.BACKSPACE:
            self.next_level()
        if key == arcade.key.ESCAPE:
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
        if key == arcade.key.W:
            self.w_pressed = True
        if key == arcade.key.S:
            self.s_pressed = True

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
        if key == arcade.key.W:
            self.w_pressed = False
        if key == arcade.key.S:
            self.s_pressed = False

    def setup_players_database(self):
        pass

    def write_data_in_database(self):
        pass

    def end_game(self):
        arcade.close_window()

    def win_game(self):
        arcade.close_window()


def setup_game():
    win = Game()
    win.setup()
    arcade.run()


if __name__ == "__main__":
    setup_game()
