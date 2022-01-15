# -*- coding: utf-8 -*-
#推定に使用するライブラリ
import pandas as pd
import numpy as np
import scipy as sp

from pylab import *
from scipy import stats
import matplotlib.pyplot as plt  # プロット用
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression
import seaborn as sns
import seaborn
from pandas import DataFrame
from sklearn import linear_model, datasets
from pandas.plotting import scatter_matrix
from sklearn.tree import DecisionTreeClassifier

# 相関関係を算出するためのモジュール
from scipy.stats import kendalltau
from scipy.stats import pearsonr
from scipy.stats import spearmanr

#統計モデルを推定するライブラリ
import statsmodels.formula.api as smf
import statsmodels.api as sm
#多層パーセプトロンを適応
from sklearn.neural_network import MLPClassifier
#サンプルデータの読み込み
from sklearn.datasets import load_iris
#テストデータと訓練データを分ける
from sklearn.model_selection import train_test_split
#データの標準化を行う
from sklearn.preprocessing import StandardScaler

#グリッドサーチ
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC

# 不要なワーニングは表示に
import warnings
warnings.filterwarnings('ignore')


# file読み込み
df = pd.read_csv("test.csv", encoding="utf-8")
df.columns = ["A","B","C"]

def level_judge(ex):
    if  (-3.0 <= ex <= 3.0):
        return "OK"
    else:
        return "NG"

df.loc[:, "B判定"] = df.loc[:,"B"].apply(level_judge)
df.loc[:, "C判定"] = df.loc[:,"C"].apply(level_judge)
df.to_excel('test.xlsx')

# One-hotエンコーディング
df_b_moved = pd.get_dummies(df.loc[:, "B判定"], prefix="judgeB")
df_c_moved = pd.get_dummies(df.loc[:, "C判定"], prefix="judgeC")

df_merged = pd.concat([df, df_b_moved, df_c_moved], axis=1)

print('基本統計量')
print(df_merged.describe())
print("---------------------------")
print('相関係数')
print(df_merged.corr())
print("---------------------------")

# 散布図行列
_ = scatter_matrix(df_merged)
plt.show()

# 相関係数算出のためのデータ指定
x = df.iloc[:, 1]  # 説明変数
y = df.iloc[:, 2]  # 目的変数

correlation, pvalue = kendalltau(x, y)
print("ケンドール")
print("相関係数", correlation)
print("p値", pvalue)
print("---------------------------")

correlation2, pvalue2 = pearsonr(x, y)
print("ピアソン")
print("相関係数", correlation2)
print("p値", pvalue2)
print("---------------------------")

# 無相関検定
r, p = stats.pearsonr(x, y)
print("ピアソンの無相関検定", r,p)
print("---------------------------")

correlation3, pvalue3 = spearmanr(x, y)
print("スピアマン")
print("相関係数", correlation3)
print("p値", pvalue3)
print("---------------------------")


# 直線回帰分析
x = df[['B']].values
y = df[['C']].values
model_lr = LinearRegression()
model_lr.fit(x, y)

fig, axes = plt.subplots(5)
fig.suptitle('test')
axes[0].scatter(x, y, label='error')
axes[0].plot(x, model_lr.predict(x), linestyle="solid", label='LinearRegression')
axes[0].set_title('chamber vs Delta4 ')
axes[1].set_title('Delta4')
axes[2].set_title('chamber')
axes[0].set_xlabel('delta4 error (%)')
axes[0].set_ylabel('chamber error (%)')
axes[0].legend(loc='best')
# n, bins, patches = ax[1].hist(x['B'])
# n, bins, patches = ax[2].hist(y['C'])
axes[1].hist(x, bins=25)
axes[2].hist(y, bins=25)
axes[3].boxplot(x)
axes[4].boxplot(y)
plt.show()

y_pred = model_lr.predict(x)
print('回帰分析の結果')
print('モデル関数の回帰変数 w1: %.3f' %model_lr.coef_)
print('モデル関数の切片 w2: %.3f' %model_lr.intercept_)
print('y= %.3fx + %.3f' % (model_lr.coef_ , model_lr.intercept_))
print('決定係数 R^2： ', model_lr.score(x, y))
print("---------------------------")

#R2
from sklearn.metrics import r2_score
r2 = r2_score(y, y_pred)
print("R^2 :", r2)
print("---------------------------")

#Root Mean Squared Error (RMSE)
import numpy as np
from sklearn.metrics import mean_squared_error

rmse = np.sqrt(mean_squared_error(y, y_pred))
print("RMES :", rmse)
print("---------------------------")

#Mean Absolute Error (MAE)
from sklearn.metrics import mean_absolute_error

mae = mean_absolute_error(y, y_pred)
print("MAE :", mae)
print("---------------------------")



# 決定木
# 学習データセットとテストデータに分割する
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=123)
# 決定木をインスタンス化する (木の最大深さ=3)
tree = DecisionTreeClassifier(max_depth=3)
# 学習
tree.fit(X_train, y_train)



