import random
import arcade
from arcade.particles import FadeParticle, Emitter, EmitBurst

from arcade.examples.camera_platform import JUMP_SPEED
from pyglet.graphics import Batch

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
ENEMY_SPEED = 0.75
# Physic const
GRAVITY = 0.8
MAX_LEVEL = 5
TILE_SCALE = 2.5

# textures for blood
BLOOD_TEX = [
    arcade.make_soft_circle_texture(20, arcade.color.DARK_RED),
    arcade.make_soft_circle_texture(15, arcade.color.DARK_CANDY_APPLE_RED),
    arcade.make_soft_circle_texture(16, arcade.color.BURGUNDY),
]

GREEN_TEX = [
    arcade.make_soft_circle_texture(20, arcade.color.GREEN),
    arcade.make_soft_circle_texture(15, arcade.color.ANDROID_GREEN),
    arcade.make_soft_circle_texture(16, arcade.color.APPLE_GREEN),
]


# mutator for blood
def blood_spray_mutator(p):
    p.change_y -= 0.58

    p.change_x *= 0.96
    p.change_y *= 0.96

    p.alpha = max(0, p.alpha - 3)


# fabric of blood
def make_blood_spray(x, y, count=500, color=BLOOD_TEX):
    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitBurst(count),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=random.choice(color),
            change_xy=(
                random.uniform(-5.0, 5.0),
                random.uniform(2.5, 7.0),
            ),
            lifetime=random.uniform(0.8, 1.6),
            start_alpha=255,
            end_alpha=0,
            scale=random.uniform(0.35, 0.6),
            mutation_callback=blood_spray_mutator,
        ),
    )


# classes
class Player(arcade.Sprite):
    def __init__(self, x, y, scale=2):
        super().__init__('resources/players_frames/pack1/idle.png', scale=scale)
        # some attributes
        self.live = True
        self.pack_of_skin = 1
        # posiotion of player
        self.center_x = x
        self.center_y = y
        self.change_x = 0
        self.change_y = 0
        # movement variables
        self.jumps_remaining = MAX_JUMPS
        self.max_jumps = MAX_JUMPS
        self.double_jump = False
        self.was_on_ground = False
        self.stamina = 3.0
        self.stamina_refresh_speed = STAMINA_REFRESH_SPEED
        self.stamina_using_speed = SPEED_OF_USING_STAMINA
        self.stamina_using_value = STAMINA_USING_VALUE
        # textures
        self.frames = dict()
        self.frames["running_right"] = list()
        self.frames["running_left"] = list()
        self.frames["running_jump"] = list()
        self.frames["die"] = None
        self.frames["idle"] = None
        self.frames["jump"] = None
        # base skin
        self.frames["die"] = arcade.load_texture("resources/players_frames/pack1/die.png")
        self.frames["idle"] = arcade.load_texture("resources/players_frames/pack1/idle.png")
        self.frames["jump"] = arcade.load_texture("resources/players_frames/pack1/jump.png")
        for i in range(1, 5):
            self.frames["running_right"].append(arcade.load_texture(f"resources/players_frames/pack1/run_r_{i}.png"))

        for i in range(1, 5):
            self.frames["running_left"].append(arcade.load_texture(f"resources/players_frames/pack1/run_l_{i}.png"))

        # animation
        self.current_frame = 0
        self.animation_speed = 0.0
        self.animation_timer = 0

    def update(self, delta_time=1 / 60):
        super().update()
        # easter with "капустка"
        if self.pack_of_skin == "easter_pack":
            self.texture = arcade.load_texture("resources/players_frames/easter_pack/капустка.jpg")
            return
        # checking for alive and change texture
        if not self.live:
            self.texture = self.frames["die"]
            return
        # animation
        self.animation_timer += delta_time
        if self.change_y != 0 and self.change_x == 0:
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

        elif abs(self.change_x) == 0 and self.change_y == 0:
            self.texture = self.frames["idle"]
            self.animation_timer = 0

    def update_skin(self, pack_of_skin):
        self.pack_of_skin = pack_of_skin
        # easter pack
        if self.pack_of_skin == "easter_pack":
            self.scale = 0.05
            self.center_y = 150
            return
        # texture from normal packs
        self.frames["die"] = arcade.load_texture(f"resources/players_frames/pack{pack_of_skin}/die.png")
        self.frames["idle"] = arcade.load_texture(f"resources/players_frames/pack{pack_of_skin}/idle.png")
        self.frames["jump"] = arcade.load_texture(f"resources/players_frames/pack{pack_of_skin}/jump.png")
        self.frames["running_right"].clear()
        self.frames["running_left"].clear()
        for i in range(1, 5):
            self.frames["running_right"].append(
                arcade.load_texture(f"resources/players_frames/pack{pack_of_skin}/run_r_{i}.png"))

        for i in range(1, 5):
            self.frames["running_left"].append(
                arcade.load_texture(f"resources/players_frames/pack{pack_of_skin}/run_l_{i}.png"))


