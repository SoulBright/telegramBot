import json
import requests
from constant import currency


class APIException(Exception):
    pass


class CurrConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Вы сравниваете одинаковые валюты {base}')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise APIException(f'Не верная валюта {base}!\n Список валют /values')

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise APIException(f'Не верная валюта {base}!\n Список валют /values')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не верно указанно колличество - {amount}')

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        cur_base = json.loads(r.content)[currency[base]]
        cur_total = float(cur_base) * float(amount)
        return cur_total
