from src.converter import Converter
from src.storage import Storage
import json
import unittest
from unittest.mock import patch


class ConverterTest(unittest.TestCase):

    with open("test/test_exchange_rates.json", "r") as file:
        test_rates = json.loads(file.read())

    def setUp(self):
        self.rates_mock = unittest.mock.patch.object(Storage, "get_dict")
        self.rates_mock.return_value = self.test_rates

    def test_one_to_one(self):
        with self.rates_mock as mock:
            mock.return_value = self.test_rates
            converter = Converter(input_currency="AUD", amount=1, output_currency="CZK")
            result, status_code = converter.convert()
            self.assertEqual(result["input"]["currency"], "AUD")
            self.assertEqual(result["output"]["CZK"], 15.65)
            self.assertEqual(status_code, 200)

    def test_one_to_all(self):
        with self.rates_mock as mock:
            mock.return_value = self.test_rates
            converter = Converter(input_currency="AUD", amount=1)
            result, status_code = converter.convert()
            self.assertEqual(result["input"]["currency"], "AUD")
            self.assertEqual(result["input"]["amount"], 1)
            self.assertEqual(len(result["output"]), 33)
            self.assertEqual(status_code, 200)

    def test_many_to_one(self):
        with self.rates_mock as mock:
            mock.return_value = self.test_rates
            converter = Converter(input_currency="$", amount=1, output_currency="US$")
            result, status_code = converter.convert()
            self.assertEqual(
                result,
                "Too many input currency options! Please insert a currency code/symbol matching the unique currency.",
            )
            self.assertEqual(status_code, 400)

    def test_symbol_to_symbol(self):
        with self.rates_mock as mock:
            mock.return_value = self.test_rates
            converter = Converter(input_currency="£", amount=1, output_currency="zł")
            result, status_code = converter.convert()
            self.assertEqual(result["input"]["currency"], "GBP")
            self.assertEqual(result["input"]["amount"], 1)
            self.assertEqual(len(result["output"]), 1)
            self.assertEqual(list(result["output"].keys())[0], "PLN")
            self.assertEqual(list(result["output"].values())[0], 4.94)
            self.assertEqual(status_code, 200)

    def test_non_valic_code(self):
        with self.rates_mock as mock:
            mock.return_value = self.test_rates
            converter = Converter(input_currency="XYZ", amount=1)
            result, status_code = converter.convert()
            self.assertEqual(
                result,
                "Unsupported currency symbol/code! Please check inserted values with supported values help and try again!",
            )
            self.assertEqual(status_code, 400)

    def test_empty_rates_storage(self):
        with self.rates_mock as mock:
            mock.return_value = {}
            converter = Converter(input_currency="CZK", amount=1)
            result, status_code = converter.convert()
            self.assertEqual(
                result,
                "Missing currency exchange rates. Please try to update the storage.",
            )
            self.assertEqual(status_code, 400)


if __name__ == "__main__":
    unittest.main()