# yyplot 作成関数
def yyplot(y, y_pred):
    yvalues = np.concatenate([y.flatten(), y_pred.flatten()])
    ymin, ymax, yrange = np.amin(yvalues), np.amax(yvalues), np.ptp(yvalues)
    fig = plt.figure(figsize=(8, 8))
    plt.scatter(y, y_pred)
    plt.plot([ymin - yrange * 0.01, ymax + yrange * 0.01], [ymin - yrange * 0.01, ymax + yrange * 0.01])
    plt.xlim(ymin - yrange * 0.01, ymax + yrange * 0.01)
    plt.ylim(ymin - yrange * 0.01, ymax + yrange * 0.01)
    plt.xlabel('y_observed', fontsize=24)
    plt.ylabel('y_predicted', fontsize=24)
    plt.title('Observed-Predicted Plot', fontsize=24)
    plt.tick_params(labelsize=16)
    plt.show()

    return fig


# yyplot の実行例
np.random.seed(0)
y = np.random.normal(size=(10000, 1))
y_pred = y + np.random.normal(scale=0.3, size=(10000, 1))
# fig = yyplot(y, y_pred)

import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

np.random.seed(0)

# yの正解値を作成
y = np.random.normal(size=(10000, 1)).reshape(-1, 1)

# yの予測値を作成
# 正解値に異なる誤差を与えて4種類のデータを作成
y_pred_1 = y + np.random.normal(scale=0.3, size=(10000, 1))
y_pred_2 = y + np.random.laplace(scale=0.3 * (2 / np.pi) ** 0.5, size=(10000, 1))
y_pred_3 = y + np.random.uniform(low = (-0.6) * (2 / np.pi) ** 0.5,
                                     high = 0.6 * (2 / np.pi) ** 0.5,
                                     size=(10000, 1))
y_pred_4 = y + np.concatenate([np.ones((5000, 1)) * 0.3 * (2 / np.pi) ** 0.5,
                                   np.ones((5000, 1)) * (-0.3) * (2 / np.pi) ** 0.5])


# 4種類の予測値に対しyyplotを作図
yvalues = np.concatenate([y, y_pred_1, y_pred_2, y_pred_3, y_pred_4]).flatten()
ymin, ymax, yrange = np.amin(yvalues), np.amax(yvalues), np.ptp(yvalues)
f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 10))
# y_pred_1
ax1.scatter(y, y_pred_1, marker='.',
            label='RMSE : %.3f, MAE : %.3f \n RMSE/MAE = %.3f'%(
                mean_squared_error(y, y_pred_1)**0.5, mean_absolute_error(y, y_pred_1),
                mean_squared_error(y, y_pred_1)**0.5 / mean_absolute_error(y, y_pred_1)))
ax1.plot([ymin - yrange * 0.01, ymax + yrange * 0.01], [ymin - yrange * 0.01, ymax + yrange * 0.01])
ax1.legend(fontsize=12, loc='upper left')
ax1.tick_params(labelsize=10)
ax1.set_title('Normal distribution error', fontsize=15)
# y_pred_2
ax2.scatter(y, y_pred_2, marker='.',
            label='RMSE : %.3f, MAE : %.3f \n RMSE/MAE = %.3f'%(
                mean_squared_error(y, y_pred_2)**0.5, mean_absolute_error(y, y_pred_2),
                mean_squared_error(y, y_pred_2)**0.5 / mean_absolute_error(y, y_pred_2)))
ax2.plot([ymin - yrange * 0.01, ymax + yrange * 0.01], [ymin - yrange * 0.01, ymax + yrange * 0.01])
ax2.legend(fontsize=12, loc='upper left')
ax2.tick_params(labelsize=10)
ax2.set_title('Laplace distribution error', fontsize=15)
# y_pred_3
ax3.scatter(y, y_pred_3, marker='.',
            label='RMSE : %.3f, MAE : %.3f \n RMSE/MAE = %.3f'%(
                mean_squared_error(y, y_pred_3)**0.5, mean_absolute_error(y, y_pred_3),
                mean_squared_error(y, y_pred_3)**0.5 / mean_absolute_error(y, y_pred_3)))
ax3.plot([ymin - yrange * 0.01, ymax + yrange * 0.01], [ymin - yrange * 0.01, ymax + yrange * 0.01])
ax3.legend(fontsize=12, loc='upper left')
ax3.tick_params(labelsize=10)
ax3.set_title('Uniform distribution error', fontsize=15)
# y_pred_4
ax4.scatter(y, y_pred_4, marker='.',
            label='RMSE : %.3f, MAE : %.3f \n RMSE/MAE = %.3f'%(
                mean_squared_error(y, y_pred_4)**0.5, mean_absolute_error(y, y_pred_4),
                mean_squared_error(y, y_pred_4)**0.5 / mean_absolute_error(y, y_pred_4)))
ax4.plot([ymin - yrange * 0.01, ymax + yrange * 0.01], [ymin - yrange * 0.01, ymax + yrange * 0.01])
ax4.legend(fontsize=12, loc='upper left')
ax4.tick_params(labelsize=10)
ax4.set_title('Level error', fontsize=15)

# plt.xlim(ymin - yrange * 0.01, ymax + yrange * 0.01)
# plt.ylim(ymin - yrange * 0.01, ymax + yrange * 0.01)
# plt.show()


#Median Absolute Error
from sklearn.metrics import median_absolute_error

med_a_e = median_absolute_error(y, y_pred)
print("Median Absolute Error :", med_a_e)
print("---------------------------")

from sklearn.metrics import explained_variance_score

evs = explained_variance_score(y, y_pred)
print("evs :", evs)
print("---------------------------")

