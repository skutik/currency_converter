import aiohttp
import asyncio
import logging
from requests import get
from src.storage import Storage
from src.config import supported_currencies
import json


class CurrencyDowloader:
    def __init__(self, currencies):
        if not isinstance(currencies, dict) and isinstance(currencies, list):
            raise TypeError("currencies has to be type of dict or list")
        self.currencies = currencies

    async def _download_currency_rate(self, session, currency):
        url = f"https://api.ratesapi.io/api/latest?base={currency}"
        logging.debug(f"{currency}: with url {url} has been processed")
        async with session.get(url) as response:
            logging.debug(f"Status code of response: {response.status}")
            if response.status == 200:
                return currency, await response.text()
            else:
                return currency, None

    async def _fetch_data(self):
        async with aiohttp.ClientSession() as session:
            logging.debug("Session created")
            currency_codes = self.currencies.keys() if isinstance(self.currencies, dict) else self.currencies
            tasks = [
                self._download_currency_rate(session, currency)
                for currency in currency_codes
            ]
            return await asyncio.gather(*tasks)

    def _check_updates(self):
        response = get("https://api.ratesapi.io/api/latest")
        if response.status_code == 200:
            storage = Storage("test_db")
            latest_api_date = json.loads(response.text)["date"]
            logging.debug(f"API date: {latest_api_date}")
            rates = storage.get_dict()
            latest_storage_date = rates.get("last_update")
            logging.debug(f"Storage date: {latest_storage_date}")
            if latest_storage_date:
                if (
                    latest_storage_date < latest_api_date
                    or [
                        currency
                        for currency, rates in rates["currencies"].items()
                        if rates["rates"].keys() != supported_currencies.keys()
                    ]
                    or rates["currencies"].keys() != supported_currencies.keys()
                ):
                    return "update"
                else:
                    return "ok"
            else:
                return "empty"
        else:
            return "failed"

    def update(self):
        status = self._check_updates()
        logging.debug(f"Status: {status}")
        if status == "ok":
            return "Already up to date."
        elif status == "failed":
            return "API call failed. Can't check for updates. Please try later"
        else:
            logging.debug("Waiting for asyncio loop")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(self._fetch_data())
            updated_dict = {"currencies": {}}
            min_date = ""
            for result in results:
                currency_code, response = result
                updated_dict["currencies"][currency_code] = {}
                updated_dict["currencies"][currency_code]["rates"] = {}
                if response:
                    logging.debug(json.loads(response).get("rates"))
                    content = json.loads(response)
                    updated_dict["currencies"][currency_code]["rates"] = content[
                        "rates"
                    ]
                    if (
                        currency_code not in updated_dict["currencies"][currency_code]["rates"]
                    ):  # API workaround - each currency returns rates including base currency itsefl, except EUR
                        updated_dict["currencies"][currency_code]["rates"][
                            currency_code
                        ] = 1.0
                    if min_date == "" or min_date > content["date"]:
                        min_date = content["date"]
            updated_dict["last_update"] = min_date
            logging.debug(updated_dict)
            storage = Storage("test_db")
            storage.update_storage(updated_dict)
            return "Updated successfully"
