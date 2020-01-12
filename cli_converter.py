from src.converter import Converter
from src.downloader import CurrencyDowloader
from src.config import supported_currencies
import argparse
import logging

# logging.getLogger().setLevel(logging.DEBUG)

desc = """
Supported currencies - 
Currency code (Currency symbol):
"""
for key, value in supported_currencies.items():
    desc += f"{key} ({value}), "

# Top-level paraser
parser = argparse.ArgumentParser(description=desc[:-2], prog="Currency converter")
subparsers = parser.add_subparsers(dest="action", help="Action commands.")

# Converter
conv_paraser = subparsers.add_parser("conv", help="Converting currencies.")
conv_paraser.add_argument(
    "--input_currency",
    type=str,
    required=True,
    help="Currency code/symbol of input currency.",
)
conv_paraser.add_argument(
    "--output_currency",
    type=str,
    required=False,
    help="Currency code/symbol to which will be amount converted to. Not required. In case of missing value will be returned all available currencies.",
)
conv_paraser.add_argument(
    "--amount", type=float, required=True, help="Amount to be converted."
)

# Storage update
update_parser = subparsers.add_parser("update", help="Update currency exchange rates.")

args = parser.parse_args()

if args.action == "conv":
    conv = Converter(
        input_currency=args.input_currency,
        amount=args.amount,
        output_currency=args.output_currency,
    )
    print(conv.convert(pretiffy=True)[0])
elif args.action == "update":
    downloader = CurrencyDowloader(supported_currencies)
    print(downloader.update())
