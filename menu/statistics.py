#import dependencies
import arcade
from arcade.gui import UIManager, UIFlatButton, UILabel, UIImage
from arcade.gui.experimental import UIScrollArea
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout
from arcade.gui.experimental.scroll_area import UIScrollBar


#stats window class
class Statistics(arcade.View):
    def __init__(self, game, cleaner, endgame, window, icon, bd_handler, gamegui):
        super().__init__()
        self.manager = UIManager()
        self.manager.enable()
        self.anchor_layout = UIAnchorLayout()
        self.game = game
        self.cleaner = cleaner
        self.endgame = endgame
        self.window = window
        diagonal = (self.window.width ** 2 + self.window.width ** 2) ** 0.5
        base_diagonal = (2560 ** 2 + 1440 ** 2) ** 0.5
        self.scale = diagonal / base_diagonal
        self.icon = icon
        self.bd_handler = bd_handler
        self.gamegui = gamegui
        arcade.set_background_color((56, 56, 56))
        self.box_layout = UIBoxLayout(vertical=True, space_between=int(10 * self.scale))
        self.setup_widgets()
        self.manager.add(self.anchor_layout)
        self.window.set_caption('Run from antivirus! - Статистика')

    #setup gui elements
    def setup_widgets(self):
        content_left = UIAnchorLayout(size_hint=(0.5, 1))
        self.anchor_layout.add(content_left, anchor_x="left", anchor_y="center")
        content_left.add(self.box_layout)
        content_right = UIAnchorLayout(size_hint=(0.5, 1))
        self.anchor_layout.add(content_right, anchor_x="right", anchor_y="center")

        vertical_list = UIBoxLayout(size_hint=(1, 0), space_between=1)
        all_stats = self.bd_handler.get_all_stats('name, value')
        for i in range(len(all_stats)):
            stat = UILabel(text=all_stats[i][0].strip() + '—' + str(all_stats[i][1]),
                                font_size=int(40 * self.scale),
                                text_color=(237, 0, 108),
                                align="center")
            vertical_list.add(stat)
        v_scroll_area = UIBoxLayout(vertical=False, size_hint=(0.8, 0.8))
        content_right.add(v_scroll_area, anchor_x="center", anchor_y="center")
        scroll_layout = v_scroll_area.add(UIScrollArea(size_hint=(1, 1)))
        scroll_layout.with_border(color=arcade.uicolor.WHITE_CLOUDS)
        scroll_layout.add(vertical_list)
        v_scroll_area.add(UIScrollBar(scroll_layout))
        btn_style = {
            "normal": UIFlatButton.UIStyle(
                font_size=int(18 * self.scale),
                bg=(213, 0, 97, 255)
            ),
            "hover": UIFlatButton.UIStyle(
                font_size=int(18 * self.scale),
                bg=(192, 0, 87, 255)
            ),
            "press": UIFlatButton.UIStyle(
                font_size=int(18 * self.scale),
                bg=(172, 0, 63, 255)
            )
        }
        logo = arcade.texture.load_texture(self.icon)
        logo = UIImage(texture=logo, width=int(300 * self.scale), height=int(300 * self.scale), alpha=255)
        self.box_layout.add(logo)
        page_name = UILabel(text="Run from antivirus! - Статистика",
                            font_size=int(50 * self.scale),
                            text_color=(237, 0, 108),
                            width=int(300 * self.scale),
                            align="center")
        self.box_layout.add(page_name)
        to_menu_btn = UIFlatButton(text="Вернуться в меню", width=int(500 * self.scale), height=int(50 * self.scale), style=btn_style)
        to_menu_btn.on_click = lambda a: self.to_menu()
        self.box_layout.add(to_menu_btn)

    #draw all gui
    def on_draw(self):
        self.clear()
        self.manager.draw()

    #return to menu button handler
    def to_menu(self):
        view = self.gamegui(self.game, self.cleaner, self.endgame, self.window, self.icon,
                               self.bd_handler, Statistics)
        self.window.show_view(view)

    #close manager to avoid error
    def on_close(self):
        self.manager.disable()