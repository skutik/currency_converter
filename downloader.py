import aiohttp
import asyncio
import logging
from requests import get
from storage import Storage
import json


class CurrencyDowloader():

    def __init__(self, currencies):
        if isinstance(currencies, str):
            currencies = [currencies]
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
            tasks = [self._download_currency_rate(session, currency) for currency in self.currencies_list]
            return await asyncio.gather(*tasks)

    @property
    def _check_date(self):
        response = get("https://api.ratesapi.io/api/latest")
        if response.status_code == 200:
            return json.loads(response.text)["date"]
        else:
            return "failed"

    def update(self):
        storage = Storage("test_db")
        latest_api_date = self._check_date[0]
        latest_storage_date = storage.get_dict.get("last_update")
        if latest_storage_date:
            if latest_storage_date >= latest_api_date:
                if latest_api_date == "failed":
                    return "Update has failed. Please try later!"
                else:
                    return "Data are up to date."
        loop = asyncio.get_event_loop()
        logging.info("Waiting for asyncio loop")
        results = loop.run_until_complete(self._fetch_data())
        for result in results:
            print(result)