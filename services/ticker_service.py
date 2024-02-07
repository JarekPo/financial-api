from typing import List
from fastapi import HTTPException, Query
import requests
from config import API_KEY, FINANCIAL_API_BASE_URL
from models.ticker_data import TickerData


SEARCH_TICKER_URL = f"{FINANCIAL_API_BASE_URL}/search-ticker"


def get_ticker_list(
    query: str = Query(..., title="Query", description="Query for the ticker list.")
) -> List[TickerData]:
    params = {
        "apikey": API_KEY,
        "query": query,
    }

    response = requests.get(SEARCH_TICKER_URL, params=params)

    if response.status_code == 200:
        data: List[TickerData] = response.json()
        return data
    else:
        raise HTTPException(status_code=response.status_code, detail="Unexpected error")
