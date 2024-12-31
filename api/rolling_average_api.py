"""
---API Call to rolling average method


First created by SZ on Feb 25, 2021

Update Log:

"""

import sys
import os

import flask
from flask import request

sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.getcwd())
print(os.getcwd())

import import_data as imp  # pylint: disable=wrong-import-position
import rolling_average as ra  # pylint: disable=wrong-import-position

app = flask.Flask(__name__)
app.config["DEBUG"] = False


@app.route("/rolling_average", methods=["GET"])
def rolling_average():
    """Return rolling average prediction"""
    data = imp.FetchYahooFin()
    rolling_average_forecast = ra.RollingAverage()
    # adding parameters
    query_parameters = request.args
    quote = query_parameters.get("quote")
    startdate = query_parameters.get("startdate")

    data_frame = data.fetch(quote, start=startdate)
    result = rolling_average_forecast.fit_estimate(data_frame).tail(1)

    return result.to_json()


app.run()
