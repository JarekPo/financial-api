from typing import Dict, List, Union
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from models.historical_price import HistoricalPriceResponse
from models.ticker_data import TickerData
from services.historical_price_service import get_historical_price
from services.ticker_service import get_ticker_list
import uvicorn

app = FastAPI()

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


@app.get("/historical-price", response_model=HistoricalPriceResponse | Dict[None, None])
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
