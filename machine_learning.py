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
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

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

def level_judge(ex):
    if  (-1.0 <= ex <= 1.0):
        return 1
    else:
        return 0

df.loc[:,"error1or0"] = df.loc[:,"error"].apply(level_judge)
df.to_excel('test.xlsx')



# One-hotエンコーディング
df_b_moved = pd.get_dummies(df.loc[:, "判定"], prefix="judge")
df_merged = pd.concat([df, df_b_moved], axis=1)

# 各カラムのデータ型を確認
df_merged.dtypes

# object型のデータを削除
df_merged_except_object = df_merged.select_dtypes(['int64','float64'])
df_merged_except_object.isnull().sum()
df_merged_except_object.isnull().any()
# 欠損値を確認して、欠損値があった場合、fillna()メソッド等で補間や削除を行う

print('基本統計量')
print(df_merged_except_object.describe())
print("---------------------------")
print('相関係数')
print(df_merged_except_object.corr())
print("---------------------------")

# jupter表示の際にヒートマップで表示
df_merged_except_object.corr().style.background_gradient(axis=None)

# 散布図行列
_ = scatter_matrix(df_merged_except_objec)
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


# 教師あり学習
# 線形回帰に正則化項を加えた手法に、ラッソ回帰(lasso regression)とリッジ回帰(ridge regression)がある
# ロジスティック回帰は分類問題に用いる手法
# ランダムフォレスト
# SVM
# ニューラルネットワーク（線形分類にしかできない）　➡　多重パーセプトロン
# 自己回帰モデル(ARモデル)　➡　時系列データを対象にする

# 教師なし学習
# 階層なしクラスタリング(k-means法)
# 階層ありクラスタリング(ウォード法)
# 主成分分析
# 協調フィルタリング
# トピックモデル

# 強化学習
# バンディットアルゴリズム
# マルコフ決定過程モデル
# 価値関数
# 方策勾配

# deep learning

# 直線回帰分
x = df[['calculatedose']].values
y = df[['chamberdose']].values
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
# 分類木を読み込み
decision_tree = tree.DecisionTreeClassifier()
# decision_tree = DecisionTreeRegressor()
decision_tree = tree.DecisionTreeClassifier()
decision_tree

# 学習
decision_tree = decision_tree.fit(X_train, y_train)
decision_tree

# 予測
y_pred = decision_tree.predict(X_test)
y_pred

# 正解率
print('正解率 : ' + str(accuracy_score(y_test, y_pred)))


min_samples_split_list = [i for i in range(2,7)]
print(min_samples_split_list)

for min_samples_split in min_samples_split_list:
    decision_tree = tree.DecisionTreeClassifier(min_samples_split=min_samples_split)
    decision_tree.fit(X_train, y_train)
    y_pred = decision_tree.predict(X_test)
    print(min_samples_split,accuracy_score(y_test, y_pred))

min_impurity_decrease_list = np.arange(0, 0.1, 0.02)
print(min_impurity_decrease_list)

for min_impurity_decrease in min_impurity_decrease_list:
    decision_tree = tree.DecisionTreeClassifier(min_impurity_decrease=min_impurity_decrease)
    decision_tree.fit(X_train, y_train)
    y_pred = decision_tree.predict(X_test)
    print(min_impurity_decrease,accuracy_score(y_test, y_pred))

# 適合率
from sklearn.metrics import precision_score
print('適合率 : ' + str(precision_score(y_test, y_pred)))

# 再現率
from sklearn.metrics import recall_score
print('再現率 : ' + str(recall_score(y_test, y_pred)))

# F値
from sklearn.metrics import f1_score
print('F値 : ' + str(f1_score(y_test, y_pred)))

# F値(最適なパラメータを探す。split_listの幅を狭めてよりよいものを)
for min_samples_split in min_samples_split_list:
    for min_impurity_decrease in min_impurity_decrease_list:
        decision_tree = tree.DecisionTreeClassifier(min_samples_split=min_samples_split, min_impurity_decrease=min_impurity_decrease)
        decision_tree.fit(X_train, y_train)
        y_pred = decision_tree.predict(X_test)
        print(min_samples_split,min_impurity_decrease,f1_score(y_test, y_pred))

best_score = 0
min_samples_split_list = [i for i in range(5,11)]
min_impurity_decrease_list = np.arange(0, 0.025, 0.005)
for min_samples_split in min_samples_split_list:
    for min_impurity_decrease in min_impurity_decrease_list:
        decision_tree = tree.DecisionTreeClassifier(min_samples_split=min_samples_split, min_impurity_decrease=min_impurity_decrease)
        decision_tree.fit(X_train, y_train)
        y_pred = decision_tree.predict(X_test)
        score = f1_score(y_test, y_pred)
        if score > best_score:
            best_score = score
            best_parameters = {'min_samples_split':min_samples_split,'min_impurity_decrease':min_impurity_decrease,'best_score':best_score}
print(best_parameters)

# 不要なパラメータ削除
X_train.drop('DD',axis=1,inplace=True)
X_test.drop('DD',axis=1,inplace=True)
print("X_train:",X_train.columns)
print("X_test:",X_test.columns)

