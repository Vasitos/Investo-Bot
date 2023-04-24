from pydantic import BaseModel
from datetime import date


class EMAResponse(BaseModel):
    action: str
    
    dates: list[date]
    
    ema_short: list[float]
    ema_long: list[float]
    closing_price: list[int]
    

class HistoryResponse(BaseModel):
    history: dict[str, dict[date, float]]
