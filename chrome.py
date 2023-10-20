from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from typing import List
import os
from time import sleep

IPT_VALOR = "input.input-field"
BTN_2X = "button.double"
BTN_APOSTA = "div.place-bet button"
BTN_CORES = "div.select div"
CSS = "css selector"
RANK = "div.top div.user-rank"
NIVEL = "div.top div.level"
BANK = "div.currency"
MENU_SAQUE = "div.user"


class ApostaAutomaticaDouble:
    def __init__(self, user: str, senha: str) -> None:
        self.senha = senha
        self.user = user
        self.url = "https://blaze-1.com/pt/games/double?modal=auth&tab=login"
        path = os.getcwd()
        options = Options()
        service = Service(ChromeDriverManager().install())
        # options.add_argument("--start-maximized")
        # options.add_argument("--headless=new")
        options.add_argument(
            r"user-data-dir=" + path + "profile/Aviator"
        )
        self.chrome = Chrome(options=options, service=service)
        self.chrome.get(self.url)
        self.entrar()
        self._btn_cores = self.espera_elementos(self.chrome, BTN_CORES, 30)
        self._cpo_valor = self.espera_elemento(self.chrome, IPT_VALOR, 30)
        self._valor_banca = self.espera_elemento(self.chrome, BANK, 30)
        self._apostar = self.espera_elemento(self.chrome, BTN_APOSTA, 30)

    @property
    def valor_banca(self) -> str:

        """
        Propiedade da classe responsável por raspar o valor
        da conta de usuario!
        """

        try:
            return float(self._valor_banca.text.replace(
                ",",
                "."
            ).replace(
                "R$",
                ""
            ))
        except Exception:
            assert 0, "Valor não foi raspado erro ao tentar!"

    def espera_elemento(
            self,
            driver: WebDriver,
            selector: str,
            time: int
    ) -> WebElement:

        """
        Função responsável por esperar o elemento aparecer na tela
        sem gerar erro para o sistema!
        """

        for _ in range(time):
            try:
                return driver.find_element(CSS, selector)
            except Exception:
                sleep(1)
                continue
        assert 0, "Erro ao tentar selecionar o elemento na pagina"

    def espera_elementos(
            self,
            driver: WebDriver,
            selector: str,
            time: int
    ) -> List[WebElement]:

        """
        Função responsável por esperar o elemento aparecer na tela
        sem gerar erro para o sistema!
        """

        for _ in range(time):
            try:
                return driver.find_elements(CSS, selector)
            except Exception:
                sleep(1)
                continue
        assert 0, "Erro ao tentar selecionar o elemento na pagina"

    def entrar(self) -> None:
        """
        Função responsável por logar cada elemento selecionado em sequencia
        para que possa iserir o user a senha e clicar no botão de login!
        """
        try:
            self.chrome.find_element(
                "name", "username"
            ).send_keys(self.user)
            sleep(1)
            self.chrome.find_element(
                "name", "password"
            ).send_keys(self.senha)
            sleep(1)
            self.chrome.find_element(CSS, "button.submit").click()
            sleep(5)
            return
        except Exception:
            assert 0, "Erro ao logar na Blaze por favor reinicie o BOT!"

    def selecionar_botao_cor(self, cor: str) -> None:
        """
        Função responsável por selecionar o botão das cores
        Parâmetro cor: str = '🔴' ou '⚪️' ou '⚫️'

        ex: self.selecionar_botao_cor('🔴') :: seleciona a cor vermelha!
        """
        if cor == "🔴":
            self._btn_cores[0].click()
            return
        if cor == "⚪️":
            self._btn_cores[2].click()
            return
        if cor == "⚫️":
            self._btn_cores[4].click()
            return
        assert 0, "Cor selecionada errada por favor selecionar a cor correta!"

    def inserir_quantia(self, quantia: str) -> None:
        """
        Função responsável por inserir a quantia da aposta no campo
        primeiro ela apaga o campo apos apagar digita o valor!

        Parâmetro quantia = int ou float :
        exemplo1 float: self.inserir_quantia(quantia=0.10)
        exemplo2 int: self.inserir_quantia(10)
        """

        try:
            self._cpo_valor.send_keys(Keys.BACK_SPACE)
        except Exception:
            assert 0, "Erro ao apagar valor!"

        try:
            self._cpo_valor.send_keys(quantia)
        except (Exception, ValueError):
            assert 0, "Erro ao digitar o valor no campo!"

    def clicar_btn_aposta(self) -> None:

        """
        Função responsável por apostar realiza o click
        no botão apstar.
        """

        try:
            self._apostar.click()
        except Exception:
            return

    def realizar_aposta(self, stake: str, _cor: str):

        """
        Principal função do bot realiza as apostas de acordo com sua
        escolha por favor num mexer nessa função.

        Parânetro:: stake: str exemplo:(stake='0,50')
        Parânetro:: stake: str exemplo:(cor='red')

        Retorna Booleano: sucesso retorna True | erro retorna False;
        """

        try:
            banca = float(self._valor_banca.text.replace(
                "R$",
                ""
            ).replace(
                ",",
                "."
            ))

            self.selecionar_botao_cor(cor=_cor)
            sleep(0.5)

            self.inserir_quantia(quantia=stake)
            sleep(0.5)

            self.clicar_btn_aposta()
            sleep(0.5)

            nova_banca = float(self._valor_banca.text.replace(
                "R$",
                ""
            ).replace(
                ",", "."
            ))

            if banca > nova_banca:
                print(f"Valor em banca: R${nova_banca}")
                print(f"Valor Aposta: R${stake} ")
                print(f"Cor Aposta: {_cor} ")
                print("Aposta realizada com sucesso!")
                return
            print("Falha ao apostar! (Revise seu saldo ou reinicie o bot!)")
            return
        except Exception as erro:
            print(f"Erro: {erro}")
            return


if __name__ == "__main__":
    robo = ApostaAutomaticaDouble("ramonma31@gmail.com", "Manu.0512")
