from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from pandas import array
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

sample = Image.open('tiger.png')

print(type(sample))
print(sample.size)
print(sample)

# サイズの変更
size = (200, 200)
re_sample = sample.resize(size, resample=Image.LANCZOS)
# 画像の回転
rot_sample = sample.rotate(15, expand=True)
# 画像の切り出し
crop_sample = sample.crop((0, 0, 3000, 1000))
# 画像の数値データ変換
num_img = np.array(sample)
# crop_sample.save('testttttttt.png')

# fig, ax = plt.subplots()
# ax.imshow(crop_sample)
# plt.show()
