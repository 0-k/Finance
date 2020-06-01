import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.DataCollection import DataCollection
from config.config import Config


class TrainingData:

    def __init__(self):
        self.values = None
        self.columns = Config.columns
        self.data_collections = None
        self.is_prepared = False

    def load(self, use_cached_values_if_possible=True):
        if use_cached_values_if_possible:
            self.__load_cached()
        if self.values is None:
            self.__load_data_collections()
            self.__cache()
        return self.values

    def __load_cached(self):
        try:
            self.values = pd.read_hdf('../data/cached/training/training_data.h5')
            self.is_prepared = True
        except FileNotFoundError:
            self.values = None
        return self.values

    def __load_data_collections(self):
        self.values = pd.DataFrame()
        if self.data_collections is None:
            raise ValueError('Data collections need to be set first.')
        for collection in self.data_collections:
            self.values = pd.concat([self.values, collection], axis=1)

    def __cache(self):
        try:
            self.values.to_hdf('../data/cached/training/training_data.h5', key='data')
        except:
            print('Warning: Failed to cache training data values.')

    def prepare(self, is_relative=True):
        if self.is_prepared:
            print('all done already')
            return
        self.__drop_NA_SP500()
        self.__fill_NA_other_series()
        self.__calc_changes()
        self.__make_target_row()
        self.__remove_remaining_NA()
        self.__cache()
        self.is_prepared = True

    def __drop_NA_SP500(self):
        self.values = self.values.dropna(subset=['SP_500'])

    def __fill_NA_other_series(self):
        self.values.fillna(method='ffill', inplace=True)

    def __calc_changes(self):
        for column in self.columns:
            if self.columns[column] == 'PCT':
                self.values[column] = self.values[column].pct_change()
            elif self.columns[column] == 'DIFF':
                self.values[column] = self.values[column].diff()
            else:
                raise ValueError('Could not retrieve column type for ' + column)

    def __make_target_row(self):
        self.values['Target'] = self.values['SP_500'].shift(-1)
        self.values.loc[self.values.Target <= 0, 'Target'] = 0
        self.values.loc[self.values.Target > 0, 'Target'] = 1

    def __remove_remaining_NA(self):
        self.values.dropna(inplace=True)


def prepare_training_data():


    t = TrainingData()
    indices = DataCollection(collect=Config.indices, name='indices').load()
    commodities = DataCollection(collect=Config.commodities, name='commodities').load()
    currencies = DataCollection(collect=Config.currencies, name='currencies').load()
    treasuries = DataCollection(collect=Config.treasuries, name='treasuries').load()
    t.data_collections = [indices, commodities, currencies, treasuries]
    t.load()
    t.prepare()
    print(t.values)

if __name__ == '__main__':
    prepare_training_data()
