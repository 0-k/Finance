import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.FinancialSeries import FinancialSeries
from config.config import Config


class TrainingData:

    def __init__(self):
        self.values = None

    def load(self, use_cached_values_if_possible=True):
        if use_cached_values_if_possible:
            self.__load_cached()
        if self.values is None:
            self.__load_series()
            self.__cache()
        return self.values

    def __load_cached(self):
        try:
            self.values = pd.read_hdf('../data/cached/training/training_data.h5')
            return self.values
        except:
            print('Warning: Failed to load cached data, will fetch data online')

    def __load_series(self):
        self.values = pd.DataFrame()
        for name in Config.indicators:
            try:
                ticker = Config.indicators[name]
                series = FinancialSeries(ticker=ticker, name=name).fetch()
                self.values = pd.concat([self.values, series], axis=1)
            except:
                print('Loading of series {} unsuccessful.'.format(name))
        return self.values

    def __cache(self):
        try:
            self.values.to_hdf('../data/cached/training/training_data.h5', key='data')
        except:
            print('Warning: Failed to cache training data values.')

    def print(self):
        print(self.values)


t = TrainingData()
t.load()
t.print()