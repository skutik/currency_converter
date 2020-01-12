from flask import Flask, request, jsonify
from src.converter import Converter
from src.downloader import CurrencyDowloader
from src.config import supported_currencies
import logging
from markdown import markdown

logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)
downloader = CurrencyDowloader(supported_currencies)
downloader.update()


@app.route("/")
def index():
    with open("README.md", "r") as file:
        read_me = file.read()
    return markdown(read_me), 200


@app.route("/currency_converter", methods=["GET"])
def currency_converter():
    if request.method == "GET":
        input_currency = request.args.get("input_currency", type=str)
        amount = request.args.get("amount", type=float)
        output_currency = request.args.get("output_currency", type=str)
        logging.info(f"{input_currency} - {type(input_currency)}")
        logging.info(f"{output_currency}  - {type(output_currency)}")
        logging.info(f"{amount}  - {type(amount)}")
        if input_currency and amount:
            converter = Converter(
                input_currency=input_currency,
                amount=amount,
                output_currency=output_currency,
            )
            response, status_code = converter.convert()
            response = (
                jsonify(response) if status_code == 200 else jsonify(message=response)
            )
            return response, status_code
        else:
            return (
                jsonify(message="Missing required params or wrong type of params."),
                400,
            )
    else:
        return jsonify(message="Unsupported HTTP method."), 400


@app.route("/update", methods=["GET"])
def update_rates():
    if request.method == "GET":
        return jsonify(message=downloader.update()), 200
    else:
        return jsonify(message="Unsupported HTTP method."), 400
