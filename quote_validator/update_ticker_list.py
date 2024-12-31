'''
###   Stock Quote (AKA Tickers) Validation - Step 1: Maintain ticker library in storage   ###

Description:
    Update ticker library regularly to stay current, frequency of update TBD
    Estimated time required to complete update: Unknown
    Updated file will be stored on disk

First created by EL on Jan 18, 2021

Update Log:

'''


import pandas as pd
import pickle 
from sklearn.feature_extraction.text import TfidfVectorizer
import os


def _write_pickle(path,filename,file,suffix='.pickle'):
    filepath = os.path.join(path,filename+suffix)
    with open(filepath, 'wb') as handle:
        pickle.dump(file, handle, protocol=pickle.HIGHEST_PROTOCOL)

#Read in the list of quotes and company names traded
#Want to automate this in the future

class TickerLibUpdate:
    
    def __init__(self,path=None):
        
        if path is not None:
            if path.exists(path):
                self.path=path
            else:
                print("provided invalid path, using default path")
        else:
            self.path=os.path.join(os.getcwd(),'data')
        
    def read_lib(self,input_file_path,ticker_col='Symbol',name_col='Name'):
        
        df=pd.read_csv(input_file_path)
#         print(df.columns)

        company_tickers = df[ticker_col].tolist()
        company_names = df[name_col].tolist()

        _write_pickle(self.path,'company_tickers',company_tickers)  
        _write_pickle(self.path,'company_names',company_names)

        #Vectorize tickers
        vectorizer_ticker = TfidfVectorizer(min_df=1, analyzer='char_wb', ngram_range=(1,3))
        vectorizer_ticker.fit(company_tickers)
        tf_idf_matrix_ticker = vectorizer_ticker.transform(company_tickers)

        _write_pickle(self.path,'vectorizer_ticker',vectorizer_ticker)  
        _write_pickle(self.path,'tf_idf_matrix_ticker',tf_idf_matrix_ticker)
#         with open('vectorizer_ticker.pickle', 'wb') as handle:
#             pickle.dump(vectorizer_ticker, handle, protocol=pickle.HIGHEST_PROTOCOL)
#         with open('tf_idf_matrix_ticker.pickle', 'wb') as handle:
#             pickle.dump(tf_idf_matrix_ticker, handle, protocol=pickle.HIGHEST_PROTOCOL)


        #Vectorize company names 
        vectorizer_names = TfidfVectorizer(min_df=1, analyzer='char_wb', ngram_range=(3,3))
        vectorizer_names.fit(company_names)
        tf_idf_matrix_names = vectorizer_names.transform(company_names)
        
        _write_pickle(self.path,'vectorizer_names',vectorizer_names)  
        _write_pickle(self.path,'tf_idf_matrix_names',tf_idf_matrix_names)
#         with open('vectorizer_names.pickle', 'wb') as handle:
#             pickle.dump(vectorizer_names, handle, protocol=pickle.HIGHEST_PROTOCOL)

#         with open('tf_idf_matrix_names.pickle', 'wb') as handle:
#             pickle.dump(tf_idf_matrix_names, handle, protocol=pickle.HIGHEST_PROTOCOL)

    #End


# ticker_updator=TickerLibUpdate()
# ticker_updator.read_lib("C:\\Users\\erin_\\Downloads\\nasdaq_screener_1610744879725.csv") 
