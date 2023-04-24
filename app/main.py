from fastapi import FastAPI
from .routers import stock_router


app = FastAPI(title="Investo Bot Backend", docs_url="/")

app.include_router(stock_router)