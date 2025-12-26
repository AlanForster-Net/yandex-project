
import arcade
from arcade.gui import UIManager, UIFlatButton, UITextureButton, UILabel, UIInputText, UITextArea, UISlider, UIDropdown, \
    UIMessageBox  # Это разные виджеты
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout  # А это менеджеры компоновки, как в pyQT
from main import Game


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class gameGUI(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Супер GUI Пример!")
        arcade.set_background_color(arcade.color.GRAY)

        # UIManager — сердце GUI
        self.manager = UIManager()
        self.manager.enable()  # Включить, чтоб виджеты работали

        # Layout для организации — как полки в шкафу
        self.anchor_layout = UIAnchorLayout()  # Центрирует виджеты
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)  # Вертикальный стек

        # Добавим все виджеты в box, потом box в anchor
        self.setup_widgets()  # Функция ниже

        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)  # Всё в manager

    def setup_widgets(self):
        # Здесь добавим ВСЕ виджеты — по порядку!
        label = UILabel(text="Run from antivirus!",
                        font_size=20,
                        text_color=arcade.color.WHITE,
                        width=300,
                        align="center")
        self.box_layout.add(label)
        flat_button = UIFlatButton(text="Плоская Кнопка", width=200, height=50, color=arcade.color.BLUE)
        flat_button.on_click = self.pressBlue  # Не только лямбду, конечно
        texture_normal = arcade.load_texture("заглушка3.png")
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
        self.manager.draw()  # Рисуй GUI поверх всего
        pass

    def pressBlue(self, a):
        win = Game(1)
        win.setup()
        arcade.run()


    def on_mouse_press(self, x, y, button, modifiers):
        pass


def setup_gui():
    win = gameGUI()
    arcade.run()


if __name__ == "__main__":
    setup_gui()
