from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import stock_router, predict_router


app = FastAPI(title="Investo Bot Backend", docs_url="/")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(predict_router)
app.include_router(stock_router)
