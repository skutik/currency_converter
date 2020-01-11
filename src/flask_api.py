from flask import Flask, request, jsonify
from src.converter import Converter, supported_currencies
from src.downloader import CurrencyDowloader
import logging

app = Flask(__name__)
downloader = CurrencyDowloader(supported_currencies)
downloader.update()


@app.route("/")
def index():
    return ("Convetor App!"), 200


@app.route("/currency_converter", methods=["GET"])
def currency_converter():
    if request.method == "GET":
        if request.args.get("input_currency", type=str) and request.args.get("amount", type=float):
            converter = Converter(input_currency=request.args.get("input_currency", type=str),
                                  amount=request.args.get("amount", type=float),
                                  output_currency=request.args.get("output_currency"))
            return jsonify(converter.convert()), 200
        else:
            return jsonify(message="Missing one or both required params."), 400
    else:
        return jsonify(message="Unsupported HTTP method."), 400

@app.route("/update", methods=["GET"])
def update_rates():
    if request.method == "GET":
        return jsonify(message=downloader.update()), 200
    else:
        return jsonify(message="Unsupported HTTP method."), 400
