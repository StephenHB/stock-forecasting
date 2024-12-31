"""
This module is used for rolling average calculation
"""
import datetime as dt
import holidays
import pandas as pd


def next_business_day(today):
    """
    Tool package used to find the next business day
    based on US calendar
    """
    one_day_ahead = dt.timedelta(days=1)
    holiday_usa = holidays.US()
    next_day = today + one_day_ahead
    while next_day.weekday() in holidays.WEEKEND or next_day in holiday_usa:
        next_day += one_day_ahead
    return next_day


class RollingAverage:
    """
    This is module for rolling average fit and estimation
    """
    def __init__(self):
        self.data = None
        self.window = 22
        self.rolling = True
        # self.columnname = "Adj Close"
        self.scoremethod = "MAE"

    def fit_estimate(self, data):
        """
        This function produces the predicted return of the stock prices
        as the historical average. Default window size = 22 if rolling
        window method is applied
        Input: dataframe with date as the index, stock price as column
        Output: out-of-sample one-day-lead rolling price prediction with
                data one-business-day ahead of the input df.
        """
        df_return = data.pct_change()
        name = list(data.columns)
        obs= len(name)
        if self.rolling == True:
            # Rolling window-day-Moving average of all returns
            rolling_average = pd.DataFrame(columns=name)
            for i in range(obs):
                rolling_average[name[i]] = (
                    df_return[name[i]].rolling(window=self.window).mean()
                )
        else:
            rolling_average = df_return

        ## Rolling window average forecasting 1-business-day-ahead

        # today's price = yesterday's real price + yesterday's 22-day-rolling-averaged-return
        df_price_predicted = (1 + rolling_average.shift(periods=1)) * data.shift(
            periods=1
        )

        # Next business day as the one-day-lead forecast
        date_predicted = next_business_day(rolling_average.index[-1])
        value_predicted = (1 + rolling_average.iloc[-1]) * data.iloc[-1]
        # output = pd.DataFrame(value_predicted, index=[date_predicted], columns=data.columns)
        new_row = pd.DataFrame(
            value_predicted.values.transpose(),
            index=list(data.columns),
            columns=[date_predicted],
        ).T
        # Append the new_row to the df_price_predicted dataframe
        df_price_predicted = df_price_predicted.append(new_row)

        return df_price_predicted

    def performance(self):
        """
        Need to re-write this part
        This function produces the MAE bwtween the predicted return and the true return
        """
        """
        df_return = data.diff()
        name = list(data.columns)
        predict_return = self.fit(data)
        predict_return_match_lag = predict_return.shift(periods=1)
        method = self.scoremethod 
        if method == "MAE":
            diff = df_return-predict_return_match_lag
            output = diff.abs().mean()
        elif method == "MSE":
            diff = df_return-predict_return_match_lag
            output = diff.pow(2).mean()
        return output
        """
        pass
