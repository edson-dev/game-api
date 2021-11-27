from typing import Optional

from fastapi import APIRouter, FastAPI
import requests

class Crypto():
    def __init__(self, app: FastAPI, repository, access_point="/crypto", dependencies=None):
        self.router = APIRouter()
        self.repository = repository
        self.init_app(self.router)
        app.include_router(prefix=access_point,
                           router=self.router,
                           tags=[access_point],
                           dependencies=dependencies)

    def init_app(self, router):
        @router.post("/")
        async def get_all(currency_name: Optional[str] = "btc"):
            url = f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=1000000'
            response = requests.get(url)
            data = response.json()
            return data

        @router.post("/plataforms")
        async def get_platforms():
            url = f'https://api.coingecko.com/api/v3/finance_platforms'
            response = requests.get(url)
            data = response.json()
            return data
