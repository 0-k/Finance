import pandas as pd
import yfinance as yt
import numpy as np
import matplotlib.pyplot as plt


class FinancialSeries:

    def __init__(self, ticker: str, name: str = None, start_date: str = '2003-07-01'):
        self.ticker = ticker
        self.closing_values = None
        self.name = name
        self.start_date = start_date

    def fetch(self, use_cached_values_if_possible=True):
        if use_cached_values_if_possible:
            self.__fetch_cached()
        if self.closing_values is None:
            self.__fetch_online()
            self.__cache()
        return None

    def __fetch_cached(self):
        try:
            self.closing_values = pd.read_hdf('../data/cached/{}.h5'.format(self.ticker))  #
            return self.closing_values
        except:
            print('Warning: Failed to load cached data, will fetch data online')

    def __fetch_online(self):
        try:
            ticker = yt.Ticker(self.ticker)
            self.closing_values = ticker.history(start=self.start_date).Close
            print(self.closing_values)
            return self.closing_values
        except:
            print('Warning: Could not fetch ' + self.ticker + ' from online sources.')

    def __cache(self):
        try:
            self.closing_values.to_hdf('../data/cached/{}.h5'.format(self.ticker), key='data')
        except:
            print('Warning: Failed to cache online values.')

    def plot(self):
        if self.closing_values is not None:
            plt.plot(self.closing_values)
            plt.show()


if __name__ == '__main__':
    f = FinancialSeries('GOOGL')
    f.fetch()
    f.plot()
