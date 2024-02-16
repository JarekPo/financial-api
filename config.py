from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("API_KEY")
FINANCIAL_API_BASE_URL = os.getenv("FINANCIAL_API_BASE_URL")

TWELVE_DATA_BASE_URL = os.getenv("TWELVE_DATA_BASE_URL")

DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
