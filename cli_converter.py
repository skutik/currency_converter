from src.converter import Converter, supported_currencies
import argparse
import logging

logging.getLogger().setLevel(logging.DEBUG)

desc = """
Supported currencies - 
Currency code (Currency symbol):
\n\n\n

"""
for key, value in supported_currencies.items():
    desc += f"{key} ({value})".format(key, value)

parser = argparse.ArgumentParser(description=desc)
subparsers = parser.add_subparsers()

convert_app = subparsers.add_parser("", description="Currency converting")

parser.add_argument("--input_currency", type=str, required=True, help="Currency code of input currency.")
parser.add_argument("--output_currency", type=str, required=False, help="Currency code of output currency. Not required. In case of None will be returned all available currencies.")
parser.add_argument("--amount", type=float, required=True, help="Amount to be converted.")

download_data = subparsers.add_parser("download", description="Download data from API.")
# parser.add_argument("--help", "-h")

args = parser.parse_args()

conv = Converter(input_currency=args.input_currency,
                 amount=args.amount,
                 output_currency=args.output_currency)

# conv._get_currencies_list()
print(conv.convert(pretiffy=True))