import arcade
from arcade import get_screens
from arcade.gui import UIManager, UIFlatButton, UITextureButton, UILabel
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout


TITLE = "Выберите экран для запуска"
SCREEN_HEIGHT = 200
SCREEN_WIDTH = 400


class Dialog(arcade.Window):
    def get_sc(self):
        screens = arcade.get_screens()
        print(screens)


    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, title=TITLE, fullscreen=False)
        arcade.set_background_color(arcade.color.WHITE)
        self.manager = UIManager()
        self.manager.enable()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)
        self.setup_widgets()
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)
        self.get_sc()




    def setup_widgets(self):
        pass

