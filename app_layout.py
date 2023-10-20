from flet import (AlertDialog, Column, Dropdown, IconButton, MainAxisAlignment,
                  Page, Row, Text, TextField, colors, dropdown, icons)

from active_view_settings import SettingsView
from colors import BLACK_MEDIUM, CYAN_PRIMARY, GREEN_MEDIUM, RED_PRIMARY
from data_base import DataBaseOptions
from sidebar import Sidebar
from active_view_game import ActiveViewGame


class AppLayout(Row):
    def __init__(
        self,
        app,
        page: Page,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page
        self.data_config = DataBaseOptions()
        self.toggle_nav_rail_button = IconButton(
            icon=icons.ARROW_CIRCLE_LEFT,
            icon_color=colors.BLUE_GREY_400,
            selected=False,
            selected_icon=icons.ARROW_CIRCLE_RIGHT,
            on_click=self.toggle_nav_rail)

        self.sidebar = Sidebar(self, self.page, self.app)
        self.settings_view = SettingsView(self.app, self.page, self)
        self.active_view_game = ActiveViewGame(self.page, self, self.app)

        self.generic_text_field_bet = TextField(
            label="Valor",
            hint_text="ex: 0,00",
            focused_border_color=CYAN_PRIMARY
        )

        self.active_view_charts = Row(
            controls=[Text("Estatisticas")],
            visible=False
        )

        self.active_view = Column(
            controls=[
                # self.generic_text_field_bet,
                self.active_view_game,
                self.active_view_charts,
                self.settings_view.table,
                # self.active_view_config,
            ],
            alignment="center",
            horizontal_alignment="center"
        )

        self.controls = [
            self.sidebar, self.toggle_nav_rail_button, self.active_view,
        ]

    def toggle_nav_rail(self, e):
        self.sidebar.visible = not self.sidebar.visible
        self.toggle_nav_rail_button.selected = not (
            self.toggle_nav_rail_button.selected
        )
        self.update()
        self.page.update()

    def edit_values_config(self, e):

        def destroy_dlg(e):
            edite_dialog.open = False
            self.update()
            self.page.update()

        def close_dlg(e):

            if valor.value == "" and not dropdown_itens.value:
                dropdown_itens.error_text = "⚠️Selecione um item!"
                valor.error_text = "⚠️Campo Obrigatorio!"
                self.update()
                self.page.update()
                return
            if valor.value == "":
                valor.error_text = "⚠️Campo Obrigatorio!"
                self.update()
                self.page.update()
                return

            if not dropdown_itens.value:
                dropdown_itens.error_text = "⚠️Selecione um item!"
                self.update()
                self.page.update()
                return

            list_display_config = [
                self.settings_view.config_color,
                self.settings_view.config_interval,
                self.settings_view.config_betg0,
                self.settings_view.config_betg1,
                self.settings_view.config_betg2,
                self.settings_view.config_betg3,
                self.settings_view.config_bcobetg0,
                self.settings_view.config_bcobetg1,
                self.settings_view.config_bcobetg2,
                self.settings_view.config_bcobetg3
            ]

            list_itens = [
                "Cor", "Intervalo", "Cor sem gale", "Cor gale 1",
                "Cor gale 2", "Cor gale 3", "Branco sem gale",
                "Branco gale 1", "Branco gale 2", "Branco gale 3",
                "Tamanho da lista", "Qtd Gales"
            ]
            list_columns = [
                "color", "interval", "betcolorg0", "betcolorg1", "betcolorg2",
                "betcolorg3", "betwhiteg0", "betwhiteg1", "betwhiteg2",
                "betwhiteg3", "qtdminutos", "qtdgales"
            ]

            for index, option in enumerate(list_itens):
                if option == dropdown_itens.value:
                    column = list_columns[index]
                    if option in (""):
                        try:
                            int(valor.value)
                        except ValueError:
                            valor.error_text = "⚠️ Valor invalido!"
                            self.update()
                            self.page.update()
                            return
                        self.data_config.update_from(
                            f"{column}={valor.value}"
                        )
                        list_display_config[index].value = valor.value
                    else:
                        self.data_config.update_from(
                            f"{column}='{valor.value}'"
                        )
                        list_display_config[index].value = valor.value

            parametro.error_text = ""
            valor.error_text = ""
            edite_dialog.open = False
            self.update()
            self.page.update()
            return

        parametro = TextField(
            label="Parâmetro",
            border_color=CYAN_PRIMARY,
            hint_text="Nome do parametro"
        )
        valor = TextField(
            label="Valor",
            border_color=CYAN_PRIMARY,
            hint_text="Valor"
        )
        dropdown_itens = Dropdown(
            options=[
                dropdown.Option("Cor"),
                dropdown.Option("Intervalo"),
                dropdown.Option("Tamanho da lista"),
                dropdown.Option("Qtd Gales"),
                dropdown.Option("Cor sem gale"),
                dropdown.Option("Cor gale 1"),
                dropdown.Option("Cor gale 2"),
                dropdown.Option("Cor gale 3"),
                dropdown.Option("Branco sem gale"),
                dropdown.Option("Branco gale 1"),
                dropdown.Option("Branco gale 2"),
                dropdown.Option("Branco gale 3"),
            ]
        )
        edite_dialog = AlertDialog(
            content=Column(
                [
                    dropdown_itens,
                    valor,
                    Row(
                        [
                            IconButton(
                                icon=icons.CHECK,
                                icon_color=BLACK_MEDIUM,
                                bgcolor=GREEN_MEDIUM,
                                on_click=close_dlg
                            ),
                            IconButton(
                                icon=icons.CLOSE,
                                icon_color=BLACK_MEDIUM,
                                bgcolor=RED_PRIMARY,
                                on_click=destroy_dlg
                            )
                        ],
                        alignment=MainAxisAlignment.SPACE_AROUND
                    ),

                ],
                tight=True,
            ),
            title=Text("Editar Configurações"),
        )
        self.page.dialog = edite_dialog
        edite_dialog.open = True
        self.page.update()
