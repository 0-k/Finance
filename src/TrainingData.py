import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.FinancialSeries import FinancialSeries
from config.config import Config


class TrainingData:

    def __init__(self, dataset=Config.indices, name='indices'):
        self.values = None
        self.dataset = dataset
        self.name = name

    def load(self, use_cached_values_if_possible=True):
        if use_cached_values_if_possible:
            self.__load_cached()
        if self.values is None:
            self.__load_series()
            self.__cache()
        return self.values

    def __load_cached(self):
        if self.name is not None:
            try:
                self.values = pd.read_hdf('../data/cached/training/training_data_{}.h5'.format(self.name))
                return self.values
            except:
                print('Warning: Failed to load cached data, will fetch data.')
        else:
            try:
                self.values = pd.read_hdf('../data/cached/training/training_data.h5')
                return self.values
            except:
                print('Warning: Failed to load cached data, will fetch data.')

    def __load_series(self):
        self.values = pd.DataFrame()
        for key in self.dataset:
            try:
                ticker = self.dataset[key]
                series = FinancialSeries(ticker=ticker, name=key).fetch()
                self.values = pd.concat([self.values, series], axis=1)
            except:
                print('Loading of series {} unsuccessful.'.format(key))
        return self.values

    def __cache(self):
        if self.name is not None:
            try:
                self.values.to_hdf('../data/cached/training/training_data_{}.h5'.format(self.name), key='data')
            except:
                print('Warning: Failed to cache training data values.')
        else:
            try:
                self.values.to_hdf('../data/cached/training/training_data.h5', key='data')
            except:
                print('Warning: Failed to cache training data values.')

    def prepare(self, is_relative=True):
        self.values.fillna(method='ffill', inplace=True)
        if is_relative:
            self.values = self.values.pct_change()
        else:
            self.values = self.values.diff()

    def consolidate(self, _with):
        self.name = None
        self.values = pd.concat([self.values, _with.values], axis=1)
        self.values.dropna(inplace=True)
        self.__cache()
        return self.values

    def __str__(self):
        return self.values


def prepare_training_data():
    indices = TrainingData(dataset=Config.indices, name='indices')
    indices.load()
    indices.prepare()

    treasuries = TrainingData(dataset=Config.treasuries, name='treasuries')
    treasuries.load()
    treasuries.prepare(is_relative=False)
    indices.consolidate(_with=treasuries)


if __name__ == '__main__':
    full_training_data = TrainingData(name=None)
    full_training_data.load()
    plt.plot(full_training_data.values)
    plt.show()
