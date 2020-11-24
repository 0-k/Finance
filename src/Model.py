import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras import initializers
import tensorflow.keras.backend as kb
import numpy as np
import math

from src.TrainingData import TrainingData


class Model:

    def __init__(self):
        self.data = None
        self.model = None
        self.training_dataset = None
        self.validation_dataset = None
        self.test_dataset = None

    def run(self, is_testing=False):
        self.__initialize(is_testing)
        self.__format_targets()
        self.__prepare_data()
        self.compile()
        self.model.fit(self.training_dataset, epochs=50)
        loss, accuracy = self.model.evaluate(self.validation_dataset, verbose=2)
        predictions = self.model.predict(self.validation_dataset, verbose=2)
        labelx = np.zeros(1288)
        predictionx = np.zeros(1288)
        idx = 0
        for images, labels in self.validation_dataset.take(1288):
            labelx[idx] = labels.numpy()[0]
            idx += 1
        idx = 0
        for row in predictions:
            predictionx[idx] = np.argmax(row)
            idx += 1
        plt.hist(predictionx, bins=8)
        plt.show()
        matrix = tf.math.confusion_matrix(
            labels=labelx, predictions=predictionx, num_classes=None, weights=None, dtype=tf.dtypes.int32,
            name=None
        )
        plt.imshow(matrix)
        plt.show()
        plt.show(predictionx)
        plt.show()
        return loss, accuracy

    def custom_loss(self, y_actual, y_pred):
        return kb.abs(y_actual - y_pred)

    def __initialize(self, is_testing):
        self.data = TrainingData(is_testing)
        self.data.load()
        self.data.normalize()
        self.data.split(size_training_data=0.6)

    def __format_targets(self):
        self.data.training_targets = self.data.training.pop('Target').astype('int64')
        self.data.validation_targets = self.data.validation.pop('Target').astype('int64')
        self.data.test_targets = self.data.test.pop('Target').astype('int64')

    def __prepare_data(self):
        training_dataset = tf.data.Dataset.from_tensor_slices((self.data.training.values, self.data.training_targets.values))
        self.training_dataset = training_dataset.batch(1)
        for feat, targ in self.training_dataset.take(20):
            print('Features: {}, Target: {}'.format(feat, targ))

        validation_dataset = tf.data.Dataset.from_tensor_slices((self.data.validation.values, self.data.validation_targets.values))
        self.validation_dataset = validation_dataset.batch(1)
        print(type(self.validation_dataset))
        test_dataset = tf.data.Dataset.from_tensor_slices((self.data.test.values, self.data.test_targets.values))
        self.test_dataset = test_dataset.batch(1)

    def compile(self):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(30, activation='relu'),#, kernel_initializer=initializers.RandomNormal(stddev=0.01)),
            tf.keras.layers.Dropout(rate=0.3),
            tf.keras.layers.Dense(15, activation='relu'),
            tf.keras.layers.Dropout(rate=0.3),
            tf.keras.layers.Dense(8, activation='relu')
        ])
        self.model.compile(optimizer='adam',
                      loss=self.custom_loss, #loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy'])


if __name__ == '__main__':
    m = Model()
    m.run(is_testing=False)

