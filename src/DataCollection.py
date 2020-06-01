import pandas as pd
from src.FinancialSeries import FinancialSeries
from config.config import Config


class DataCollection:

    def __init__(self, collect=Config.indices, name='indices'):
        self.values = None
        self.collection = collect
        self.name = name

    def load(self, use_cached_values_if_possible=True):
        if use_cached_values_if_possible:
            self.__load_cached()
        if self.values is None:
            self.__load_series()
            self.__cache()
        return self.values

    def __load_cached(self):
        if self.name is None:
            raise NameError('No data collection name was given.')
        try:
            self.values = pd.read_hdf('../data/cached/training/data_collection_{}.h5'.format(self.name))
        except FileNotFoundError:
            self.values = None
        return self.values

    def __load_series(self):
        self.values = pd.DataFrame()
        for key in self.collection:
            try:
                ticker = self.collection[key]
                series = FinancialSeries(ticker=ticker, name=key).fetch()
                self.values = pd.concat([self.values, series], axis=1)
            except:
                print('Loading of series {} unsuccessful.'.format(key))
        return self.values

    def __cache(self):
        if self.name is None:
            raise NameError('No data collection name was given.')
        if self.values is None:
            raise ValueError('Data collection empty.')
        self.values.to_hdf('../data/cached/training/data_collection_{}.h5'.format(self.name), key='data')


def prepare_data_collections():
    indices = DataCollection(collect=Config.indices, name='indices').load()
    commodities = DataCollection(collect=Config.commodities, name='commodities').load()
    currencies = DataCollection(collect=Config.currencies, name='currencies').load()
    treasuries = DataCollection(collect=Config.treasuries, name='treasuries').load()


if __name__ == '__main__':
    prepare_data_collections()
