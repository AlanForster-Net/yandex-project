import arcade
from arcade.gui import UIManager, UIFlatButton, UITextureButton, UILabel
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout

START_LEVEL = 5

class GameGUI(arcade.View):
    def __init__(self, game, cleaner, endgame, window):
        super().__init__()
        self.Game = game
        self.window = window
        self.cleaner = cleaner
        self.endgame = endgame
        arcade.set_background_color(arcade.color.GRAY)
        self.manager = UIManager()
        self.manager.enable()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)
        self.setup_widgets()
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)
        self.window.set_fullscreen(True)

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

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_close(self):
        self.manager.disable()

    def press_blue(self, junk):
        view = self.Game(self.cleaner, GameGUI, self.endgame, self.window, START_LEVEL)
        view.setup()
        self.window.show_view(view)

    def clear_file_and_close_event(self):
        self.cleaner()
        arcade.close_window()

