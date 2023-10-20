import pendulum
from pendulum.datetime import DateTime
import requests
# import random
from typing import List, Dict, Any


class ProbabilityDouble:
    def __init__(self) -> None:
        self.tz = pendulum.now().timezone_name

    def conversor_de_horarios(self, horario: str) -> DateTime:
        return pendulum.parse(horario).in_timezone(self.tz)

    def historico_double(self) -> List[Dict]:
        url = 'https://blaze-4.com/api/roulette_games/history'
        while True:
            try:
                return requests.get(url).json()['records']
            except Exception:
                continue

    def statisticas_double(self) -> Dict[str, str]:
        dict_return = {}
        url = 'https://blaze-1.com/api/roulette_games/history'
        records = requests.get(url).json()['records']
        qtd_rounds = len(records)
        qtd_black = 0
        qtd_white = 0
        qtd_red = 0
        for i in records:
            if i['color'] == 'red':
                qtd_red += 1
            if i['color'] == 'black':
                qtd_black += 1
            if i['color'] == 'white':
                qtd_white += 1
        dict_return['qtd_red'] = qtd_red
        dict_return['porc_red'] = (
            qtd_red * 100 / qtd_rounds if qtd_red > 0 else 0
        )
        dict_return['qtd_black'] = qtd_black
        dict_return['porc_black'] = (
            qtd_black * 100 / qtd_rounds if qtd_black > 0 else 0
        )
        dict_return['qtd_white'] = qtd_white
        dict_return['porc_white'] = (
            qtd_white * 100 / qtd_rounds if qtd_white > 0 else 0
        )
        return dict_return

    def por_id(self, id: str) -> List[Dict]:
        results = self.historico_double()
        search = []
        for i in results:
            if i['id'] == id:
                search.append(i)
        return search

    def por_cor(self, cor: str) -> List[Dict]:
        results = self.historico_double()
        search = []
        for i in results:
            if i['color'] == cor:
                search.append(i)
        return search

    def por_numero(self, numero: int) -> List[Dict]:
        results = self.historico_double()
        search = []
        for i in results:
            if i['roll'] == numero:
                search.append(i)
        return search

    def por_horario(self, horario: str) -> List[Dict]:
        results = self.historico_double()
        search = []
        for i in results:
            h_result = pendulum.parse(
                i['created_at']
            ).in_timezone(self.tz).format("HH:mm")
            if horario == h_result:
                search.append(i)
        return search

    def procurar_resultado(
            self,
            por_horario: str | None = None,
            por_cor: str | None = None,
            por_numero: int | None = None,
            por_id: str | None = None,
    ) -> List[Dict]:
        if por_horario:
            return self.por_horario(por_horario)
        if por_cor:
            return self.por_cor(por_cor)
        if por_numero:
            return self.por_numero(por_numero)
        if por_numero:
            return self.por_id(por_id)

    def diferenca_horario(self, cor: str) -> int:
        dif = self.media_horarios(cor)
        qtd = len(dif)
        soma = sum(dif)
        return int(soma / qtd)

    def media_horarios(self, cor: str):
        difs = []
        resultado = self.procurar_resultado(por_cor=cor)
        index = -1
        for _ in range(len(resultado)):
            try:
                horario1 = self.conversor_de_horarios(
                    resultado[index]['created_at']
                )
                index -= 1
                horario2 = self.conversor_de_horarios(
                    resultado[index]['created_at']
                )
                dife = horario1.diff(horario2).in_minutes()
                difs.append(dife)
            except Exception:
                continue
        return difs


class HistoryAnalytics:
    def __init__(self) -> None:
        self.url_base: str = 'https://blaze-1.com/api/'\
            'roulette_games/history_analytics?n='

    def request_api(self, qtd: int) -> Dict[Any, Any]:
        return requests.get(f'{self.url_base}{qtd}').json()

    def porcentagem_por_cor(self, qtd: int, cor: str) -> float:
        if cor.lower() == 'branco':
            return float(
                self.request_api(qtd)['colors_info'][0]['percent']
            )
        if cor.lower() == 'vermelho':
            return float(
                self.request_api(qtd)['colors_info'][2]['percent']
            )
        return float(self.request_api(qtd)['colors_info'][1]['percent'])

    def quantidade_por_numero(self, qtd: int, numero: int) -> int:
        numeros = self.request_api(qtd)['rolls_info']
        for number in numeros:
            if number['roll'] == numero:
                return int(number['count'])

    def porcentagem_por_numero(self, qtd: int, numero: int) -> float:
        numeros = self.request_api(qtd)['rolls_info']
        for number in numeros:
            if number['roll'] == numero:
                return float(number['percent'])


if __name__ == "__main__":
    analytics = HistoryAnalytics()

if __name__ == "__main__":
    pro = ProbabilityDouble()
