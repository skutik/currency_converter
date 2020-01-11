import logging
import json
from src.storage import Storage

supported_currencies = {
    "AUD": "$",
    "BGN": "BGN",
    "BRL": "R$",
    "CAD": "$",
    "CHF": "Fr.",
    "CNY": "¥",
    "CZK": "Kč",
    "DKK": "Kr",
    "GBP": "£",
    "HKD": "HK$",
    "HRK": "kn",
    "HUF": "Ft",
    "IDR": "Rp",
    "ILS": "₪",
    "INR": "₹",
    "ISK": "kr",
    "JPY": "¥",
    "KRW": "W",
    "MXN": "$",
    "MYR": "RM",
    "NOK": "kr",
    "NZD": "NZ$",
    "PHP": "₱",
    "PLN": "zł",
    "RON": "L",
    "RUB": "R",
    "SEK": "kr",
    "SGD": "S$",
    "THB": "฿",
    "TRY": "TRY",
    "USD": "US$",
    "ZAR": "R",
}

class Converter:
    def __init__(self, input_currency, amount, output_currency):
        self.input_currency = self._get_currency_codes(input_currency)
        self.amount = amount
        if output_currency:
            output_currency = self._get_currency_codes(output_currency)
        self.output_currency = output_currency
        logging.debug(self.input_currency)
        logging.debug(self.output_currency)


    def _get_currency_codes(self, currency):
        if currency in supported_currencies.values():
            codes = list()
            for code, symbol in supported_currencies.items():
                if symbol == currency:
                    codes.append(code)
            return codes
        elif currency.upper() in supported_currencies:
            return [currency.upper()]
        else:
            return []

    def convert(self, pretiffy=False):
        if self.input_currency:
            if len(self.input_currency) > 1:
                return "Too many input currency options! Please insert a currency code/symbol matching the unique currency.", 400
            input_dict = {"amount": self.amount, "currency": self.input_currency[0]}
            storage = Storage("test_db")
            rates = storage.get_dict()
            try:
                rates = rates["currencies"][self.input_currency[0]]["rates"]
                logging.debug(rates)
            except KeyError:
                return "Missing currency rates data. Please try to update storage.", 400
            if self.output_currency:
                output_dict = {currency: round(rate * self.amount, 2) for currency, rate in rates.items() if currency in self.output_currency}
            else:
                output_dict = {currency: round(rate * self.amount, 2) for currency, rate in rates.items()}
            return json.dumps({"input": input_dict, "output": output_dict}, indent=4, sort_keys=True) if pretiffy else {"input": input_dict, "output": output_dict}, 200
        else:
            return "Unsupported input currency symbol/code! Please check input values or supported values help and try again!", 400

