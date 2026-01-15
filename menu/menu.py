import arcade
from arcade.gui import UIManager, UIFlatButton, UITextureButton, UILabel
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout
from pyglet.event import EVENT_HANDLE_STATE

from game.game import Game
from handlers.screen_handler import check_screen, get_screen_data, JSONPATH
from handlers.json_handler import cleaner


TITLE = "Run from antivirus! — Idle"
SCREEN = arcade.get_screens()[get_screen_data("screenNum")]


class GameGUI(arcade.Window):
    def __init__(self):
        super().__init__(get_screen_data("screenWidth"), get_screen_data("screenHeight"), title=TITLE,
                         fullscreen=False, screen=SCREEN, center_window=False)
        self.set_location(0, 108)
        self.set_fullscreen()
        arcade.set_background_color(arcade.color.GRAY)
        self.manager = UIManager()
        self.manager.enable()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)
        self.setup_widgets()
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        label = UILabel(text="Run from antivirus!",
                        font_size=20,
                        text_color=arcade.color.WHITE,
                        width=300,
                        align="center")
        self.box_layout.add(label)
        flat_button = UIFlatButton(text="Плоская Кнопка", width=200, height=50, color=arcade.color.BLUE)
        flat_button.on_click = self.press_blue
        texture_normal = arcade.load_texture("resources/img/заглушка3.png")
        texture_button = UITextureButton(texture=texture_normal,
                                         texture_hovered=texture_normal,
                                         texture_pressed=texture_normal,
                                         scale=0.05)
        self.box_layout.add(texture_button)
        texture_normal1 = arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png")
        texture_hovered1 = arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png")
        texture_pressed1= arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png")
        texture_button1 = UITextureButton(texture=texture_normal1,
                                         texture_hovered=texture_hovered1,
                                         texture_pressed=texture_pressed1,
                                         scale=1.0)
        self.box_layout.add(texture_button1)
        self.box_layout.add(flat_button)
        exit_with_open = UIFlatButton(text="Выйти из игры (с выбором монитора)",
                                   width=325, height=50, color=arcade.color.BLUE)
        exit_with_open.on_click = lambda a: self.clear_file_and_close_event()
        self.box_layout.add(exit_with_open)



    def on_draw(self):
        self.clear()
        self.manager.draw()
        pass

    def press_blue(self, junk):
        check_screen()
        win = Game('1')
        win.setup()
        arcade.run()
        arcade.close_window()

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()

    def clear_file_and_close_event(self):
        cleaner(JSONPATH)
        arcade.close_window()
