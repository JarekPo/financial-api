from typing import Any, Dict, List, Union, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from pydantic import BaseModel
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


class HistoricalPrice(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    adjClose: float
    change: float
    changeOverTime: float
    changePercent: float
    unadjustedVolume: int
    volume: int
    vwap: float
    label: str


class HistoricalPriceResponse(BaseModel):
    symbol: Optional[str]
    historical: Optional[List[HistoricalPrice]]


class TickerData(BaseModel):
    symbol: str
    name: str
    currency: Optional[str]
    stockExchange: str
    exchangeShortName: str


@app.get("/historical-price", response_model=HistoricalPriceResponse | Dict[None, None])
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


@app.get("/search-ticker", response_model=List[TickerData])
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
