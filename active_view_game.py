# import requests
from flet import (BorderRadius, BoxShadow, Column, Container, ElevatedButton,
                  Page, Row, Text, UserControl)

from colors import BLACK_MEDIUM, CYAN_PRIMARY
from data_base import DataBaseOptions, DataBaseUser
from Random_blaze import DoubleRandomBot


class ActiveViewGame(UserControl):
    def __init__(
            self,
            page: Page,
            app_layout,
            app,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.page = page
        self.app_layout = app_layout
        self.app = app

        self.db_gaming_config = DataBaseOptions()
        self.db_gaming_user = DataBaseUser()

        initial_config = self.db_gaming_user.select_from(False)
        self.double = DoubleRandomBot(
            token=initial_config[0][4],
            chat_id=initial_config[0][5],
            login=initial_config[0][2],
            senha=initial_config[0][3],
            app=self,
            app_layout=self.app_layout,
            page=self.page
        )

        self.line_result = Row()
        self.line_statistics = Row(visible=False)
        self.line_alerts = Row(visible=False)
        self.btn_start = ElevatedButton("start Game", on_click=self.game_start)
        self.game_view = Container(
            content=Column(
                [
                    Text("ULTIMOS RESULTADOS", weight="bold"),
                    Container(
                        content=self.line_result,
                        bgcolor=BLACK_MEDIUM,
                        padding=5
                    ),
                    Container(
                        content=self.line_alerts,
                        bgcolor=BLACK_MEDIUM,
                        padding=5
                    ),
                    self.line_statistics,
                    self.btn_start,
                ],
                visible=True
            ),
            bgcolor=BLACK_MEDIUM,
            padding=10,
            shadow=BoxShadow(1.5, 1.5, CYAN_PRIMARY),
            border_radius=BorderRadius(2, 2, 2, 2),
            margin=5
        )

    def build(self):
        return self.game_view

    def game_start(self, e):
        bets_config = self.db_gaming_config.select_from(False)
        att_config = self.db_gaming_user.select_from(False)
        self.double.token = att_config[0][4]
        self.double.chat_id = att_config[0][5]
        self.btn_start.disabled = True
        self.double.init_bot(
            qtd_gales=3,
            cor_lista=bets_config[0][1],
            intervalo=bets_config[0][2],
            qtd_horarios=bets_config[0][11]
        )
