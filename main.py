from flet import (AlertDialog, AppBar, Container, Divider, ElevatedButton,
                  Icon, Page, PopupMenuButton, PopupMenuItem, Text, TextField,
                  Column, UserControl, icons, margin, app)

from app_layout import AppLayout
from colors import BLACK_PRIMARY, CYAN_PRIMARY
from data_base import DataBaseUser


class DoubleRandom(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.db = DataBaseUser()
        self.user = False
        self.user_id = None
        self.chat_id = None
        self.token = None
        self.appbar_items = [
            PopupMenuItem(text="Entrar", on_click=self.login),
            PopupMenuItem(),  # divider
            PopupMenuItem(
                text="Editar Token/ChatId",
                on_click=self.edit_profile
            ),
            PopupMenuItem(),  # divider
            PopupMenuItem(text="Sair", on_click=self.login),
        ]
        self.appbar = AppBar(
            leading=Icon(icons.LOCAL_FIRE_DEPARTMENT_OUTLINED),
            leading_width=100,
            title=Text(
                "Double Random",
                size=32,
                text_align="start"
            ),
            center_title=True,
            toolbar_height=75,
            bgcolor=BLACK_PRIMARY,
            actions=[
                Container(
                    content=PopupMenuButton(
                        items=self.appbar_items
                    ),
                    margin=margin.only(left=50, right=25)
                )
            ],
        )
        self.layout = AppLayout(
            self,
            self.page,
            tight=True,
            expand=True,
            vertical_alignment="start",
        )
        self.page.appbar = self.appbar
        self.page.add(Divider(color=CYAN_PRIMARY))
        self.page.update()

    def build(self):
        self.layout = AppLayout(
            self,
            self.page,
            tight=True,
            expand=True,
            vertical_alignment="start",
        )
        return self.layout

# __------Editar Token E Chat_id do Telegram------__ #

    def edit_profile(self, e):

        def close_dlg_not_user(e):
            dialog_not_user.open = False
            self.page.update()
            return

        def close_dlg(e):
            if token.value == "" and chat_id.value == "":
                token.error_text = "Por favor insira um token"
                chat_id.error_text = "Por favor insira um chat id"
                self.page.update()
                return
            if token.value != "" and chat_id.value == "":
                token.error_text = ""
                chat_id.error_text = "Por favor insira um chat id"
                self.page.update()
                return
            if token.value == "" and chat_id.value != "":
                token.error_text = "Por favor insira um token"
                chat_id.error_text = ""
                self.page.update()
                return
            else:
                self.db.update_from(
                    f"tokenbot='{token.value}' WHERE nameuser='{self.user_id}'"
                )
                self.db.update_from(
                    f"chatid='{chat_id.value}' WHERE nameuser='{self.user_id}'"
                )
                user = self.db.select_from(False)
                dialog_edit.open = False
                self.appbar_items[0] = PopupMenuItem(
                    text=f"{user[0][1]}'s Profile"
                )
                self.page.update()

        token = TextField(label="Novo Token", width=300)
        chat_id = TextField(label="Novo Chat Id", width=300)
        dialog_not_user = AlertDialog(
            title=Text("Nenhum usuario conectado"),
            content=ElevatedButton(text="Ok", on_click=close_dlg_not_user),
            on_dismiss=lambda e: print("Modal dialog dismissed!")
        )
        dialog_edit = AlertDialog(
            title=Text("Insira seu token e chat id"),
            content=Column(
                [
                    token,
                    chat_id,
                    ElevatedButton(text="Editar", on_click=close_dlg),
                ],
                tight=True,
            ),
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        if not self.user:
            self.page.dialog = dialog_not_user
            dialog_not_user.open = True
            self.page.update()
        else:
            self.page.dialog = dialog_edit
            dialog_edit.open = True
            self.page.update()

    # __ ------LOGIN DE USUARIO NO APP COM CHECK DE CREDENCIAL----- __ #

    def login(self, e):

        def close_dlg(e):
            if user_name.value == "" and password.value == "":
                user_name.error_text = "Please insert User Name"
                password.error_text = "Please insert Password"
                self.page.update()
                return
            if user_name.value != "" and password.value == "":
                user_name.error_text = ""
                password.error_text = "Please insert User Name"
                self.page.update()
                return
            if user_name.value == "" and password.value != "":
                user_name.error_text = "Please insert User Name"
                password.error_text = ""
                self.page.update()
                return
            else:
                user = self.db.select_from(
                    f"WHERE email='{user_name.value}'"
                )
                if len(user) <= 0:
                    user_name.error_text = "Usuario ou senha incorreto!"
                    password.error_text = "Usuario ou senha incorreto!"
                    self.page.update()
                    return

                if user_name.value == user[0][2]:
                    if password.value == user[0][3]:
                        self.user = True
                        self.user_id = user[0][1]
                        self.token = user[0][4]
                        self.chat_id = user[0][5]
                        self.page.client_storage.set(
                            "current_user",
                            user_name.value
                        )
                else:
                    user_name.error_text = "Usuario ou senha incorreto!"
                    password.error_text = "Usuario ou senha incorreto!"
                    self.page.update()
                    return

            dialog.open = False
            self.appbar_items[0] = PopupMenuItem(
                text=f"{user[0][1]}'s Profile"
            )
            self.page.update()

        user_name = TextField(label="User name")
        password = TextField(label="Password", password=True)
        dialog = AlertDialog(
            title=Text("Please enter your login credentials"),
            content=Column(
                [
                    user_name,
                    password,
                    ElevatedButton(text="Login", on_click=close_dlg),
                ],
                tight=True,
            ),
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()


def main(page: Page):

    page.title = "Bot Double Random"
    page.padding = 0
    page.fonts = {
        "drius": "/driusital.ttf"
    }
    page.window_width = 800
    page.window_height = 800
    page.bgcolor = BLACK_PRIMARY
    page.update()
    app = DoubleRandom(page)
    page.add(app)
    page.update()


app(target=main, assets_dir="./assets", view="web_browser")
