from typing import List, Optional, Union
from fastapi import HTTPException, Query, Response
from fastapi.responses import HTMLResponse
import requests
from sqlalchemy import (
    ColumnElement,
    create_engine,
    select,
    text,
)
from sqlmodel import SQLModel, Session
from models.country_data import CountryData
from models.stock_data import StockData
from config import TWELVE_DATA_BASE_URL, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST

GET_STOCKS_URL = f"{TWELVE_DATA_BASE_URL}/stocks"

DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}"


def set_stock_data() -> Response:

    response = requests.get(GET_STOCKS_URL)
    engine = create_engine(DATABASE_URL, echo=True)
    SQLModel.metadata.create_all(engine)

    if response.status_code == 200:
        data = response.json()["data"]

        with Session(engine) as session:
            existing_record = session.execute(select(StockData)).first()
            if not existing_record:
                for item in data:
                    stock_data_instance = StockData(
                        symbol=item["symbol"],
                        name=item["name"],
                        currency=item["currency"],
                        exchange=item["exchange"],
                        mic_code=item["mic_code"],
                        country=item["country"],
                        type=item["type"],
                    )
                    session.add(stock_data_instance)
                session.commit()
                return HTMLResponse(
                    content="Data added successfully",
                    status_code=200,
                )
            else:
                return HTMLResponse(
                    content="OK, Data already exists",
                    status_code=200,
                )
    else:
        raise HTTPException(status_code=response.status_code, detail="Unexpected error")


def get_stock_list(
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
) -> List[StockData]:
    engine = create_engine(DATABASE_URL, echo=True)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:

        data_query = session.query(StockData)

        filters: Union[ColumnElement[bool], List[bool]] = []

        if country is not None:
            filters.append(StockData.country.ilike(f"%{country}%"))
        if exchange is not None:
            filters.append(StockData.exchange.ilike(f"%{exchange}%"))
        if symbol is not None:
            filters.append(StockData.symbol.ilike(f"%{symbol}%"))
        if name is not None:
            filters.append(StockData.name.ilike(f"%{name}%"))

        if filters:
            data_query = data_query.filter(*filters)

        data = data_query.all()

        if data:
            return data
        else:
            raise HTTPException(status_code=404, detail="No data found for the query")


def get_country_data() -> List[CountryData]:
    engine = create_engine(DATABASE_URL, echo=True)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        data_query = text(
            """
            SELECT country, STRING_AGG(DISTINCT exchange, ', ')
            FROM (
                SELECT DISTINCT country, exchange
                FROM stockdata
            ) AS subquery
            GROUP BY country;
            """
        )

        results = session.execute(data_query)
        data = []
        for row in results:
            country = row[0]
            exchange = row[1]
            if country and exchange:
                country_data = CountryData(
                    country=country,
                    exchange=exchange,
                )
                data.append(country_data)

        if data:
            return data
        else:
            raise HTTPException(
                status_code=500, detail="Error occurred while fetching country data"
            )