class WallOfDeath(arcade.Sprite):
    def __init__(self, x, y, scale=1.95):
        super().__init__('resources/enemy_frames/death_wall(1).png', scale=scale)
        self.center_x = x
        self.center_y = y
        # textures for wall
        self.frames = [arcade.load_texture("resources/enemy_frames/death_wall(1).png"),
                       arcade.load_texture("resources/enemy_frames/death_wall(2).png"),
                       arcade.load_texture("resources/enemy_frames/death_wall(3).png")]
        # animation variables
        self.animation_speed = 0.8
        self.current_frame = 0
        self.animation_timer = 0
        # move variables
        self.change_x = ENEMY_SPEED
        self.height = self.height * 1.25
        self.width = self.width * 1.25

    def update(self, delta_time):
        super().update()
        self.animation_timer += delta_time
        # make animation
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % 3
            self.texture = self.frames[self.current_frame]


class Game(arcade.View):
    def __init__(self, cleaner, gamegui, endgame, window, icon, bd_handler, statistics, n=1):
        title = f"Run from antivirus! — Level {n}"
        super().__init__()
        self.emitters = list()
        # variables for view
        self.cleaner = cleaner
        self.gamegui = gamegui
        self.endgame = endgame
        self.window = window
        self.icon = icon
        self.bd_handler = bd_handler
        self.statistics = statistics
        # physic engine
        self.pp_eng = None
        arcade.set_background_color(arcade.color.PINK)
        self.player = None
        self.player_list = None
        # variables for levels
        self.level = n
        self.background_color = arcade.color.BLACK
        self.tilemap = arcade.load_tilemap(f"resources/tile/tilemaps/tilemap{self.level}.tmx", scaling=TILE_SCALE)
        self.walls = arcade.SpriteList()
        self.collisions = arcade.SpriteList()
        self.traps = arcade.SpriteList()
        self.bugs = arcade.SpriteList()
        self.end = arcade.SpriteList()
        self.walls = self.tilemap.sprite_lists["wall"]
        self.collisions = self.tilemap.sprite_lists["collision"]
        self.traps = self.tilemap.sprite_lists["trap"]
        self.bugs = self.tilemap.sprite_lists["bug"]
        self.ladders = self.tilemap.sprite_lists["ladder"]
        self.end = self.tilemap.sprite_lists["end"]
        # flag of controllers button
        self.left_pressed = False
        self.right_pressed = False
        self.space_pressed = False
        self.space_just_pressed = False
        self.shift_pressed = False
        self.dash_button = False
        self.w_pressed = False
        self.s_pressed = False
        # timer of game
        self.timer_running = 0
        self.window.set_caption(title)

    # function for changing levels
    def init_scene(self, tilemap):
        self.walls = self.tilemap.sprite_lists["wall"]
        self.collisions = self.tilemap.sprite_lists["collision"]
        self.traps = self.tilemap.sprite_lists["trap"]
        self.bugs = self.tilemap.sprite_lists["bug"]
        self.ladders = self.tilemap.sprite_lists["ladder"]
        self.end = self.tilemap.sprite_lists["end"]

    def setup(self):
        # initilizate of player
        self.player = Player(100, 100 // 2, 3)
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        self.bug_count = 0
        # initilizate wall
        self.wall_of_death = WallOfDeath(-700, 230)
        # positions for each levels
        if self.level == 5:
            self.wall_of_death.center_x = -1400
            self.wall_of_death.center_y = 400
            self.wall_of_death.change_x *= ENEMY_SPEED * 0.75
        elif self.level == 4:
            self.wall_of_death.change_x *= ENEMY_SPEED * 1
            self.wall_of_death.change_x *= ENEMY_SPEED * 1.75
            self.wall_of_death.center_x = -1100
            self.wall_of_death.center_y = 200
        elif self.level == 3:
            self.wall_of_death.change_x *= ENEMY_SPEED * 1.5
            self.wall_of_death.center_x = -1100
            self.wall_of_death.center_y = 200
        elif self.level == 2:
            self.wall_of_death.change_x *= ENEMY_SPEED * 1.25
            self.wall_of_death.center_x = -1100
            self.wall_of_death.center_y = 199
        else:
            self.wall_of_death.center_x = -1100
            self.wall_of_death.center_y = 200
        # lists for player and enemy
        self.enemy_list = arcade.SpriteList()
        self.enemy_list.append(self.wall_of_death)
        # camera
        self.player_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()
        self.pp_eng = arcade.PhysicsEnginePlatformer(player_sprite=self.player,
                                                     platforms=self.collisions,
                                                     ladders=self.ladders,
                                                     gravity_constant=GRAVITY)
        arcade.schedule(self.update_timer, 1.0)
        self.main_theme = arcade.load_sound("resources/sound/soundtrack.mp3")
        self.music_player = self.main_theme.play(volume=0.3, loop=True)

    def gui_draw(self):
        # Stamina bar
        scale = 0.000546875 * self.window.width # scale for different monitors
        left_shift = int(50 * scale)  # shift with scale
        panel_width = int(305 * scale)  # size of stamina bar
        panel_height = int(50 * scale)
        # stamina's bar positon
        panel_x = int(self.window.width - (275 * scale) - left_shift)
        panel_y = int(25 * scale)
        # drawing everything
        arcade.draw_lbwh_rectangle_filled(
            panel_x, panel_y, panel_width, panel_height, arcade.color.WHITE
        )
        # size of segments
        segment_width = int(95 * scale)
        segment_height = int(44 * scale)
        segment_y = int(panel_y + 3 * scale)
        # segment's shift
        segment_offset = 5 * scale
        # drawing segments
        if self.player.stamina >= 1:
            arcade.draw_lbwh_rectangle_filled(
                int(panel_x + segment_offset),
                segment_y,
                segment_width,
                segment_height,
                arcade.color.BLACK
            )
        if self.player.stamina >= 2:
            arcade.draw_lbwh_rectangle_filled(
                int(panel_x + segment_offset + segment_width + (5 * scale)),
                segment_y,
                segment_width,
                segment_height,
                arcade.color.BLACK
            )
        if self.player.stamina >= 3:
            arcade.draw_lbwh_rectangle_filled(
                int(panel_x + segment_offset + (segment_width * 2) + (10 * scale)),
                segment_y,
                segment_width,
                segment_height,
                arcade.color.BLACK
            )
        # timer
        self.batch = Batch()
        base_x = self.window.width
        base_y = self.window.height
        desired_offset = 20
        text_x = int(base_x + (desired_offset * scale) - left_shift)
        text_y = int(base_y - (desired_offset * scale))
        font = int(15 * scale)
        str_for_timer = f'{self.timer_running // 60}:{self.timer_running % 60}'
        text = arcade.Text(
            str_for_timer,
            text_x,
            text_y,
            arcade.color.WHITE,
            font,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch
        )
        #score bar
        bug_font_size = int(15 * scale)
        bug_counter_text = f"Bugs: {self.bug_count}"
        bug_text_x = int(self.window.width / 2)
        bug_text_y = int(self.window.height - (20 * scale))

        bug_text = arcade.Text(
            bug_counter_text,
            bug_text_x,
            bug_text_y,
            arcade.color.WHITE,
            bug_font_size,
            anchor_x="center",
            anchor_y="top",
            batch=self.batch
        )
        self.batch.draw()

    def on_draw(self):
        self.clear()
        self.player_camera.use()
        self.walls.draw()
        self.traps.draw()
        self.end.draw()
        self.bugs.draw()
        self.ladders.draw()
        for e in self.emitters:
            e.draw()
        self.player_list.draw()
        self.enemy_list.draw()
        self.gui_camera.use()
        self.gui_draw()

    def on_update(self, delta_time=1 / 60):
        base_speed = PLAYER_SPEED  # new variable for speed(walking)
        if self.shift_pressed and self.player.stamina > 0:
            base_speed = SHIFT_SPEED  # running
            self.player.stamina -= self.player.stamina_using_speed * delta_time
        # determine the direction of the vector
        if self.left_pressed and not self.right_pressed:
            self.player.change_x = -base_speed
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x = base_speed
        else:
            self.player.change_x = 0

        # climbing on ladder
        is_on_ladder = self.pp_eng.is_on_ladder()
        if is_on_ladder:
            # up/down on leader
            if self.w_pressed and not self.s_pressed:
                self.player.change_y = LADDER_SPEED
            elif self.s_pressed and not self.w_pressed:
                self.player.change_y = -LADDER_SPEED
            else:
                self.player.change_y = 0

        # jump
        is_on_ground = self.pp_eng.can_jump()
        if is_on_ground and self.player.live:
            if not self.player.was_on_ground:
                self.player.jumps_remaining = self.player.max_jumps
                self.player.was_on_ground = True
        else:
            self.player.was_on_ground = False
        # double jump
        if self.space_just_pressed and self.player.jumps_remaining > 0 and self.player.stamina >= 1:
            if is_on_ground:
                self.bd_handler.add_stats(searching='jumps')
            else:
                self.bd_handler.add_stats(searching='double')

            self.player.change_y = JUMP_SPEED
            self.player.jumps_remaining -= 1
            self.space_just_pressed = False

        if not self.space_pressed:
            self.space_just_pressed = False

        # dash
        if self.dash_button and self.right_pressed and self.player.stamina >= 1:
            self.player.stamina -= self.player.stamina_using_value
            self.player.change_x = 0
            self.player.center_x += DASH_GAP
            self.bd_handler.add_stats(searching='dash')
            self.dash_button = False
        elif self.dash_button and self.left_pressed and self.player.stamina >= 1:
            self.player.stamina -= self.player.stamina_using_value
            self.player.change_x = 0
            self.player.center_x -= DASH_GAP
            self.bd_handler.add_stats(searching='dash')
            self.dash_button = False



        # update camera's position
        pos = (self.player.center_x, self.player.center_y)
        self.player_camera.position = arcade.math.lerp_2d(self.player_camera.position,
                                                          pos,
                                                          0.14)
        # update emitters' position
        emitters_copy = self.emitters.copy()
        for e in emitters_copy:
            e.update(delta_time)

        for e in emitters_copy:
            if e.can_reap():
                self.emitters.remove(e)

        # Sprites update
        self.enemy_list.update()
        self.player_list.update()
        self.wall_of_death.update(delta_time)

        # Calculate collusion of player
        dead_player = arcade.check_for_collision(self.wall_of_death, self.player)
        if dead_player:
            self.player.live = False
            self.end_game()

        c_bugs = arcade.check_for_collision_with_list(self.player, self.bugs)
        c_bug_2 = arcade.check_for_collision_with_list(self.wall_of_death, self.bugs)

        # Count collected bugs
        for bug in c_bugs:
            bug.remove_from_sprite_lists()
            self.emitters.append(make_blood_spray(bug.center_x, bug.center_y, color=GREEN_TEX))
            self.bug_count += 1

        for bug in c_bug_2:
            bug.remove_from_sprite_lists()
            self.emitters.append(make_blood_spray(bug.center_x, bug.center_y))  # burst them!
        # collusion with wall
        if arcade.check_for_collision(self.player, self.wall_of_death):
            self.end_game()
        # fall into trap
        if len(arcade.check_for_collision_with_list(self.player, self.traps)) != 0:
            self.end_game()
        # reach the end
        if len(arcade.check_for_collision_with_list(self.player, self.end)) != 0:
            self.win_game()
        self.pp_eng.update()

    # timer of running
    def update_timer(self, delta_time):
        self.timer_running += 1
        if self.player.stamina < 3.0:
            self.player.stamina += self.player.stamina_refresh_speed
            if self.player.stamina > 3.0:
                self.player.stamina = 3.0

    def on_key_press(self, key, modifiers):
        # controllers buttons
        if key == arcade.key.ESCAPE:
            arcade.stop_sound(self.music_player)
            view = self.gamegui(Game, self.cleaner, self.endgame, self.window, self.icon, self.bd_handler,
                                self.statistics)
            self.window.show_view(view)
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
        if key == arcade.key.DELETE:
            self.end_game()

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

    def end_game(self):
        arcade.stop_sound(self.music_player)
        view = self.endgame(self.level, self.gamegui, Game, self.cleaner, self.window, MAX_LEVEL, self.icon, True,
                            self.bd_handler, self.timer_running, self.statistics)
        self.window.show_view(view)

    def win_game(self):
        arcade.stop_sound(self.music_player)
        view = self.endgame(self.level, self.gamegui, Game, self.cleaner, self.window, MAX_LEVEL, self.icon, False,
                            self.bd_handler, self.statistics, self.timer_running, self.bug_count)
        self.window.show_view(view)
