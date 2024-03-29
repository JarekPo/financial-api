from typing import Optional
from pydantic import BaseModel


class TickerData(BaseModel):
    symbol: str
    name: str
    currency: Optional[str]
    stockExchange: Optional[str]
    exchangeShortName: Optional[str]
