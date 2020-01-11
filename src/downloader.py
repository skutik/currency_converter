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
        logging.info(f"{currency}: with url {url} has been processed")
        async with session.get(url) as response:
            logging.info(f"Status code of response: {response.status}")
            if response.status == 200:
                return currency, await response.text()
            else:
                return currency, None

    async def _fetch_data(self):
        async with aiohttp.ClientSession() as session:
            logging.info("Session created")
            tasks = [self._download_currency_rate(session, currency) for currency in self.currencies.keys()]
            return await asyncio.gather(*tasks)

    def _check_date(self):
        response = get("https://api.ratesapi.io/api/latest")
        if response.status_code == 200:
            return json.loads(response.text)["date"]
        else:
            return "failed"

    def update(self):
        storage = Storage("test_db")
        latest_api_date = self._check_date()
        logging.info(latest_api_date)
        latest_storage_date = storage.get_dict().get("last_update")
        logging.info(latest_storage_date)
        if latest_storage_date:
            if latest_storage_date >= latest_api_date:
                if latest_api_date == "failed":
                    return "Update has failed. Please try later!"
                else:
                    return "Already are up to date."
        # loop = asyncio.get_event_loop()
        logging.info("Waiting for asyncio loop")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(self._fetch_data())
        updated_dict = {"currencies": {}}
        min_date = ""
        for result in results:
            updated_dict["currencies"][result[0]] = {}
            updated_dict["currencies"][result[0]]["symbol"] = self.currencies[result[0]]
            updated_dict["currencies"][result[0]]["rates"] = {}
            if result[1]:
                logging.info(json.loads(result[1])["rates"])
                content = json.loads(result[1])
                updated_dict["currencies"][result[0]]["rates"] = content["rates"]
                if min_date == "" or min_date > content["date"]:
                    min_date = content["date"]
        updated_dict["last_update"] = min_date
        logging.info(updated_dict)
        storage.update_storage(updated_dict)
        return "Updated successfully"
