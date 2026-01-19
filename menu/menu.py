import arcade
from arcade.gui import UIManager, UIFlatButton, UIImage, UILabel
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout

class GameGUI(arcade.View):
    def __init__(self, game, cleaner, endgame, window, icon, bd_handler):
        super().__init__()
        self.Game = game
        self.window = window
        self.cleaner = cleaner
        self.endgame = endgame
        self.bd_handler = bd_handler
        self.icon = icon
        self.start_level = bd_handler.get_stats('cur_lvl')
        arcade.set_background_color((56, 56, 56))
        self.manager = UIManager()
        self.manager.enable()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)
        self.setup_widgets()
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)
        self.window.set_fullscreen(True)

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
        game_name = UILabel(text="Run from antivirus!",
                        font_size=50,
                        text_color=(237, 0, 108),
                        width=300,
                        align="center")
        logo = arcade.texture.load_texture(self.icon)
        logo = UIImage(texture=logo, width=200, height=200, alpha=255)
        name_layout = UIBoxLayout(vertical=False, space_between=20)
        start_game_btn = UIFlatButton(text="Начать игру", width=500, height=50, style=btn_style)
        start_game_btn.on_click = self.start_game
        stat_btn = UIFlatButton(text="Статистика", width=500, height=50, style=btn_style)
        stat_btn.on_click = lambda a: self.open_stat_win()
        exit_with_open = UIFlatButton(text="Выйти из игры (с выбором монитора)", width=500, height=50, style=btn_style)
        exit_with_open.on_click = lambda a: self.clear_file_and_close_event()
        exit_btn = UIFlatButton(text="Выйти из игры", width=500, height=50, style=btn_style)
        exit_btn.on_click = lambda a: arcade.close_window()
        name_layout.add(logo)
        name_layout.add(game_name)
        self.box_layout.add(name_layout)
        self.box_layout.add(start_game_btn)
        self.box_layout.add(stat_btn)
        self.box_layout.add(exit_with_open)
        self.box_layout.add(exit_btn)


    def on_draw(self):
        self.clear()
        self.manager.draw()
        pass

    def on_close(self):
        self.manager.disable()

    def start_game(self, junk):
        view = self.Game(self.cleaner, GameGUI, self.endgame, self.window, self.icon, self.bd_handler, self.start_level)
        view.setup()
        self.window.show_view(view)

    def open_stat_win(self):
        pass

    def clear_file_and_close_event(self):
        self.cleaner()
        arcade.close_window()

