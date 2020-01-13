# Currency converter

### Source and supported currencies

 - Currency rates are gathered via [RatesAPI](https://ratesapi.io/).
 - The service provides current and historical exchange rates published by European Central Bank (exchange rates are updated once per day at 15:00 CET).
 - Supported currencies:
 
Currency Code|Currency Symbol 
:---|:---
AUD|$
BGN|BGN
BRL|R$
CAD|$
CHF|Fr.
CNY|¥
CZK|Kč
DKK|Kr
GBP|£
HKD|HK$
HRK|kn
HUF|Ft
IDR|Rp
ILS|₪
INR|₹
ISK|kr
JPY|¥
KRW|W
MXN|$
MYR|RM
NOK|kr
NZD|NZ$
PHP|₱
PLN|zł
RON|L
RUB|R
SEK|kr
SGD|S$
THB|฿
TRY|TRY
USD|US$
ZAR|R

### Currency Converter
- Convert specified amount to other currency/currencies
- Takes two required arguments (`input_currency`, `amount`) and one optional (`output_currency`)
- `input_currency` - can be defined by 3-letter currency code (not case-sensitive) or currency symbol (case-sensitive). `input_currency` has to be **unique**, therefore symbol `$` can't be used because is shared between three different currencies (`AUD`, `CAD`, `MXN`)
- `amount` - an amount which will be converted to other currency/currencies
- `output_currency` - can be defined by 3-letter currency code (not case-sensitive) or currency symbol (case-sensitive). In the case of omitting, the attribute will be returned converted amount for all supported currencies.
- Action will print/return formatted JSON or error message.
- The app requires packages from `requirements.txt` for correct behavior

### Local Storage
 - The storage contains a JSON file with exchange rates for all supported currencies.
 - Storage is updated by *update* command or on the start-up of the web application.

#### Example

##### Currency converter

- CLI
```
python cli_converter.py conv --input_currency CZK --amount 20
```
- Web application (started with `python api_runner.py`)
```shell script
GET http://localhost:5000/currency_converter?input_currency=CZK&amount=20.05
```

- output
```
{
    "input": {
        "amount": 20.0,
        "currency": "CZK"
    },
    "output": {
        "AUD": 1.28,
        "BGN": 1.55,
        "BRL": 3.58,
        "CAD": 1.15,
        "CHF": 0.86,
        "CNY": 6.08,
        "CZK": 20.0,
        "DKK": 5.92,
        "EUR": 0.79,
        "GBP": 0.67,
        "HKD": 6.82,
        "HRK": 5.89,
        "HUF": 264.28,
        "IDR": 12083.11,
        "ILS": 3.05,
        "INR": 62.29,
        "ISK": 108.13,
        "JPY": 96.26,
        "KRW": 1018.01,
        "MXN": 16.52,
        "MYR": 3.58,
        "NOK": 7.82,
        "NZD": 1.33,
        "PHP": 44.33,
        "PLN": 3.36,
        "RON": 3.78,
        "RUB": 53.86,
        "SEK": 8.35,
        "SGD": 1.18,
        "THB": 26.55,
        "TRY": 5.16,
        "USD": 0.88,
        "ZAR": 12.51
    }
}
```

##### Storage update
- CLI
```
python cli_converter.py update
```
- Web application (started with `python api_runner.py`)
```shell script
GET http://localhost:5000/update
```

- output (for web application in JSON format)
```
Updated successfully
```