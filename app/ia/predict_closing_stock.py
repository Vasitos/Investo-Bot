from sklearn.preprocessing import MinMaxScaler
import numpy as np
import yfinance as yf
from datetime import date, timedelta, datetime
import keras


def predict(symbol: str, start_date: str, predict_days: int):
    # Load the saved model
    saved_model = keras.models.load_model('app/model/stock_prediction_model.h5')

    # Get the stock data from yfinance
    new_df = yf.download(symbol, start=start_date, progress=False)
    new_data = new_df.filter(['Close'])
    new_dataset = new_data.values
    dates = new_df.index.to_list()
    
    # Scale the new data using the same scaler used during training
    scaler = MinMaxScaler(feature_range=(0,1))
    new_scaled_data = scaler.fit_transform(new_dataset)

    # Predict the next 30 days of closing values
    next_predictions = []
    for _ in range(predict_days):
        next_prediction = saved_model.predict(np.array([new_scaled_data[-60:, 0]]).reshape(1, 60, 1))
        next_predictions.append(next_prediction)
        new_scaled_data = np.append(new_scaled_data, next_prediction, axis=0)

    # Scale the next predictions back to original values
    next_predictions = scaler.inverse_transform(np.array(next_predictions).reshape(-1, 1))

    next_date = dates[-1]
    
    for _ in range(1, predict_days + 1):
        # Add 1 day to the current date and check if it's a weekend
        next_date += timedelta(days=1)
        while next_date.weekday() >= 5:
            next_date += timedelta(days=1)
        dates.append(next_date)
    
    return new_dataset, next_predictions, dates