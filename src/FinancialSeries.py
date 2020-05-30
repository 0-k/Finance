import pandas as pd
import yfinance as yt
import numpy as np
import matplotlib.pyplot as plt


class FinancialSeries:

    def __init__(self, ticker: str, name: str = None, start_date: str = '2004-01-01'):
        self.ticker = ticker
        self.closing_values = None
        self.name = name
        self.start_date = start_date

    def fetch(self, use_cached_values_if_possible=True):
        if use_cached_values_if_possible:
            self.__fetch_cached()
        if self.closing_values is None:
            self.__fetch_online()
            self.__set_name()
            self.__cache()
        return self.closing_values

    def __fetch_cached(self):
        try:
            self.closing_values = pd.read_hdf('../data/cached/tickers/{}.h5'.format(self.ticker))  #
            return self.closing_values
        except:
            print('Could not load cached {}, will fetch data online'.format(self.ticker))

    def __fetch_online(self):
        try:
            ticker = yt.Ticker(self.ticker)
            self.closing_values = ticker.history(start=self.start_date).Close
            return self.closing_values
        except:
            print('Warning: Could not fetch ' + self.ticker + ' from online sources.')

    def __set_name(self):
        if self.name is None:
            self.name = self.ticker
        self.closing_values.rename(self.name, inplace=True)

    def __cache(self):
        try:
            self.closing_values.to_hdf('../data/cached/tickers/{}.h5'.format(self.ticker), key='data')
        except:
            print('Warning: Failed to cache online values.')

    def plot(self):
        if self.closing_values is not None:
            plt.plot(self.closing_values)
            plt.show()

    def print(self):
        print(self.closing_values)


if __name__ == '__main__':
    f = FinancialSeries()
    f.fetch()
    f.print()
    f.plot()
