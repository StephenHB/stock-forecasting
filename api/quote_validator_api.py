'''
---API Call to Stock Quote (AKA Tickers) Validation - quote matching---


First created by EL on Feb 24, 2021

Update Log:

'''

import sys
import os

import flask
from flask import jsonify, request

sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.getcwd())
print(os.getcwd())
import quote_validator.quote_validator as qv # pylint: disable=wrong-import-position


app = flask.Flask(__name__)
app.config["DEBUG"] = False


@app.route("/stock", methods=["GET"])
def stock():
    '''Return stock query results as json'''
    ticker_matcher = qv.QuoteValidator()
    ticker_matcher.load(
        filepath=os.path.join(os.getcwd(), "quote_validator", "data")
    )

    query_parameters = request.args
    quote = query_parameters.get('quote')

    result = ticker_matcher.match(quote)
    return jsonify(result)


app.run()
