from fastapi import APIRouter
from app.ia import getStock, calculateEMA, determineActions
from app.schemas import EMAResponse, HistoryResponse


stock_router = APIRouter(prefix="/api/v1/stock",
                         tags=["Stock Recommendations"])


@stock_router.get("/{symbol}/suggest", response_model=EMAResponse)
async def suggestions(symbol: str):

    data = getStock(symbol)
    movingAverage = calculateEMA(data)
    action = determineActions(data, symbol)
    
    return {
                "action": action,
                "ema_short": movingAverage[0].tolist(),
                "ema_long": movingAverage[1].tolist(),
                "closing_price": movingAverage[2]['Close'].tolist(),
                "dates": movingAverage[0].index.tolist()
            }
    
@stock_router.get("/{symbol}/history", response_model=HistoryResponse)
async def history(symbol: str):
    
    data = getStock(symbol)
    
    return { "history": data.to_dict() }