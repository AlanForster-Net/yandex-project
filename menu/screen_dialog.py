import arcade
from arcade.gui import UIManager, UIDropdown, UIFlatButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout


def get_sc():
    ans = []
    for x in enumerate(arcade.get_screens()):
        ans.append(str(x[0] + 1) + ". " + x[1].get_monitor_name() + ' ' + str(x[1].width) + 'x' + str(x[1].height))
    return ans


def run_dialog(writer, icon):
    window = arcade.Window(width=400, height=200, fullscreen=False)
    window.set_caption("Выберите экран для запуска")
    window.set_icon(icon)
    view = Dialog(writer, window)
    window.show_view(view)
    arcade.run()


class Dialog(arcade.View):
    def __init__(self, writer, window):
        super().__init__()
        self.dropdown = None
        self.flat_button = None
        self.writer = writer
        self.window = window
        arcade.set_background_color((56, 56, 56))
        self.manager = UIManager()
        self.manager.enable()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)
        self.setup_widgets()
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)
        self.setup_clicks()

    def button_handler(self):
        current = int(self.dropdown.value.split(".")[0]) - 1
        self.writer(arcade.get_screens()[current], current)
        self.manager.disable()
        self.window.close()

    def setup_widgets(self):
        btn_style = {
            "normal": UIFlatButton.UIStyle(
                font_size=18,
                bg=(213, 0, 97, 255)
            ),
            "hover": UIFlatButton.UIStyle(
                font_size=18,
                bg=(192, 0, 87, 255)
            ),
            "press": UIFlatButton.UIStyle(
                font_size=18,
                bg=(172, 0, 63, 255)
            )
        }


        screens = get_sc()
        self.dropdown = UIDropdown(options=screens, width=200, color=arcade.color.BLACK, default=screens[0])
        self.box_layout.add(self.dropdown)
        self.flat_button = UIFlatButton(text="Выбрать экран", width=200, height=50, style=btn_style)
        self.box_layout.add(self.flat_button)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def setup_clicks(self):
        self.flat_button.on_click = lambda a: self.button_handler()