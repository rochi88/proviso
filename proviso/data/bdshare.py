import os
import datetime as dt
import pickle
from bdshare import get_basic_hist_data 

def get_dse_data(ticker, cache_path):
    '''
    Download data from dse, or retrieve from the cache_path if it exists
    :param ticker: The stock ticker
    :param cache_path: The cache path
    :return: The dse data
    '''
    if os.path.exists(cache_path):
        f = open(cache_path, 'rb')
        data = pickle.load(f)
        print('Loaded {} data from cache'.format(ticker))
    else:
        #end = dt.datetime.now().strftime('%Y-%m-%d')
        end = dt.datetime.now().date()
        #start = end - dt.timedelta(days=2*360)
        data = get_basic_hist_data('2008-01-01', end, ticker)
        # reverse order so newest is at end of list
        #data = data[::-1]
        if not cache_path == None:
            with open(cache_path, 'wb') as f:
                data.to_pickle(f)
                print('Cached {} data at {}'.format(ticker, cache_path))
    return data