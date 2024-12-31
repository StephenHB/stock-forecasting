import pandas as pd
import pandas_datareader as web
import datetime as dt
import numpy as np


class FetchYahooFin:
    def __init__(self):

        self.site = None
        self.stock = None
        self.start = None
        self.end = None
        # self.out_data=None

    def fetch(self, stock, start="2010-01-01", end=dt.datetime.today(), site="yahoo"):
        if isinstance(stock, str):
            self.stock = [stock]
        elif isinstance(stock, list):
            self.stock = stock
        else:
            raise ("Provide Stock Quote as String or List of Strings")

        self.start = start
        self.end = end
        self.site = site

        ## Remote Data access
        try:
            df = web.DataReader(self.stock, self.site, self.start, self.end)
        except Exception as e:
            print(e)

        try:
            ## Reduce the index levels
            df.columns = ["_".join(col) for col in df.columns]
        except:
            df = None

        return df
