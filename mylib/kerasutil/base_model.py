import os
import keras
import matplotlib.pyplot as plt
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
import numpy as np


@dataclass()
class BaseContext(metaclass=ABCMeta):
    split_rate: float = 0.3
    batch_size: int = 300
    epochs: int = 100
    validation_split: float = 0.1
    activation = 'linear'
    loss = 'mean_squared_error'
    optimizer = 'adam'
    metrics = ['mae', 'acc']
    tensor_board_dir: str = './dat/tensorboard'
    model_dir: str = './dat/model'
    model_name: str = 'model.json'
    weight_name: str = 'weight.hdf5'



class BaseModel(metaclass=ABCMeta):

    def __init__(self, context):
        self.context = context

    @abstractmethod
    def preprocess(self, ndarr):
        pass

    def test_split(self, X, y):
        from sklearn.model_selection import train_test_split
        return train_test_split(X, y, test_size=self.context.split_rate)

    def save2file(self, model: keras.models.Model):
        model_json = model.to_json()
        with open(os.path.join(self.context.model_dir, self.context.model_name), 'w') as f:
            f.write(model_json)
        model.save_weights(os.path.join(self.context.model_dir, self.context.weight_name))


    def loadModelFfile(self):
        with open(os.path.join(self.context.model_dir, self.context.model_name)) as f:
            model_json = f.read()
        model: keras.models.Model = keras.models.model_from_json(model_json)
        model.summary()
        model.compile(loss=self.context.loss,
                      optimizer=self.context.optimizer,
                      metrics=self.context.metrics)
        model.load_weights(os.path.join(self.context.model_dir, self.context.weight_name))
        return model

    def plot2image(self, buffer, dim= 0):
        import tensorflow as tf
        image = tf.image.decode_png(buffer.getvalue(), channels=4)
        image = tf.expand_dims(image, dim)
        return image

    def add_image2board(self, name, image, step=0):
        import tensorflow as tf
        writer = tf.summary.create_file_writer(self.context.tensor_board_dir)
        with writer.as_default():
            tf.summary.image(name, image, step=step)
            writer.flush()