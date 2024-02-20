from typing import Dict, List, Optional, Union
from fastapi import FastAPI, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import ColumnElement
from models.historical_price import HistoricalPriceResponse
from models.stock_data import StockData, StockDataInput
from models.ticker_data import TickerData
from services.historical_price_service import get_historical_price
from services.stock_data_service import get_stock_list, set_stock_data
from services.ticker_service import get_ticker_list
import uvicorn

app = FastAPI(title="Financial Analysis")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://financial-ui.onrender.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root() -> Dict[str, str]:
    return {"Health": "OK"}


@app.get(
    "/historical-price", response_model=Union[HistoricalPriceResponse, Dict[None, None]]
)
def handle_historical_price_request(
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
    return get_historical_price(symbol, date_start, date_end)


@app.get("/search-ticker", response_model=List[TickerData])
def handle_ticker_search_request(
    query: str = Query(..., title="Query", description="Query for the ticker list.")
) -> List[TickerData]:
    return get_ticker_list(query)


@app.post("/stocks", response_model=StockDataInput)
def handle_stock_data_create() -> Response:
    return set_stock_data()


@app.get("/stock-search", response_model=list[StockData])
def handle_stock_search_request(
    country: Optional[str] = Query(
        None, title="Country", description="Country of the financial instrument."
    ),
    exchange: Optional[str] = Query(
        None, title="Exchange", description="Exchange for financial instrument."
    ),
    symbol: Optional[str] = Query(
        None, title="Symbol", description="Symbol for financial instrument."
    ),
    name: Optional[str] = Query(
        None, title="Name", description="Name for financial instrument."
    ),
) -> list[StockData]:
    return get_stock_list(country, exchange, symbol, name)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
