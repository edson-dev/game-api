from typing import Optional

from fastapi import APIRouter
import requests

router = APIRouter()

@router.post("/")
async def get_all(currency_name: Optional[str] = "btc"):
    url = f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10000000'
    response = requests.get(url)
    data = response.json()
    return data

@router.post("/plataforms")
async def get_platforms():
    url = f'https://api.coingecko.com/api/v3/finance_platforms'
    response = requests.get(url)
    data = response.json()
    return data
