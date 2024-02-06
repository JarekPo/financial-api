from typing import Any, Dict, List, Union, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from config import API_KEY, FINANCIAL_API_BASE_URL

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://financial-ui.onrender.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

FINANCIAL_API_HISTORICAL_URL = f"{FINANCIAL_API_BASE_URL}/historical-price-full"
SEARCH_TICKER_URL = f"{FINANCIAL_API_BASE_URL}/search-ticker"


@app.get("/")
async def read_root() -> Dict[str, str]:
    return {"Health": "OK"}


@app.get("/historical-price")
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

    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="Invalid API key")
    elif response.status_code == 404:
        return {}
    else:
        raise HTTPException(status_code=response.status_code, detail="Unexpected error")


@app.get("/search-ticker")
def get_ticker_list(
    query: str = Query(..., title="Query", description="Query for the ticker list.")
) -> List[Dict[str, Optional[str]]]:
    params = {
        "apikey": API_KEY,
        "query": query,
    }

    response = requests.get(SEARCH_TICKER_URL, params=params)

    if response.status_code == 200:
        data: List[Dict[str, Optional[str]]] = response.json()
        return data
    else:
        raise HTTPException(status_code=response.status_code, detail="Unexpected error")
