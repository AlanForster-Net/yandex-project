import arcade
from arcade.gui import UIManager, UIDropdown, UIFlatButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout
from handlers.json_handler import writer


JSONPATH = 'data/cfg.json'
TITLE = "Выберите экран для запуска"
SCREEN_HEIGHT = 200
SCREEN_WIDTH = 400


def run_dialog():
    _ = Dialog()
    arcade.run()


def get_sc():
    ans = []
    for x in enumerate(arcade.get_screens()):
        ans.append(str(x[0] + 1) + ". " + x[1].get_monitor_name() + ' ' + str(x[1].width) + 'x' + str(x[1].height))
    return ans


class Dialog(arcade.Window):
    CHOSEN = None

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, title=TITLE, fullscreen=False)
        self.flat_button = None
        arcade.set_background_color(arcade.color.WHITE)
        self.manager = UIManager()
        self.manager.enable()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)
        self.setup_widgets()
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def update_chosen(self, value):
        self.CHOSEN = int(value.new_value.split('.')[0]) - 1
        self.flat_button.on_click = lambda event: writer(JSONPATH, arcade.get_screens()[self.CHOSEN], self.CHOSEN)
        self.flat_button.on_click = lambda event: arcade.close_window()

    def setup_widgets(self):
        screens = get_sc()
        dropdown = UIDropdown(options=screens, width=200, color=arcade.color.BLACK)
        dropdown.on_change = lambda value: self.update_chosen(value)
        self.box_layout.add(dropdown)
        self.flat_button = UIFlatButton(text="Выбрать экран", width=200, height=50, color=arcade.color.BLACK)
        self.box_layout.add(self.flat_button)

    def on_draw(self):
        self.clear()
        self.manager.draw()