best_score = 0
min_samples_split_list = [i for i in range(5,11)]
min_impurity_decrease_list = np.arange(0, 0.025, 0.005)
for min_samples_split in min_samples_split_list:
    for min_impurity_decrease in min_impurity_decrease_list:
        decision_tree = tree.DecisionTreeClassifier(min_samples_split=min_samples_split, min_impurity_decrease=min_impurity_decrease)
        decision_tree.fit(X_train, y_train)
        y_pred = decision_tree.predict(X_test)
        score = f1_score(y_test, y_pred)
        if score > best_score:
            best_score = score
            best_parameters = {'min_samples_split':min_samples_split,'min_impurity_decrease':min_impurity_decrease,'best_score':best_score}
print(best_parameters)



# print(accuracy_score(y_test, y_pred))
# # 決定木をインスタンス化する (木の最大深さ=3)
# tree = DecisionTreeClassifier(max_depth=3)
# # 学習
# tree.fit(X_train, y_train)



# ロジスティック回帰

logistic_regression = LogisticRegression(random_state=0)
logistic_regression

logistic_regression = logistic_regression.fit(X_train,y_train)
logistic_regression

y_pred = logistic_regression.predict(X_test)
y_pred

# F価
from sklearn.metrics import f1_score
print(f1_score(y_test, y_pred))

# 正則化項調整のためのパラメータ
C_list =[10**i for i in range(-5, 6)]
C_list

for C in C_list:
    logistic_regression =  LogisticRegression(random_state=0,C=C)
    logistic_regression.fit(X_train, y_train)
    y_pred = logistic_regression.predict(X_test)
    print(C,f1_score(y_test, y_pred))





# ランダムフォレスト

random_forest = RandomForestClassifier(random_state=0)
random_forest

random_forest = random_forest.fit(X_train,y_train)
random_forest

y_pred = random_forest.predict(X_test)
y_pred

from sklearn.metrics import f1_score
print(f1_score(y_test, y_pred))

# ランダムフォレストの主要パラメータであるn_estimotrs（木の数）、max_depth（木の深さ）、max_features（分岐に用いる説明変数の数を設定）を変更
n_estimators_list = [5,10,100,300]
print(n_estimators_list)
max_depth_list = [2,3,4]
print(max_depth_list)
max_feature_list = [2,3,5]
print(max_feature_list)

best_score = 0

for n_estimators in n_estimators_list:
    for max_depth in max_depth_list:
        for max_features in max_feature_list:
            random_forest =  RandomForestClassifier(n_estimators=n_estimators,max_depth=max_depth,max_features=max_features,random_state=0)
            random_forest.fit(X_train, y_train)
            y_pred = random_forest.predict(X_test)
            score = f1_score(y_test, y_pred)
            if score > best_score:
                best_score = score
                best_parameters = {'n_estimators':n_estimators,'max_depth':max_depth,'max_features':max_features,'best_score':best_score}
print(best_parameters)

random_forest =  RandomForestClassifier(n_estimators=10,max_depth=3,max_features=2,random_state=0)
random_forest.fit(X_train, y_train)
features = X_train.columns
importances = random_forest.feature_importances_
indices = np.argsort(importances)
plt.barh(range(len(indices)), importances[indices])
plt.yticks(range(len(indices)), features[indices])
plt.show()


# 目的変数が量的変数の場合（回帰）を確認
y_train = X_train['Median']
y_test = X_test['Median']
X_train.drop('Median',axis=1,inplace=True)
X_test.drop('Median',axis=1,inplace=True)
print('X_train:',X_train.columns)
print('X_test:',X_test.columns)
print('y_train:',y_train.head())
print('y_test:',y_test.head())


random_forest = RandomForestRegressor(random_state=0)
random_forest

random_forest = random_forest.fit(X_train,y_train)
random_forest

y_pred = random_forest.predict(X_test)
y_pred[:50]

from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_pred,y_test)

plt.scatter(y_pred,y_test)
plt.title('Scatter Plot of Predict vs Test')
plt.xlabel('Pred')
plt.ylabel('Test')
plt.grid()
plt.show()


# K-means

kmeans_model = KMeans(n_clusters=4, random_state=0).fit(df)
kmeans_model

labels = kmeans_model.labels_
labels[0:50]

# cluster列を作成し、クラスタリング結果を格納
df['cluster'] = labels
titanic_add_cluster = df
titanic_add_cluster.head()

# クラスタリング結果を確認
df['cluster'].value_counts()

# グループ毎に各カラムの値の平均値を出
titanic_add_cluster.groupby('cluster').mean()

pca = PCA(random_state=0)
pca

# 主成分分析を実行
pca.fit(titanic_add_cluster)

# 次元削減を実行し、featureと言う変数に格納
feature = pca.transform(titanic_add_cluster)
feature

# 主成分分析を可視化
color_codes = {0:'#00FF00', 1:'#FF0000', 2:'#0000FF',  3:'#ffff00'}
colors = [color_codes[x] for x in labels]
colors[:50]

plt.figure(figsize=(6, 6))
plt.scatter(feature[:, 0], feature[:, 1], color=colors)
plt.title("Principal Component Analysis")
plt.xlabel("First principal component")
plt.ylabel("Second principal component")
plt.show()












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

