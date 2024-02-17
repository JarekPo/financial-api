from fastapi import HTTPException, Response
from fastapi.responses import HTMLResponse
import requests
from sqlalchemy import create_engine, select
from sqlmodel import SQLModel, Session
from models.stock_data import StockData
from config import TWELVE_DATA_BASE_URL, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST

GET_STOCKS_URL = f"{TWELVE_DATA_BASE_URL}/stocks"

DATABASE_URL = f"mysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/financial"


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
