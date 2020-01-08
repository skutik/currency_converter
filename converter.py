from os import getenv
import json
from requests import get
from random import choice

class Converter():

    SUPPORTED_CURRENCIES = {}
    API_KEY = getenv("CONV_API_KEY")

    def __init__(self, input_currency, amount, output_currency):
        self._get_currencies_list()
        self.input_currency = input_currency.upper()
        self.amount = amount
        self.output_currency = (output_currency.upper()) if output_currency else {choice(list(self.SUPPORTED_CURRENCIES)) for _ in range(5)}

    def _get_currencies_list(self):
        response = get(f"https://free.currconv.com/api/v7/currencies?apiKey={self.API_KEY}")
        if response.status_code == 200:
            self.SUPPORTED_CURRENCIES = json.loads(response.text)["results"]
        else:
            raise("Update of currencies failed!")

    def convert(self):
        print(self.output_currency)
        if self.input_currency in self.SUPPORTED_CURRENCIES:
            response = get(f"https://free.currconv.com/api/v7/convert?apiKey={self.API_KEY}&q={self.input_currency}_{self.output_currency}&compact=utlra")
            if response.status_code == 200:
                rate = json.loads(response.text)["results"][f"{self.input_currency}_{self.output_currency}"]["val"]
                dict ={"input":{"currecy":self.input_currency, "amount": self.amount}, "output":{self.output_currency: round(self.amount *rate, 2)}}
                return json.dumps(dict, indent=2, sort_keys=True)
        else:
            return f"Unsupported currency code {self.input_currency}"