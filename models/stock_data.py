from typing import Optional
from sqlmodel import SQLModel, Field


class StockDataInput(SQLModel):
    symbol: str
    name: str
    currency: str
    exchange: str
    mic_code: str
    country: str
    type: str


class StockData(StockDataInput, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
