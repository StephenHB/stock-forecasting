"""
This is for LSTM prediction
"""
import numpy as np
import holidays
import datetime as dt
import math
import pandas as pd

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error




def next_business_day(today):
"""
Tool package used to find the next business day
based on US calendar
"""
    one_day = dt.timedelta(days=1)
    holiday_us = holidays.US()
    next_day = today + one_day
    while next_day.weekday() in holidays.WEEKEND or next_day in holiday_us:
        next_day += one_day
    return next_day


class LstmPredict:
    """
    LSTM Predict model
    """
    def __init__(self):
        self.data = None
        self.look_back = None
        self.epochs_number = None
        self.batch_size_number = None
        self.neurons = None
        self.train_percent = 0.67
        self.column_name = "Adj Close_AAPL"



    def create_dataset(self, data, look_back=22):
    """
    Convert an array of values into a dataset matrix,
    default look_back =22
    """

        if look_back > len(data) + 1:
            raise "look_back cannot exceed the length of input"

        dataX, dataY = [], []
        for i in range(len(data) - look_back - 1):
            x = data[i : (i + look_back)]
            dataX.append(x)
            y = data[(i + look_back)]
            dataY.append(y)
        return np.array(dataX), np.array(dataY)

    #     """
    #     Build model for LSTM
    #     """

    #     def build_model(self,neurons=4):

    #         self.neurons = neurons

    #         model = Sequential()
    #         model.add(LSTM(self.neurons,input_shape=(1,look_back)))
    #         model.add(Dense(1))
    #         model.compile(loss='mean_squared_error',optimizer='adam')

    #         return model

    def fit_estimate(
        self, data, neurons=4, epochs_number=10, batch_size_number=10, look_back=22
    ):

        self.epochs_number = epochs_number
        self.batch_size_number = batch_size_number
        self.look_back = look_back
        self.neurons = neurons

        dataset = data[self.column_name].pct_change().fillna(0)
        dataset = dataset.values
        dataset = dataset.astype("float32")
        dataset = dataset.reshape(-1, 1)

        train_size = int(len(dataset) * self.train_percent)
        test_size = len(dataset) - train_size
        train = dataset[0:train_size, 0]
        test = dataset[int(self.train_percent) : int(len(dataset)), 0]

        # Define X=[n:n+look_back], Y=n+look_back+1
        trainX, trainY = self.create_dataset(train, self.look_back)
        testX, testY = self.create_dataset(test, self.look_back)

        # Reshape input to be [samples, time steps, features]
        trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
        testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

        # Build the model
        model = Sequential()
        model.add(LSTM(self.neurons, input_shape=(1, self.look_back)))
        model.add(Dense(1))
        model.compile(loss="mean_squared_error", optimizer="adam")

        # Predict train and test
        model.fit(
            trainX,
            trainY,
            epochs=self.epochs_number,
            batch_size=self.batch_size_number,
            verbose=0,
        )
        trainPredict = model.predict(trainX)
        testPredict = model.predict(testX)

        # MSE calculation
        trainScore = math.sqrt(mean_squared_error(trainY, trainPredict[:, 0]))
        testScore = math.sqrt(mean_squared_error(testY, testPredict[:, 0]))
        print("Train Score: %.5f RMSE" % (trainScore))
        print("Test Score: %.5f RMSE" % (testScore))

        # Return to Price
        price_t = data[self.column_name][(train_size + self.look_back + 1) : len(data)]
        price_times_expected_growth = price_t * (1 + testPredict[0, :])
        df_price_predicted = price_times_expected_growth.shift(1)
        df_price_predicted = df_price_predicted.to_frame()

        # Next business day as the one-day-lead forecast
        date_predicted = next_business_day(price_t.index[-1])
        value_predicted = (1 + testPredict[-1]) * price_t.iloc[-1]

        new_row = pd.DataFrame(
            value_predicted,
            index=[date_predicted],
            columns=list(df_price_predicted.columns),
        )
        # Append the new_row to the df_price_predicted dataframe
        df_price_predicted = df_price_predicted.append(new_row)

        return df_price_predicted
