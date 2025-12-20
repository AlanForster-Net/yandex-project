import arcade
import sqlite3
from pyglet.graphics import Batch


GRAVITY = 1.0
MAX_LEVEL = 10


# Андрей
class Player(arcade.Sprite):
    pass

#? Андрей
class WallOfDeath(arcade.Sprite):
    pass


# Егор
class Level(arcade.Window):
    def __init__(self, n, title="game"):
        super().__init__(fullscreen=True, title=title)
        self.tilemap = arcade.load_tilemap(f"tilemaps/tilemap_{n}.tmx")
        self.n = n
        # self.init_scene(self.tilemap)

    def init_scene(self, tilemap):
        self.walls = self.tilemap.sprite_lists["wall"]
        self.collisions = self.tilemap.sprite_lists["collision"]
        self.traps = self.tilemap.sprite_lists["trap"]
        self.bugs = self.tilemap.sprite_lists["bug"]
        self.end = self.tilemap.sprite_lists["end"]
    
    def setup(self):
        self.bug_count = 0
        self.init_scene(self.tilemap)
        # Sprites
        self.player = Player()
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
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
        #? arcade.start_render()
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
    
    def on_key_press(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.LEFT):
            pass #? Андрей
        if key in (arcade.key.D, arcade.key.RIGHT):
            pass #? Андрей
        if key == arcade.key.SPACE:
            # Уточнить и доработать
            if self.pp_eng.can_jump():
                pass #? Андрей
    
    def on_key_release(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.LEFT, arcade.key.D, arcade.key.RIGHT):
            pass #? Андрей

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

    def write_data_in_database(self):
        pass
