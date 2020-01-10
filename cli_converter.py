from converter import Converter
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input_currency", type=str, required=True, help="Currency code of input currency.")
parser.add_argument("--output_currency", type=str, required=False, help="Currency code of output currency. Not required. In case of None will be returned all available currencies.")
parser.add_argument("--amount", type=float, required=True, help="Amount to be converted.")
# parser.add_argument("--help", "-h")

args = parser.parse_args()

print(args.output_currency)

conv = Converter(input_currency=args.input_currency,
                 amount=args.amount,
                 output_currency=args.output_currency)

conv._get_currencies_list()
print(conv.convert())