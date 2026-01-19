import arcade
from arcade.gui import UIManager, UIFlatButton, UILabel, UIImage
from arcade.gui.experimental import UIScrollArea
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout
from arcade.gui.experimental.scroll_area import UIScrollBar


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
        self.icon = icon
        self.bd_handler = bd_handler
        self.gamegui = gamegui
        arcade.set_background_color((56, 56, 56))
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.setup_widgets()
        self.manager.add(self.anchor_layout)
        self.window.set_caption('Run from antivirus! - Статистика')

    def setup_widgets(self):
        content_left = UIAnchorLayout(size_hint=(0.5, 1))
        self.anchor_layout.add(content_left, anchor_x="left", anchor_y="center")
        content_left.add(self.box_layout)
        content_right = UIAnchorLayout(size_hint=(0.5, 1))
        self.anchor_layout.add(content_right, anchor_x="right", anchor_y="center")

        vertical_list = UIBoxLayout(size_hint=(1, 0), space_between=1)
        all_stats = self.bd_handler.get_all_stats('name, value')
        for i in range(len(all_stats)):
            inner_box = UIBoxLayout(vertical=False, space_between=10)
            stat_name = UILabel(text=all_stats[i][0].strip() + '—',
                                font_size=45,
                                text_color=(237, 0, 108),
                                width=300,
                                align="left")
            stat_val = UILabel(text=str(all_stats[i][1]),
                                font_size=45,
                                text_color=(237, 0, 108),
                                width=300,
                                align="left")
            inner_box.add(stat_name)
            inner_box.add(stat_val)
            vertical_list.add(inner_box)
        v_scroll_area = UIBoxLayout(vertical=False, size_hint=(0.8, 0.8))
        content_right.add(v_scroll_area, anchor_x="center", anchor_y="center")
        scroll_layout = v_scroll_area.add(UIScrollArea(size_hint=(1, 1)))
        scroll_layout.with_border(color=arcade.uicolor.WHITE_CLOUDS)
        scroll_layout.add(vertical_list)
        v_scroll_area.add(UIScrollBar(scroll_layout))


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
        logo = arcade.texture.load_texture(self.icon)
        logo = UIImage(texture=logo, width=300, height=300, alpha=255)
        self.box_layout.add(logo)
        page_name = UILabel(text="Run from antivirus! - Статистика",
                            font_size=50,
                            text_color=(237, 0, 108),
                            width=300,
                            align="center")
        self.box_layout.add(page_name)
        to_menu_btn = UIFlatButton(text="Вернуться в меню", width=500, height=50, style=btn_style)
        to_menu_btn.on_click = lambda a: self.to_menu()
        self.box_layout.add(to_menu_btn)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def to_menu(self):
        view = self.gamegui(self.game, self.cleaner, self.endgame, self.window, self.icon,
                               self.bd_handler, Statistics)
        self.window.show_view(view)

    def on_close(self):
        self.manager.disable()