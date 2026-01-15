import arcade
from arcade.gui import UIManager, UIFlatButton, UITextureButton, UILabel
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout
from game.game import Game
from screeninfo import get_monitors


TITLE = "Run from antivirus! — Idle"
MONITOR = get_monitors()[0]
SCREEN_HEIGHT = MONITOR.height
SCREEN_WIDTH = MONITOR.width


class gameGUI(arcade.Window):
    def __init__(self):
        super().__init__(1000, 1000, title=TITLE, fullscreen=False)
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
        flat_button.on_click = self.pressBlue
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

    def on_draw(self):
        self.clear()
        self.manager.draw()
        pass

    def pressBlue(self, junk):
        win = Game('1')
        win.setup()
        arcade.run()

    def on_mouse_press(self, x, y, button, modifiers):
        pass