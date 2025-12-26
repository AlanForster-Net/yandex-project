import arcade
from arcade import get_screens
from arcade.gui import UIManager, UIFlatButton, UITextureButton, UILabel
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout


TITLE = "Выберите экран для запуска"


class Dialog(arcade.View):
    def __init__(self):
        super().__init__(400, 200, title=TITLE, fullscreen=False)
        arcade.set_background_color(arcade.color.WHITE)
        self.manager = UIManager()
        self.manager.enable()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)
        self.setup_widgets()
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def get_monitors_list(self):
        monitors = get_screens()


    def setup_widgets(self):
        pass
