"""
This module is used for summary statistics.
"""
import numpy as np
from import_data import FetchYahooFin

#### fetch data
## create an object
data_class = FetchYahooFin()

## call the method within the class
data = data_class.fetch(stock="AAPL")

#### historical analysis for log return (daily)

## calculate daily log return
data = data.assign(logret=np.log(data["Adj Close_AAPL"]).diff()) # pylint: disable = no-member

## sum stats of daily log returns
ss = data.logret.describe().to_frame().T
# sample skewness
ss["S"] = data.skew(axis=0)
# sample kurtosis
ss["K"] = data.kurt() + 3
