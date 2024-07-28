from typing import Optional

from fastapi import APIRouter
import requests

router = APIRouter()


@router.post("/")
async def get_all(currency_name: Optional[str] = "BRL", amount: Optional[int] = 1):
    url = f'https://api.exchangerate.host/latest?base={currency_name}&amount={amount}'
    response = requests.get(url)
    data = response.json()
    data.pop("motd")
    return data
