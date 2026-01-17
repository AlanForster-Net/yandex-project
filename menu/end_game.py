import arcade
from arcade.gui import UIManager, UIFlatButton, UILabel
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout


class EndGame(arcade.View):
    def __init__(self, level_num, gamegui, game, cleaner, window):
        super().__init__()
        arcade.set_background_color((56, 56, 56))
        self.game = game
        self.cleaner = cleaner
        self.gamegui = gamegui
        self.window = window
        self.manager = UIManager()
        self.manager.enable()
        self.level_num = level_num
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        if level_num < 1:
            self.setup_fail_widgets()
        else:
            self.setup_success_widgets()
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_fail_widgets(self):
        end_title = UILabel('    Game over!\nИгра окончена!', multiline=True, font_size=24,
                            text_color=arcade.color.RED)
        retry_btn = UIFlatButton(text='Еще раз', width=250, height=50, color=arcade.color.BLACK)
        exit_btn = UIFlatButton(text='Сохранить прогресс и выйти', width=250, height=50, color=arcade.color.BLACK)
        exit_btn.on_click = lambda a: self.open_menu()
        self.window.set_caption('Run from antivirus! — Конец игры')
        self.box_layout.add(end_title)
        self.box_layout.add(retry_btn)
        self.box_layout.add(exit_btn)

    def setup_success_widgets(self):
        end_title = UILabel(f'Уровень {self.level_num} пройден!\n      Поздравляем!',
                            multiline=True, font_size=24,
                            text_color=arcade.color.GREEN)
        next_btn = UIFlatButton(text='Следующий уровень', width=250, height=50, color=arcade.color.BLACK)
        exit_btn = UIFlatButton(text='Сохранить прогресс и выйти', width=250, height=50, color=arcade.color.BLACK)
        exit_btn.on_click = lambda a: self.open_menu()
        next_btn.on_click = lambda a: self.next_lvl()
        self.window.set_caption('Run from antivirus! — Уровень пройден!')
        self.box_layout.add(end_title)
        self.box_layout.add(next_btn)
        self.box_layout.add(exit_btn)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_close(self):
        self.manager.disable()

    def open_menu(self):
        view = self.gamegui(self.game, self.cleaner, EndGame, self.window)
        self.window.show_view(view)

    def next_lvl(self):
        view = self.game(self.cleaner, self.gamegui, EndGame, self.window, self.level_num + 1)
        view.setup()
        self.window.show_view(view)



