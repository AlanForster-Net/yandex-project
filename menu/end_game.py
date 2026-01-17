import arcade
from arcade.gui import UIManager, UIFlatButton, UILabel
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout


TITLE = 'Run from antivirus! — Game over'


def run_end_screen(level, get_screen_data, gamegui, game, cleaner):
    _ = EndGame(level, get_screen_data, gamegui, game, cleaner)
    arcade.run()


class EndGame(arcade.Window):
    def __init__(self, level_num, get_screen_data, gamegui, game, cleaner):
        self.get_screen_data = get_screen_data
        screen = arcade.get_screens()[self.get_screen_data('screenNum')]
        super().__init__(self.get_screen_data("screenWidth"), self.get_screen_data("screenHeight"), title=TITLE,
                         fullscreen=True, screen=screen, center_window=False)
        arcade.set_background_color((56, 56, 56))
        self.game = game
        self.cleaner = cleaner
        self.gamegui = gamegui
        self.manager = UIManager()
        self.manager.enable()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        if level_num < 1:
            self.setup_fail_widgets()
        else:
            self.setup_success_widgets(level_num)
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_fail_widgets(self):
        end_title = UILabel('    Game over!\nИгра окончена!', multiline=True, font_size=24,
                            text_color=arcade.color.DARK_RED)
        retry_btn = UIFlatButton(text='Еще раз', width=200, height=50, color=arcade.color.BLACK)
        exit_btn = UIFlatButton(text='В меню', width=200, height=50, color=arcade.color.BLACK)
        exit_btn.on_click = lambda a: self.open_menu()
        self.box_layout.add(end_title)
        self.box_layout.add(retry_btn)
        self.box_layout.add(exit_btn)

    def setup_success_widgets(self, level_num):
        end_title = UILabel(f'Уровень {level_num} пройден!\n      Поздравляем!',
                            multiline=True, font_size=24,
                            text_color=arcade.color.DARK_GREEN)
        next_btn = UIFlatButton(text='Следующий уровень', width=200, height=50, color=arcade.color.BLACK)
        exit_btn = UIFlatButton(text='В меню', width=200, height=50, color=arcade.color.BLACK)
        exit_btn.on_click = lambda a: self.open_menu()
        self.box_layout.add(end_title)
        self.box_layout.add(next_btn)
        self.box_layout.add(exit_btn)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_close(self):
        self.manager.disable()

    def open_menu(self):
        arcade.close_window()
        _ = self.gamegui(self.game, self.cleaner, self.get_screen_data, run_end_screen)
        arcade.run()

