from typing import Dict, Union

from fastapi import HTTPException, Query
import requests
from config import API_KEY, FINANCIAL_API_BASE_URL
from models.historical_price import HistoricalPriceResponse

FINANCIAL_API_HISTORICAL_URL = f"{FINANCIAL_API_BASE_URL}/historical-price-full"


def get_historical_price(
    symbol: str = Query(
        ..., title="Symbol", description="Symbol of the financial instrument."
    ),
    date_start: str = Query(
        ..., title="Start Date", description="Start date for historical prices."
    ),
    date_end: str = Query(
        ..., title="End Date", description="End date for historical prices."
    ),
) -> Union[HistoricalPriceResponse, Dict[None, None]]:
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
            return HistoricalPriceResponse(symbol=symbol, historical=data["historical"])
        else:
            return {}
    elif response.status_code == 401:
        raise HTTPException(status_code=401, detail="Invalid API key")
    elif response.status_code == 404:
        return {}
    else:
        raise HTTPException(status_code=response.status_code, detail="Unexpected error")
