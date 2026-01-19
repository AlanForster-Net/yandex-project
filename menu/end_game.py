import arcade
from arcade.gui import UIManager, UIFlatButton, UILabel
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout


class EndGame(arcade.View):
    def __init__(self, level_num, gamegui, game, cleaner, window, max_level, icon, failed, bd_handler):
        super().__init__()
        arcade.set_background_color((56, 56, 56))
        self.game = game
        self.cleaner = cleaner
        self.max_level = max_level
        self.gamegui = gamegui
        self.window = window
        self.manager = UIManager()
        self.manager.enable()
        self.level_num = level_num
        self.bd_handler = bd_handler
        self.icon = icon
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.btn_style = {
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
        if failed:
            self.setup_fail_widgets()
        else:
            self.setup_success_widgets()
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_fail_widgets(self):
        end_title = UILabel('    Game over!\nИгра окончена!', multiline=True,
                            text_color=arcade.color.RED, font_size=50)
        retry_btn = UIFlatButton(text='Еще раз', width=500, height=50, style=self.btn_style)
        exit_btn = UIFlatButton(text='Сохранить прогресс и выйти', width=500, height=50, style=self.btn_style)
        exit_btn.on_click = lambda a: self.open_menu()
        retry_btn.on_click = lambda a: self.retry()
        self.window.set_caption('Run from antivirus! — Конец игры')
        self.box_layout.add(end_title)
        self.box_layout.add(retry_btn)
        self.box_layout.add(exit_btn)

    def setup_success_widgets(self):
        if self.level_num < self.max_level:
            end_title = UILabel(f'Уровень {self.level_num} пройден!\n      Поздравляем!',
                                multiline=True, font_size=50,
                                text_color=arcade.color.GREEN)
            next_btn = UIFlatButton(text='Следующий уровень', width=500, height=50, style=self.btn_style)
            next_btn.on_click = lambda a: self.next_lvl()
            self.bd_handler.add_stats(searching='cur_lvl', modifier=self.level_num + 1, mod='new_val')
            self.box_layout.add(end_title)
            self.box_layout.add(next_btn)
        else:
            end_title = UILabel(f'Вы прошли игру!\n   Поздравляем!',
                                multiline=True, font_size=50,
                                text_color=arcade.color.GREEN)
            self.box_layout.add(end_title)
        exit_btn = UIFlatButton(text='Сохранить прогресс и выйти', width=500, height=50, style=self.btn_style)
        exit_btn.on_click = lambda a: self.open_menu()
        self.window.set_caption('Run from antivirus! — Уровень пройден!')
        self.box_layout.add(exit_btn)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_close(self):
        self.manager.disable()

    def open_menu(self):
        view = self.gamegui(self.game, self.cleaner, EndGame, self.window, self.icon, self.bd_handler)
        self.window.show_view(view)

    def next_lvl(self):
        view = self.game(self.cleaner, self.gamegui, EndGame, self.window, self.icon,
                         self.bd_handler, self.level_num + 1)
        view.setup()
        self.window.show_view(view)

    def retry(self):
        view = self.game(self.cleaner, self.gamegui, EndGame, self.window, self.icon, self.bd_handler, self.level_num)
        view.setup()
        self.window.show_view(view)



