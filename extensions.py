import requests
import json

from config import keys


class APIException(Exception):
    pass


class CryptoConverter:

    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if base == quote:
            raise APIException(f"Нельзя конвертировать {base} в {quote}.")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f"Не корректный параметр: {base}")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f"Не корректный параметр: {quote}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не корректный параметр: {amount}")


        r = requests.get(f"https://free.currconv.com/api/v7/convert?q={base_ticker}_{quote_ticker},{quote_ticker}_{base_ticker}&compact=ultra&apiKey=5465afe591eba68bfba2")

        text = json.loads(r.content)[f"{base_ticker}_{quote_ticker}"]


        res = f"{int(amount)} {base} = {float(text) * int(amount)} {quote}"

        return res

    