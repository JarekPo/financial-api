from typing import Dict
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root() -> Dict[str, str]:
    return {"Financial": "API"}
