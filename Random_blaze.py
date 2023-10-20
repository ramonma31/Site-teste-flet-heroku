import random
from typing import Any, Dict, List
from time import sleep

import pendulum
import requests
from flet import BorderRadius, Column, Container, Page, Text, alignment, Row
from pendulum.datetime import DateTime
from telebot import TeleBot
from telebot.apihelper import ApiTelegramException

from colors import BLACK_MEDIUM, BLACK_PRIMARY, BLACK_RESULT, RED_PRIMARY
# from chrome import ApostaAutomaticaDouble
from probability_double import ProbabilityDouble

MARTINGALE_STIPS = 0


class DoubleRandomBot:
    def __init__(
            self,
            token,
            chat_id,
            login,
            senha,
            app,
            app_layout,
            page: Page
    ) -> None:
        # --Definições do bot-- #
        self.token = token
        self.chat_id = chat_id
        self.login = login
        self.senha = senha
        self.app = app
        self.app_layout = app_layout
        self.page = page
        # self.bot = TeleBot(self.token)
        # self.chrome = ApostaAutomaticaDouble(self.login, self.senha)
        # --Listas de controle-- #
        self.cores_mista = ['🔴', '⚫️']
        self.cores_red = ['🔴']
        self.cores_black = ['⚫️']
        self.lista_conferencia: List[Any] = []
        self.resultados_corrigidos: List[Any] = []
        self.controle_resultados: List[Any] = []
        self.horarios_alert: List[Any] = []

        # --Controle de menssagens-- #
        self.start_game = False
        self.editar_alerta = False
        self.id_message_correcao = 0
        self.id_message_alertas = 0

        # --Controle de resultados-- #
        self.wins = 0
        self.branco_primeira = 0
        self.branco_gale = 0
        self.win_primeira = 0
        self.win_gale = 0
        self.loss = 0
        self.entradas = 0
        self.acertividade = 0
        self.wins_consecultivos = 0
        self.contador_correcao = 0
        self.controle_gales = 0
        self.count_gale = 0
        self.all_status = {
            "✅",
            "✅G1",
            "✅G2",
            "✅G3",
            "✅Branco",
            "✅Branco G1",
            "✅Branco G2",
            "✅Branco G3",
            "",
        }
        # --Urls de consulta Api-- #
        self.status_api = 'https://blaze-4.com/api/roulette_games/current'
        self.results_api = 'https://blaze-4.com/api/roulette_games/recent'
        self.historico_api = "https://blaze-4.com/api/roulette_games/history"

    # --Função envia nenssagens de correção-- #
    def enviar_correcao(self) -> None:
        dados = self.lista_conferencia
        resultados_corrigidos = [
            f'{i["horario"]}{i["cor"]}⚪️{i["palpite"]}' for i in dados if i["palpite"] in self.all_status
        ]
        self.app.line_alerts.controls.clear()
        self.app.line_alerts.controls.append(Column(
            [
                Text(f"ULTIMA JOGADA: {resultados_corrigidos[-1]}"),
                Text("AGUARDANDO PROXIMO SINAL...")
            ]
        ))
        self.app.line_statistics.controls.clear()
        entradas = self.wins + self.loss
        percent = self.wins * 100 / entradas if self.wins > 0 else 0
        self.app.line_statistics.controls.append(Column(
            [
                Text(
                    "⚙️ DADOS DO HACK.",
                    size=30,
                    weight="bold"
                ),
                Text(
                    f"🧾 Placar 🟢 {self.wins} 🔴 {self.loss}",
                    size=20,
                    weight="bold"
                ),
                Text(
                    f"🎯 Acertamos {percent}% das vezes",
                    size=20,
                    weight="bold"
                ),
                Text(
                    f"💰 Estamos com {self.wins_consecultivos} Greens seguidos!",
                    size=20,
                    weight="bold"
                ),
            ]
        ))
        self.app.line_alerts.visible = True
        self.app.line_statistics.visible = True
        self.app.update()
        # self.app_layout.update()
        self.page.update()

    # --Função responsavel por enviar menssagem de resultados-- #
    def estatisticas_resultados(self) -> None:
        entradas = self.wins + self.loss
        porcentagem = self.wins * 100 / entradas if self.wins > 0 else 0

    # --Função envia menssagem de sinal-- #
    def enviar_alerta(self, result: List[Dict]) -> None:
        falta_corrigir = [
            i for i in self.lista_conferencia if i['status'] == 'sem-correção'
        ]
        self.app.line_alerts.controls.clear()
        self.app.line_alerts.controls.append(Column(
            controls=[
                Text("🚨SINAL DOUBLE BLAZE🚨", weight="bold"),
                Text(f"HORA: {falta_corrigir[0]['horario']}", weight="bold"),
                Text(f"APOS: {result[0]['cor']} {result[0]['numero']}", weight="bold"),
                Text(f"APOSTAR: {falta_corrigir[0]['cor']}", weight="bold"),
            ]
            )
        )
        self.app.line_alerts.visible = True
        self.app.update()
        # self.app_layout.update()
        self.page.update()

    # --Função para converter os dados api em cores-- #
    def converte_cor(self, color: int) -> None | str:
        if color == 1:
            return '🔴'
        elif color == 2:
            return '⚫️'
        elif color == 0:
            return '⚪️'
        return "Null"

    # --Função responssavel pelo tempo de cada rodada-- #
    def status(self) -> str:
        while True:
            try:
                get = requests.get(self.status_api).json()
                break
            except Exception:
                continue
        return get['status']

    # --Função responssavel por coletar os resultados-- #
    def pegar_resultado(self) -> List[Dict]:
        lista_retorno: List[Dict] = []
        get = requests.get(self.results_api).json()
        if get[0]['id'] in self.controle_resultados:
            return lista_retorno
        date_time = pendulum.parse(get[0]['created_at'])
        date_timezone = date_time.in_timezone(pendulum.now().timezone_name)
        horario = date_timezone.format('HH:mm')
        numero = get[0]['roll']
        lista_retorno.append(
            {
                'horario': horario,
                'cor': self.converte_cor(get[0]['color']),
                'numero': numero
            }
        )
        self.controle_resultados.append(get[0]['id'])
        return lista_retorno

    def historico_blaze(self) -> List[int]:
        get = requests.get(self.results_api).json()
        return [int(i["roll"]) for i in get]

    # --Função responsavel por atualizar os contadores-- #
    def att_resultados(self, status: str) -> None:

        self.count_gale = 0

        match status:
            case "✅Branco":
                self.branco_primeira += 1
                self.wins += 1
                self.wins_consecultivos += 1
                return
            case "✅":
                self.win_primeira += 1
                self.wins += 1
                self.wins_consecultivos += 1
                return
            case "✅G1" | "✅G2" | "✅G3":
                self.win_gale += 1
                self.wins += 1
                self.wins_consecultivos += 1
                return
            case "✅Branco G1" | "✅Branco G2" | "✅Branco G3":
                self.branco_gale += 1
                self.wins += 1
                self.wins_consecultivos += 1
                return
            case "❌":
                self.loss += 1
                self.wins_consecultivos = 0
                return

    # --Função responsavel por atualizar o status dos dados da lista-- #
    def corrige_palpite(self, status: str, indice: int) -> None:

        if status in self.all_status:
            self.lista_conferencia[indice]['status'] = 'corrigido'
            self.lista_conferencia[indice]['palpite'] = status
            self.att_resultados(status)
            return
        self.mudar_gale(indice)
        return

    def mudar_gale(self, indx: int) -> None:
        self.lista_conferencia[indx]['status'] = 'correção-G1'
        return

    # --Função responssavel pelas condicionais da correção-- #
    def condicionais(
            self,
            index: int,
            horario_resultado: str,
            horario_palpite: str,
            status: str,
            cor_resultado: str,
            cor_palpite: str,
    ) -> None:

        if horario_resultado != horario_palpite:
            return

        if status == "sem-correção":
            if cor_resultado == cor_palpite:
                self.corrige_palpite("✅G1", index)
                self.enviar_correcao()
                return
            if cor_resultado == '⚪️':
                self.corrige_palpite("✅Branco G1", index)
                self.enviar_correcao()
                return
            self.corrige_palpite('mudar-gale', index)
            return

        if status == "correção-G1":
            if cor_resultado == cor_palpite:
                self.corrige_palpite("✅", index)
                self.enviar_correcao()
                return
            if cor_resultado == '⚪️':
                self.corrige_palpite("✅Branco", index)
                self.enviar_correcao()
                return
            return

        self.corrige_palpite("❌", index)
        self.enviar_correcao()
        return

    # --Função para corrigir a lista gerada-- #
    def corrige_lista(self, resultado: List[Dict]) -> None:
        horario_resultado = resultado[0]['horario']
        cor_resultado = resultado[0]['cor']
        horarios_palpite = [i['horario'] for i in self.lista_conferencia]
        cores_palpite = [i['cor'] for i in self.lista_conferencia]
        status = [i['status'] for i in self.lista_conferencia]

        for indice, item in enumerate(horarios_palpite):
            self.condicionais(
                indice,
                horario_resultado,
                item,
                status[indice],
                cor_resultado,
                cores_palpite[indice],
            )
        return

    # --Função responsavel por gerar a lista de palpites-- #
    def gerarLista(
        self,
        cor: str,
        intervalo_minutos: int,
        quantidade_horarios: int,
    ) -> List[str]:

        hora = pendulum.now(pendulum.now().timezone_name)
        horario_alerts = hora.subtract(minutes=1)
        horarios = []
        add = 0

        self.entradas = quantidade_horarios

        if cor.upper() == 'RED':
            cores = ['🔴']  # RED
        elif cor.upper() == 'BLACK':
            cores = ['⚫️']  # BLACK
        elif cor.upper() == 'MISTA':  # HARD MISTA G1
            cores = [
                '🔴', '⚫️', '🔴', '⚫️', '⚫️', '⚫️', '⚫️',
                '🔴', '⚫️', '🔴', '⚫️', '🔴', '🔴', '🔴'
            ]
        if intervalo_minutos == 0:
            result = random.sample(range(3, 60, 3), quantidade_horarios)
            result.sort()
            for i in result:
                cor = random.choice(cores)
                alerts = horario_alerts.add(minutes=i).format('HH:mm')
                horario = f"{hora.add(minutes=i).format('HH:mm')}:{cor}⚪️"
                horarios.append(horario)
                self.horarios_alert.append(alerts)
                self.lista_conferencia.append(
                    {
                        'status': 'sem-correção',
                        'palpite': '𝐀𝐠𝐮𝐚𝐫𝐝𝐚𝐧𝐝𝐨...',
                        'horario': hora.add(minutes=i).format('HH:mm'),
                        'cor': cor,
                    }
                )
            return horarios
        for _ in range(quantidade_horarios):
            add += intervalo_minutos
            cor = random.choice(cores)
            alerts = horario_alerts.add(minutes=add).format('HH:mm')
            horario = f"{hora.add(minutes=add).format('HH:mm')}:{cor}⚪️"
            horarios.append(horario)
            self.horarios_alert.append(alerts)
            self.lista_conferencia.append(
                {
                    'status': 'sem-correção',
                    'palpite': '𝐀𝐠𝐮𝐚𝐫𝐝𝐚𝐧𝐝𝐨...',
                    'horario': hora.add(minutes=add).format('HH:mm'),
                    'cor': cor,
                }
            )
        return horarios

    def reseta(self) -> None:
        self.lista_conferencia.clear()
        self.editar_alerta = not self.editar_alerta
        self.contador_correcao = 0
        self.wins = 0
        self.branco_primeira = 0
        self.branco_gale = 0
        self.win_primeira = 0
        self.win_gale = 0
        self.loss = 0
        self.entradas = 0
        self.acertividade = 0
        self.wins_consecultivos = 0
        return

    def mostra_resultado(self, resultados: List[int]) -> None:
        self.app.line_result.controls.clear()
        for i in resultados:
            if i in (1, 2, 3, 4, 5, 6, 7):
                self.app.line_result.controls.append(Container(
                    content=Text(f"{i}", weight="bold"),
                    width=40,
                    height=40,
                    bgcolor=RED_PRIMARY,
                    border_radius=BorderRadius(3, 3, 3, 3),
                    alignment=alignment.center
                ))
            if i in (8, 9, 10, 11, 12, 13, 14):
                self.app.line_result.controls.append(Container(
                    content=Text(f"{i}", weight="bold"),
                    width=40,
                    height=40,
                    bgcolor=BLACK_RESULT,
                    border_radius=BorderRadius(3, 3, 3, 3),
                    alignment=alignment.center
                ))
            if i in (0, 18):
                self.app.line_result.controls.append(Container(
                    content=Text(f"{i}", weight="bold", color=BLACK_RESULT),
                    width=40,
                    height=40,
                    bgcolor="white",
                    border_radius=BorderRadius(3, 3, 3, 3),
                    alignment=alignment.center
                ))
        self.app.update()
        # self.app_layout.update()
        self.page.update()

    def init_bot(
        self,
        qtd_gales,
        cor_lista,
        intervalo,
        qtd_horarios,
    ):

        # --Instancia do objeto ProbabilityDouble-- #
        probability = ProbabilityDouble()

        complete = False
        rolling = False
        waiting = False
        self.controle_gales = int(qtd_gales)

        if not qtd_gales:
            qtd_gales = 1

        if cor_lista.upper() not in ("RED", "BLACK", "MISTA"):
            pass

        try:
            intervalo_minutos = int(intervalo)
        except ValueError:
            intervalo_minutos = intervalo
        quantidade_horarios = int(qtd_horarios)

        horarios = self.gerarLista(
            cor_lista,
            intervalo_minutos,
            quantidade_horarios
        )

        # --LOOP DE CORREÇÃO DA LISTA GERADA-- #
        while quantidade_horarios > self.contador_correcao:
            if self.status() == 'complete' and not complete:
                complete = not complete
                waiting = False
                sleep(1)
                histo_double = self.historico_blaze()
                self.mostra_resultado(histo_double)
            if self.status() == 'waiting' and not waiting:
                resultado = self.pegar_resultado()
            # --Condição para o envio do sinal exatamente 1 jogada-- #
            # --Antes do horario do sinal-- #
                hora_result = resultado[0]['horario']
                if hora_result in self.horarios_alert:
                    if len(probability.procurar_resultado(
                        por_horario=hora_result
                    )) >= 2:
                        self.enviar_alerta(resultado)
                self.corrige_lista(resultado)
                waiting = not waiting
                rolling = False
            if self.status() == 'rolling' and not rolling:
                rolling = not rolling
                complete = False
    # --Envia as estatisticas do bot ao final da correção-- #
        self.estatisticas_resultados()
        self.app.btn_start.disabled = False
        self.app.update()
        self.page.update()
