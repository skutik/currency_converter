import logging
import json
from src.storage import Storage
from src.config import supported_currencies, storage_name


class Converter:
    def __init__(self, input_currency, amount, output_currency=None):
        if not isinstance(input_currency, str):
            raise TypeError("input_currency has to be type of str")
        if not isinstance(amount, float) and not isinstance(amount, int):
            raise TypeError("amount has to be type of float or int")
        self.input_currency = self._get_currency_codes(input_currency)
        self.amount = amount
        self.output_currency = self._get_currency_codes(output_currency)
        logging.debug(self.input_currency)
        logging.debug(self.output_currency)

    def _get_currency_codes(self, currency):
        if not currency:
            return supported_currencies.keys()
        elif currency in supported_currencies.values():
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
        if self.input_currency and self.output_currency:
            if len(self.input_currency) > 1:
                return (
                    "Too many input currency options! Please insert a currency code/symbol matching the unique currency.",
                    400,
                )
            else:
                input_dict = {"amount": self.amount, "currency": self.input_currency[0]}
                storage = Storage(storage_name)
                rates = storage.get_dict()
                try:
                    rates = rates["currencies"][self.input_currency[0]]["rates"]
                    logging.info(rates)
                except KeyError:
                    rates = {}
                if rates:
                    output_dict = {
                        currency: round(rates[currency] * self.amount, 2)
                        if currency in rates
                        else None
                        for currency in self.output_currency
                    }
                    return (
                        json.dumps(
                            {"input": input_dict, "output": output_dict},
                            indent=4,
                            sort_keys=True,
                        )
                        if pretiffy
                        else {"input": input_dict, "output": output_dict},
                        200,
                    )
                else:
                    return (
                        "Missing currency exchange rates. Please try to update the storage.",
                        400,
                    )
        else:
            return (
                "Unsupported currency symbol/code! Please check inserted values with supported values help and try again!",
                400,
            )
