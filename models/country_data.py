from typing import Optional
from sqlmodel import SQLModel


class CountryData(SQLModel):
    country: Optional[str]
    exchange: Optional[str]
