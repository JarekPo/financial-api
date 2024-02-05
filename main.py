from typing import Any, Dict, List, Union
from fastapi import FastAPI
import requests
from config import API_KEY, FINANCIAL_API_BASE_URL

app = FastAPI()

FINANCIAL_API_HISTORICAL_URL = f"{FINANCIAL_API_BASE_URL}/historical-price-full"


@app.get("/")
async def read_root() -> Dict[str, str]:
    return {"Health": "OK"}


@app.get("/historical-price")
async def get_historical_price(
    symbol: str, date_start: str, date_end: str
) -> Dict[str, Union[str, List[Dict[str, Any]]]]:
    params = {
        "apikey": API_KEY,
        "from": date_start,
        "to": date_end,
    }

    response = requests.get(
        f"{FINANCIAL_API_HISTORICAL_URL}/{symbol}",
        params=params,
    )

    if response.status_code == 200:
        data = response.json()
        if "historical" in data and data["historical"]:
            return {"symbol": symbol, "historical": data["historical"]}
        else:
            return {}
    elif response.status_code == 401:
        raise ValueError("Invalid API key")
    elif response.status_code == 404:
        raise ValueError("Unknown symbol")
    else:
        raise ValueError("Unexpected error")
