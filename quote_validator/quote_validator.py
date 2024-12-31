"""
---Stock Quote (AKA Tickers) Validation - quote matching---

Description:
    Compare user input quote with a valid list of quotes. Make suggestions to user of valid quotes.
    Return True when user input quote is valid, ie. exact match to valid list of quotes

Usage:
    import quote_validator as qv

    #Instantiate QuateValidator
    ticker_matcher = qv.QuoteValidator()

    #Load files to query from (required when instantiated)
    ticker_matcher.load()

    #return similar quetes to sting entered
    ticker_matcher.match('string of quote to look up')

First created by EL on Jan 18, 2021

Update Log:

"""

import pickle
import os
import numpy as np
from sparse_dot_topn import awesome_cossim_topn

def _get_non_zero_entries(sparse_matrix):
    non_zeros = sparse_matrix.nonzero()
    sparserows = non_zeros[1]

    return list(sparserows)


def _stack_rows_nodup(list_of_rows):
    assert isinstance(list_of_rows, list)

    all_rows = []
    for rows in list_of_rows:
        all_rows = all_rows + rows

    seen = set()

    return [x for x in all_rows if x not in seen and not seen.add(x)]


def _get_matches(matched_rows, ticker_vector, name_vector, top=5):

    sparserows = matched_rows

    if top <= len(sparserows):
        nr_matches = top
    else:
        nr_matches = len(sparserows)

    tickers = np.empty([nr_matches], dtype=object)
    names = np.empty([nr_matches], dtype=object)

    for index in range(0, nr_matches):
        tickers[index] = ticker_vector[sparserows[index]]
        names[index] = (
            ticker_vector[sparserows[index]] + ": " + name_vector[sparserows[index]]
        )

    return tickers.tolist(), names.tolist()


def _read_pickle(path, file):
    filepath = os.path.join(path, file)
    with open(filepath, "rb") as handle:
        return pickle.load(handle)


class QuoteValidator:
    '''
    ---Stock Quote (AKA Tickers) Validation - quote matching---

    Description:
        Compare user input quote with a valid list of quotes. Make suggestions of valid quotes.
        Return True when user input quote is valid, ie. exact match to valid list of quotes
    '''
    def __init__(self):
        self.company_tickers = None
        self.company_names = None
        self.vectorizer_names = None
        self.vectorizer_ticker = None
        self.tf_idf_matrix_names = None
        self.tf_idf_matrix_ticker = None
        self.unloaded = True


    def load(self, filepath=None):
        '''
        Load Ticker Library and keep in memory after user reached the "search quote" page
        Estimated time required to load on memory: 0.2sec
        Should persist in memory as long as user stays on "search quote" page

        Usage:
            load(filepath=YourPathToFiles)
        '''

        # Verify filepath
        # Define default path
        list_of_paths=[]
        list_of_paths.append([os.getcwd(), "data"])
        list_of_paths.append([os.getcwd(), "quote_validator", "data"])
        list_of_paths.append([os.path.dirname(os.getcwd()), "quote_validator", "data"])

        for pth in list_of_paths:
            filedir = os.path.join(*pth)

            if os.path.exists(filedir):
                break

        # Check if path valid
        if not os.path.exists(filedir):
            raise "filepath not exist, please provide valid path to quote name files"

        if filepath is not None:
            # Use user provided path
            if os.path.exists(filepath):
                filedir = filepath
            else:
                print("provided invalid filepath, using default path")

        # Load ticker library and pre-fitted encoder
        try:
            self.company_tickers = _read_pickle(filedir, "company_tickers.pickle")
            self.company_names = _read_pickle(filedir, "company_names.pickle")
            self.vectorizer_ticker = _read_pickle(
                filedir, "vectorizer_ticker.pickle"
            )
            self.vectorizer_names = _read_pickle(
                filedir, "vectorizer_names.pickle"
            )
            self.tf_idf_matrix_ticker = _read_pickle(
                filedir, "tf_idf_matrix_ticker.pickle"
            )
            self.tf_idf_matrix_names = _read_pickle(
                filedir, "tf_idf_matrix_names.pickle"
            )

            self.unloaded = False
        except: # pylint: disable=bare-except
            print("Failed to load. Check if all ticker files exist")


    def match(self, ticker_input):
        '''
        Vectorize User input and compare with ticker library
        Estimated time required to match: 0.1sec

        Usage:
            match("string to match")
        '''
        if self.unloaded:
            print("Run QuoteValidator.load() to load ticker library first")
            return None

        tf_idf_input_ticker = self.vectorizer_ticker.transform([ticker_input])
        tf_idf_input_names = self.vectorizer_names.transform([ticker_input])

        #Use standard implementation
        # c = awesome_cossim_topn(tf_idf_matrix, tf_idf_input, N, 0.01)

        #Use parallel implementation with 4 threads
        sparse_matrix_logic1 = awesome_cossim_topn(
            tf_idf_input_ticker,
            self.tf_idf_matrix_ticker.T,
            3,
            0.1,
            use_threads=True,
            n_jobs=4,
        )
        sparse_matrix_logic2 = awesome_cossim_topn(
            tf_idf_input_names,
            self.tf_idf_matrix_names.T,
            3,
            0.1,
            use_threads=True,
            n_jobs=4,
        )

        rows1 = _get_non_zero_entries(sparse_matrix_logic1)
        rows2 = _get_non_zero_entries(sparse_matrix_logic2)

        matches = _stack_rows_nodup([rows1, rows2])

        matched_tickers, matched_names = _get_matches(
            matches, self.company_tickers, self.company_names, top=5
        )

        return matched_tickers, matched_names

    def validate(self, ticker_input):
        '''
        Validate ticker_input
        Return True if exact match but not case sensitive
        '''

        # if ticker_input.upper() in self.company_tickers:
        #     return True
        # else:
        #     return False
        validated = bool(ticker_input.upper() in self.company_tickers)
        return validated


# End of Script

# import time
# t = time.time()-t1
# print("SELFTIMED vectorize:", t)
# t1 = time.time()
