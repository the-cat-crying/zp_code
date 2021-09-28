import tensorflow as tf
import numpy as np
from tensorflow import keras
import matplotlib as plt
from tensorflow.keras import layers, Sequential, metrics, optimizers
from tensorflow import keras


class BasicBlock(layers.Layer):
    def __init__(self, filter_num, stride=1):
        super(BasicBlock, self).__init__()
        self.conv1 = layers.Conv2D(filter_num, (3, 3), strides=stride, padding='same')
        self.bn1 = layers.BatchNormalization()
        self.relu1 = layers.Activation('relu')

        self.conv2 = layers.Conv2D(filter_num, (3, 3), strides=1, padding='same')
        self.bn2 = layers.BatchNormalization()

        if stride != 1:
            self.down_sample = Sequential()
            self.down_sample.add(layers.Conv2D(filter_num, (1, 1), strides=stride))
        else:
            self.down_sample = lambda x: x

    def call(self, inputs_call, training=None):
        out = self.conv1(inputs_call)
        out = self.bn1(out)
        out = self.relu1(out)

        out = self.conv2(out)
        out = self.bn2(out)

        identity = self.down_sample(inputs_call)

        output = layers.add([out, identity])
        output = tf.nn.relu(output)

        return output

    def build_block(self, filter_, blocks, stride=1):
        res_blocks = Sequential()
        res_blocks.add(BasicBlock(filter_, stride))

        for _ in range(1, blocks):
            res_blocks.add(BasicBlock(filter_, stride=1))

        return res_blocks


class ResNet(keras.Model):
    def __init__(self, layer_dims, num_classes=10):
        super(ResNet, self).__init__()

        self.stem = Sequential([
            layers.Conv2D(64, (3, 3), strides=(1, 1)),
            layers.BatchNormalization(),
            layers.Activation('relu'),
            layers.MaxPool2D(pool_size=(2, 2), strides=(1, 1), padding='same')
        ])
