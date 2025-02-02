import pandas as pd
import yfinance as yt
import matplotlib.pyplot as plt


class FinancialSeries:

    def __init__(self, ticker: str, name: str = None, start_date: str = '2004-01-01'):
        self.ticker = ticker
        self.values = None
        self.name = name
        self.start_date = start_date

    def fetch(self, use_cached_values_if_possible=True):
        if use_cached_values_if_possible:
            self.__fetch_cached()
        if self.values is None:
            self.__fetch_online()
            self.__set_name()
            self.__cache()
        return self.values

    def __fetch_cached(self):
        try:
            self.values = pd.read_hdf('../data/cached/tickers/{}.h5'.format(self.ticker))  #
        except FileNotFoundError:
            self.values = None
            print('Could not load cached {}, will fetch data online'.format(self.ticker))
        return self.values

    def __fetch_online(self):
        try:
            ticker = yt.Ticker(self.ticker)
            self.values = ticker.history(start=self.start_date).Close
            return self.values
        except:
            print('Warning: Could not fetch ' + self.ticker + ' from online sources.')

    def __set_name(self):
        if self.name is None:
            self.name = self.ticker
        self.values.rename(self.name, inplace=True)

    def __cache(self):
        if self.values is None:
            print('Warning: Financial series is empty. Could not store values. Online retrieval probably failed.')
            return
        self.values.to_hdf('../data/cached/tickers/{}.h5'.format(self.ticker), key='data')

    def plot(self):
        if self.values is not None:
            plt.plot(self.values)
            plt.show()
        else:
            print('Warning: Could not plot values.')

    def print(self):
        print(self.values)


if __name__ == '__main__':
    f = FinancialSeries('GOOGL')
    f.fetch()
    f.print()
    f.plot()
