from fastapi import APIRouter
from app.ia import predict
from app.schemas import PredictResponse


predict_router = APIRouter(prefix="/api/v1/predict",
                         tags=["Predict Closing Stock"])


@predict_router.get("/{symbol}", response_model=PredictResponse)
async def suggestions(symbol: str, start_date: str = "2020-01-01"):

    closing_price, predicted_closing_price, dates = predict(symbol, start_date)
    
    return {
                "dates": dates,
                "predicted_closing_price": predicted_closing_price.ravel().tolist(),
                "closing_price": closing_price.ravel().tolist(),
            }
