from flet import (AlertDialog, Column, Container, ElevatedButton,
                  NavigationRail, NavigationRailDestination, Row, Text,
                  UserControl, alignment, border_radius, icons, margin,
                  padding)

from colors import BLACK_MEDIUM, CYAN_PRIMARY


class Sidebar(UserControl):

    def __init__(self, app_layout, page, app):
        super().__init__()
        self.app_layout = app_layout
        self.page = page
        self.app = app
        self.top_nav_items = [
            NavigationRailDestination(
                label_content=Text("Configurações"),
                label="Configurações",
                icon=icons.SETTINGS_SUGGEST_OUTLINED,
                selected_icon=icons.SETTINGS_SUGGEST_OUTLINED
            ),
            NavigationRailDestination(
                label_content=Text("Game"),
                label="Game",
                icon=icons.CASINO_OUTLINED,
                selected_icon=icons.CASINO_OUTLINED,
            ),
            NavigationRailDestination(
                label_content=Text("Estatisticas"),
                label="Estatisticas",
                icon=icons.BAR_CHART_OUTLINED,
                selected_icon=icons.BAR_CHART_OUTLINED,
            ),

        ]
        self.top_nav_rail = NavigationRail(
            selected_index=None,
            label_type="all",
            on_change=self.top_nav_change,
            destinations=self.top_nav_items,
            bgcolor=BLACK_MEDIUM,
            extended=True,
            height=500
            # expand=True
        )

    def build(self):
        self.view = Container(
            content=Column(
                [
                    Row(
                        [
                            Text("Hack Options"),
                        ],
                        alignment="center"
                    ),
                    # divider
                    Container(
                        bgcolor=CYAN_PRIMARY,
                        border_radius=border_radius.all(30),
                        height=1,
                        alignment=alignment.center_right,
                        width=220
                    ),
                    self.top_nav_rail,
                    # divider
                    Container(
                        bgcolor=CYAN_PRIMARY,
                        border_radius=border_radius.all(30),
                        height=1,
                        alignment=alignment.center_right,
                        width=220
                    ),
                ],
                tight=True
            ),
            padding=padding.all(15),
            margin=margin.only(0, 0, 0, 5),
            width=250,
            height=self.page.window_height,
            bgcolor=BLACK_MEDIUM,
        )

        return self.view

    def top_nav_change(self, e):
        self.top_nav_rail.selected_index = e.control.selected_index

        def close_dlg(e):
            dialog_not_user.open = False
            self.page.update()
        dialog_not_user = AlertDialog(
            title=Text("Nenhum usuario conectado"),
            content=ElevatedButton(text="Ok", on_click=close_dlg),
            on_dismiss=lambda e: print("Modal dialog dismissed!")
        )
        if not self.app.user:
            self.page.dialog = dialog_not_user
            dialog_not_user.open = True
            self.page.update()
            return
        if self.top_nav_rail.selected_index == 0:
            self.app_layout.settings_view.table.visible = True
            self.app_layout.active_view_game.game_view.visible = False
            self.app_layout.active_view_charts.visible = False
            self.app_layout.settings_view.update()
            self.app_layout.update()
            self.page.update()
        if self.top_nav_rail.selected_index == 1:
            self.app_layout.active_view_game.game_view.visible = True
            self.app_layout.active_view_charts.visible = False
            self.app_layout.settings_view.table.visible = False
            self.app_layout.active_view_game.update()
            self.app_layout.settings_view.update()
            self.app_layout.update()
            self.page.update()
        if self.top_nav_rail.selected_index == 2:
            self.app_layout.active_view_game.game_view.visible = False
            self.app_layout.active_view_charts.visible = True
            self.app_layout.settings_view.table.visible = False
            self.app_layout.active_view_game.update()
            self.app_layout.settings_view.update()
            self.app_layout.update()
            self.page.update()
        self.app_layout.active_view_game.update()
        self.app_layout.settings_view.update()
        self.update()
        self.page.update()
