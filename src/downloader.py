import aiohttp
import asyncio
import logging
from requests import get
from src.storage import Storage
import json


class CurrencyDowloader():

    def __init__(self, currencies: dict):
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
            tasks = [self._download_currency_rate(session, currency) for currency in self.currencies.keys()]
            return await asyncio.gather(*tasks)

    def _check_updates(self):
        response = get("https://api.ratesapi.io/api/latest")
        if response.status_code == 200:
            storage = Storage("test_db")
            latest_api_date = json.loads(response.text)["date"]
            logging.debug(latest_api_date)
            latest_storage_date = storage.get_dict().get("last_update")
            logging.debug(latest_storage_date)
            if latest_storage_date:
                return "update" if latest_storage_date < latest_api_date else "ok"
            else:
                return "empty"
        else:
            return "failed"

    def update(self):
        status = self._check_updates()
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
                updated_dict["currencies"][result[0]] = {}
                updated_dict["currencies"][result[0]]["rates"] = {}
                if result[1]:
                    logging.debug(json.loads(result[1])["rates"])
                    content = json.loads(result[1])
                    updated_dict["currencies"][result[0]]["rates"] = content["rates"]
                    if min_date == "" or min_date > content["date"]:
                        min_date = content["date"]
            updated_dict["last_update"] = min_date
            logging.debug(updated_dict)
            storage = Storage("test_db")
            storage.update_storage(updated_dict)
            return "Updated successfully"
