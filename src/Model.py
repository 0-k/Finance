#import pandas as pd
import numpy as np
from src.TrainingData import TrainingData
import tensorflow as tf


class Model:

    def __init__(self):
        self.data = None
        self.model = None


    def initialize(self):
        self.data = TrainingData()
        self.data.load()
        self.data.normalize()
        self.data.split(size_training_data=0.71)

    def initialize_test(self):
        self.data = TrainingData(is_testing=True)
        self.data.load()
        self.data.normalize()
        self.data.split(size_training_data=0.71)

    def format_targets(self):
        self.data.training_targets = self.data.training.pop('Target').astype('int64')
        self.data.validation_targets = self.data.validation.pop('Target').astype('int64')
        self.data.test_targets = self.data.test.pop('Target').astype('int64')

    def get_compiled_model(self):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(30, activation='relu'),
            tf.keras.layers.Dropout(rate=0.1),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dropout(rate=0.1),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(16, activation='relu'),

            tf.keras.layers.Dense(8, activation='relu'),
            tf.keras.layers.Dense(1, activation ='sigmoid')
        ])
        #optimizer = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.0, nesterov=False, name='SGD')
        self.model.compile(optimizer='adam',
                      loss=tf.keras.losses.MeanSquaredError(reduction='sum'),
                      metrics=['accuracy'])
        return self.model

    def run(self):
        training_dataset = tf.data.Dataset.from_tensor_slices((self.data.training.values, self.data.training_targets.values))
        training_dataset = training_dataset.batch(1)
        validation_dataset = tf.data.Dataset.from_tensor_slices((self.data.validation.values, self.data.validation_targets.values))
        validation_dataset = validation_dataset.batch(1)

        self.model = self.get_compiled_model()
        self.model.fit(training_dataset, epochs=2)
        loss, accuracy = self.model.evaluate(validation_dataset, verbose=2)
        return loss, accuracy

    def run_actual_model(self):
        self.initialize()
        self.format_targets()
        loss, accuracy = self.run()
        return accuracy

    def run_test_model(self):
        self.initialize_test()
        self.format_targets()
        loss, accuracy = self.run()
        return accuracy

if __name__ == '__main__':
    m = Model()
    #m.run_test_model()
    m.run_actual_model()

