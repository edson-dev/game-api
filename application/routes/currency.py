from typing import Optional

from fastapi import APIRouter, FastAPI
import requests

class Currency():
    def __init__(self, app: FastAPI, repository, access_point="/currency", dependencies=None):
        self.router = APIRouter()
        self.repository = repository
        self.init_app(self.router)
        app.include_router(prefix=access_point,
                           router=self.router,
                           tags=[access_point],
                           dependencies=dependencies)

    def init_app(self, router):
        @router.post("/")
        async def get_all(currency_name: Optional[str] = "BRL", amount: Optional[int] =1):
            url = f'https://api.exchangerate.host/latest?base={currency_name}'
            response = requests.get(url)
            data = response.json()
            data.pop("motd")
            return data

        @router.post("/crypto")
        async def get_all(currency_name: Optional[str] = "btc"):
            url = f'https://api.exchangerate.host/cryptocurrencies?base={currency_name}'
            response = requests.get(url)
            data = response.json()
            data.pop("motd")
            return data
