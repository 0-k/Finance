import pandas as pd
from src.DataCollection import DataCollection
from config.config import Config
from sklearn import preprocessing
import matplotlib.pyplot as plt

class TrainingData:

    def __init__(self, is_testing=False):
        self.values = None
        self.columns = Config.columns
        self.data_collections = None
        self.is_prepared = False
        self.training = None
        self.validation = None
        self.test = None
        self.random_number_seed = 3255087
        self.new_normalization_method = True
        self.is_testing = is_testing

    def load(self, use_cached_values_if_possible=True):
        if self.is_testing:
            self.__load_test()
            return
        if use_cached_values_if_possible:
            self.__load_cached()
        if self.values is None:
            self.__load_data_collections()
            self.__cache()
        return self.values

    def __load_test(self):
        self.values = pd.read_csv('../data/cached/training/training_data_test.csv', sep=';', header=0, decimal=',')
        self.is_prepared = True
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
        if self.values is None:
            raise ValueError('Training data empty.')
        self.values.to_hdf('../data/cached/training/training_data.h5', key='data')

    def prepare(self):
        if self.is_prepared:
            return
        self.__drop_NA_SP500()
        self.__fill_NA_other_series()
        self.__calc_changes()
        self.__make_target_row()
        self.__drop_NA_remaining()
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


        self.values.loc[self.values['Target'] >= 0.03, 'Target'] = 7
        self.values.loc[(self.values['Target'] >= 0.02) & (self.values['Target'] < 0.03), 'Target'] = 6
        self.values.loc[(self.values['Target'] >= 0.005) & (self.values['Target'] < 0.02), 'Target'] = 5
        self.values.loc[(self.values['Target'] >= 0.002) & (self.values['Target'] < 0.005), 'Target'] = 4
        self.values.loc[(self.values['Target'] >= -0.002) & (self.values['Target'] < 0.002), 'Target'] = 3
        self.values.loc[(self.values['Target'] >= -0.005) & (self.values['Target'] < -0.002), 'Target'] = 2
        self.values.loc[(self.values['Target'] >= -0.02) & (self.values['Target'] < -0.005), 'Target'] = 1
        self.values.loc[self.values['Target'] < -0.02, 'Target'] = 0

        #self.values.loc[self.values.Target <= 0, 'Target'] = 0
        #self.values.loc[self.values.Target > 0, 'Target'] = 1



    def __drop_NA_remaining(self):
        self.values.dropna(inplace=True)

    def normalize(self):
        if self.new_normalization_method:
            if self.is_testing:
                data = self.values
            else:
                data = self.values.truncate(after=pd.Timestamp('2019-12-31'))
            targets = data['Target']
            data = data.drop(['Target'], axis=1)
            x = data.values  # returns a numpy array
            x_scaled = preprocessing.normalize(x)
            self.values = pd.DataFrame(x_scaled)
            targets = targets.reset_index(drop=True)
            self.values['Target'] = targets
            """
            print('jelllo')
            self.values.loc[self.values['Target'] >= 0.06, 'Target'] = 7
            self.values.loc[(self.values['Target'] >= 0.04) & (self.values['Target'] < 0.06), 'Target'] = 6
            self.values.loc[(self.values['Target'] >= 0.02) & (self.values['Target'] < 0.04), 'Target'] = 5
            self.values.loc[(self.values['Target'] >= 0.005) & (self.values['Target'] < 0.02), 'Target'] = 4
            self.values.loc[(self.values['Target'] >= -0.005) & (self.values['Target'] < 0.005), 'Target'] = 3
            self.values.loc[(self.values['Target'] >= -0.02) & (self.values['Target'] < -0.005), 'Target'] = 2
            self.values.loc[(self.values['Target'] >= -0.04) & (self.values['Target'] < -0.02), 'Target'] = 1
            self.values.loc[self.values['Target'] < -0.04, 'Target'] = 0
            """

            #self.values.loc[self.values.Target <= 0, 'Target'] = 0
            #self.values.loc[self.values.Target > 0, 'Target'] = 1
        else:
            if self.is_testing:
                data = self.values
            else:
                data = self.values.truncate(after=pd.Timestamp('2019-12-31'))
            data.loc[data['Target'] <= 0, 'Target'] = 0
            data.loc[data['Target'] > 0, 'Target'] = 1

    def split(self, size_training_data=0.5):
        if (size_training_data <= 0) or (size_training_data >= 0.8):
            raise ValueError('Relative size of training data must be larger than 0 and smaller than 0.8')
        if not self.is_prepared:
            raise BrokenPipeError('Training data needs to be prepared first.')
        data = self.values
        self.test = data.sample(frac=0.2, random_state=self.random_number_seed)
        data_rest = data.drop(self.test.index)
        self.training = data_rest.sample(frac=size_training_data, random_state=self.random_number_seed)
        self.validation = data_rest.drop(self.training.index)


def prepare_training_data():
    t = TrainingData()
    indices = DataCollection(collect=Config.indices, name='indices').load()
    commodities = DataCollection(collect=Config.commodities, name='commodities').load()
    currencies = DataCollection(collect=Config.currencies, name='currencies').load()
    treasuries = DataCollection(collect=Config.treasuries, name='treasuries').load()
    t.data_collections = [indices, commodities, currencies, treasuries]
    t.load(use_cached_values_if_possible=False)
    t.prepare()
    t.normalize()
    t.split()


if __name__ == '__main__':
    prepare_training_data()
