from flet import (DataCell, DataColumn, DataRow, DataTable, Icon, Page, Row,
                  Text, TextField, UserControl, border, icons)

from colors import BLACK_MEDIUM, CYAN_PRIMARY, GREEN_MEDIUM
from data_base import DataBaseOptions


class SettingsView(UserControl):
    def __init__(
            self,
            app,
            page: Page,
            app_layout,
            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.app = app
        self.app_layout = app_layout
        self.page = page

        self.db_config = DataBaseOptions()

        initial_config = self.db_config.select_from(False)

        self.icon_btn_edit = Icon(
            icons.EDIT_NOTE,
            size=20
        )

        self.config_color = Text(
            value=initial_config[0][1],
        )
        self.config_interval = Text(
            value=initial_config[0][2],
            semantics_label="interval",
        )

        self.config_number_hours = Text(
            value=initial_config[0][11]
        )

        self.config_number_gales = Text(
            value=initial_config[0][12]
        )

        self.config_betg0 = Text(
            value=initial_config[0][3],
            semantics_label="betg0",
        )
        self.config_betg1 = Text(
            value=initial_config[0][4],
            semantics_label="betg1"
        )
        self.config_betg2 = Text(
            value=initial_config[0][5],
            semantics_label="betg2"
        )
        self.config_betg3 = Text(
            value=initial_config[0][6],
            semantics_label="betg3"
        )
        self.config_bcobetg0 = Text(
            value=initial_config[0][7],
            semantics_label="bcobetg0"
        )
        self.config_bcobetg1 = Text(
            value=initial_config[0][8],
            semantics_label="bcobetg1"
        )
        self.config_bcobetg2 = Text(
            value=initial_config[0][9],
            semantics_label="bcobetg2"
        )
        self.config_bcobetg3 = Text(
            value=initial_config[0][10],
            semantics_label="bcobetg3"
        )

        self.generic_text_field_bet = TextField(
            label="Valor",
            hint_text="ex: 0,00",
            focused_border_color=CYAN_PRIMARY
        )

        self.table = DataTable(
                width=300,
                bgcolor=BLACK_MEDIUM,
                visible=False,
                border=border.all(2, CYAN_PRIMARY),
                border_radius=5,
                vertical_lines=border.BorderSide(1, CYAN_PRIMARY),
                horizontal_lines=border.BorderSide(1, CYAN_PRIMARY),
                sort_column_index=0,
                data_row_max_height=40,
                sort_ascending=True,
                heading_row_color=BLACK_MEDIUM,
                heading_row_height=35,
                # data_row_color={"hovered": "0x30FF0000"},
                # show_checkbox_column=True,
                divider_thickness=1,
                column_spacing=50,
                columns=[
                    DataColumn(
                        Text("Parâmetro", weight="bold"),
                        tooltip="Nome do parâmetro"
                    ),
                    DataColumn(
                        Text("Valor", weight="bold"),
                        tooltip="Valores dos parâmetros",
                    ),
                ],
                rows=[
                    DataRow(
                        cells=[
                            DataCell(content=Text("Cor")),
                            DataCell(
                                content=Row(
                                    [
                                        Text("    "),
                                        self.config_color
                                    ],
                                ),
                            )
                        ],
                        # selected=True,
                        on_select_changed=self.app_layout.edit_values_config
                    ),
                    DataRow(
                        cells=[
                            DataCell(content=Text("intervalo")),
                            DataCell(
                                content=Row(
                                    [
                                        Text("Min:"),
                                        self.config_interval
                                    ]
                                )
                            )
                        ],
                        on_select_changed=self.app_layout.edit_values_config
                    ),
                    DataRow(
                        cells=[
                            DataCell(content=Text("Tamanho da lista")),
                            DataCell(
                                content=Row(
                                    [
                                        Text("    "),
                                        self.config_number_hours
                                    ]
                                )
                            )
                        ],
                        on_select_changed=self.app_layout.edit_values_config
                    ),
                    DataRow(
                        cells=[
                            DataCell(content=Text("Qtd Gales")),
                            DataCell(
                                content=Row(
                                    [
                                        Text("    "),
                                        self.config_number_gales
                                    ]
                                )
                            )
                        ],
                        on_select_changed=self.app_layout.edit_values_config
                    ),
                    DataRow(
                        cells=[
                            DataCell(content=Text("Cor sem Gale")),
                            DataCell(
                                content=Row(
                                    [
                                        Text("R$", color=GREEN_MEDIUM),
                                        self.config_betg0
                                    ]
                                )
                            )
                        ],
                        on_select_changed=self.app_layout.edit_values_config
                    ),
                    DataRow(
                        cells=[
                            DataCell(content=Text("Cor Gale 1")),
                            DataCell(
                                content=Row(
                                    [
                                        Text("R$", color=GREEN_MEDIUM),
                                        self.config_betg1
                                    ]
                                )
                            )
                        ],
                        on_select_changed=self.app_layout.edit_values_config
                    ),
                    DataRow(
                        cells=[
                            DataCell(content=Text("Cor Gale 2")),
                            DataCell(
                                content=Row(
                                    [
                                        Text("R$", color=GREEN_MEDIUM),
                                        self.config_betg2
                                    ]
                                )
                            )
                        ],
                        on_select_changed=self.app_layout.edit_values_config
                    ),
                    DataRow(
                        cells=[
                            DataCell(content=Text("Cor Gale 3")),
                            DataCell(
                                content=Row(
                                    [
                                        Text("R$", color=GREEN_MEDIUM),
                                        self.config_betg3
                                    ]
                                )
                            )
                        ],
                        on_select_changed=self.app_layout.edit_values_config
                    ),
                    DataRow(
                        cells=[
                            DataCell(content=Text("Branco sem Gale")),
                            DataCell(
                                content=Row(
                                    [
                                        Text("R$", color=GREEN_MEDIUM),
                                        self.config_bcobetg0
                                    ]
                                )
                            )
                        ],
                        on_select_changed=self.app_layout.edit_values_config
                    ),
                    DataRow(
                        cells=[
                            DataCell(content=Text("Branco Gale 1")),
                            DataCell(
                                content=Row(
                                    [
                                        Text("R$", color=GREEN_MEDIUM),
                                        self.config_bcobetg1
                                    ]
                                )
                            )
                        ],
                        on_select_changed=self.app_layout.edit_values_config
                    ),
                    DataRow(
                        cells=[
                            DataCell(content=Text("Branco Gale 2")),
                            DataCell(
                                content=Row(
                                    [
                                        Text("R$", color=GREEN_MEDIUM),
                                        self.config_bcobetg2
                                    ]
                                )
                            )
                        ],
                        on_select_changed=self.app_layout.edit_values_config
                    ),
                    DataRow(
                        cells=[
                            DataCell(content=Text("Branco Gale 3")),
                            DataCell(
                                content=Row(
                                    [
                                        Text("R$", color=GREEN_MEDIUM),
                                        self.config_bcobetg3
                                    ]
                                )
                            )
                        ],
                        on_select_changed=self.app_layout.edit_values_config
                    ),
                ],
            )

    def build(self):
        return self.table
