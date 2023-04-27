from sklearn.preprocessing import MinMaxScaler
import numpy as np
import yfinance as yf
from datetime import date, timedelta, datetime
import keras


def predict(symbol: str, start_date: str):
    # Load the saved model
    saved_model = keras.models.load_model('app/model/stock_prediction_model.h5')

    # Get the stock data from yfinance
    new_df = yf.download(symbol, start=start_date, end=datetime.now())
    new_data = new_df.filter(['Close'])
    new_dataset = new_data.values
    
    # Scale the new data using the same scaler used during training
    scaler = MinMaxScaler(feature_range=(0,1))
    new_scaled_data = scaler.fit_transform(new_dataset)

    # Create the testing data set for the new stock
    x_test = []

    for i in range(60, len(new_scaled_data)):
        x_test.append(new_scaled_data[i-60:i, 0])

    x_test = np.array(x_test)

    # Reshape the data
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    # Use the saved model to make predictions
    predictions = saved_model.predict(x_test)

    # Scale the predictions back to original values
    predictions = scaler.inverse_transform(predictions)

    # Predict the next 5 days of closing values
    next_predictions = []
    for i in range(5):
        next_prediction = saved_model.predict(np.array([new_scaled_data[-60:, 0]]).reshape(1, 60, 1))
        next_predictions.append(next_prediction)
        new_scaled_data = np.append(new_scaled_data, next_prediction, axis=0)

    # Scale the next predictions back to original values
    next_predictions = scaler.inverse_transform(np.array(next_predictions).reshape(-1, 1))
    
    start_date = date(*[int(date) for date in start_date.split("-")])
    end_date = date.today() + timedelta(days=5)

    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days)]
    
    return new_dataset[60:], next_predictions, date_range