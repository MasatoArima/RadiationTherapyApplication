
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

# 目的変数の加工処理で必要なライブラリ
from keras.utils.np_utils import to_categorical

# warningを表示させない
warnings.simplefilter('ignore')

# データ読み込み
from keras.datasets import mnist
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# 画像を1次元化
X_train = X_train.reshape(60000, 784)
X_test = X_test.reshape(10000, 784)

# 画素を0~1の範囲に変換(正規化)
X_train = X_train.astype('float32') / 255
X_test = X_test.astype('float32') / 255

# 正解ラベルをone-hot-encoding
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

from keras.models import Sequential
print(Sequential)
from keras.layers import Dense
print(Dense)

model = Sequential()
image_size = 784
model.add(Dense(32, activation='sigmoid', input_dim=image_size))
model.summary()

num_classes = 10
model.add(Dense(num_classes, activation='softmax'))
model.summary()

model.compile(optimizer='sgd',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(X_train, y_train)
history = model.fit(X_train, y_train,epochs=4)
history = model.fit(X_train, y_train,epochs=4, batch_size=100)