from pydantic import BaseModel
from typing import List, Optional


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

