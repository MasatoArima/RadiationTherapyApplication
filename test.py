import pydicom
import matplotlib.pyplot as plt
import matplotlib.style
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
matplotlib.style.use('ggplot')

df = pydicom.read_file("RTplan.dcm")

# stracture読み込み必要


# DICOM origin data をプランごとに入力
origin = input('DICOMoriginを入力してください : ')
# 作成したストラクチャをa["XXX"]の形で下記に入力。区切りはカンマ(,)で行う。
b = [ a["Skin"], a["PTV_66"], a["SpinalCanal"] ]

list_y = [[b[i].keys()] for i in range(len(b))]
x = [ [ b[x][r][0][i][0] for r in list_y[x][0] for i in range (len(b[x][r][0]))] for x in range(len(b))]
y = [ [ b[x][r][0][i][1] for r in list_y[x][0] for i in range (len(b[x][r][0]))] for x in range(len(b))]
z = [ [ (origin + r) for r in list_y[x][0] for i in range (len(b[x][r][0]))] for x in range(len(b))]

fig = plt.figure(figsize=(5, 5))
fig2 = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, projection='3d')
ax2 = fig2.add_subplot(111, projection='3d')

color = ['red','blue','black']

for i in range (len(b)):
    ax.plot(x[i],y[i],z[i], color = color[i])
    ax2.plot(x[i],y[i],z[i], color = color[i])

ax.view_init(elev=0, azim=270)
ax2.view_init(elev=20, azim=200)

plt.show()

ax = plt.gca()  # gca stands for 'get  axis'
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))


# 重心を入力
w_x = 24
w_y = 23
# print(z[0])
# print(z[0].count(-14))

x = x[0][5:46]
y = y[0][5:46]


x = [x2 + w_x  for x2 in x]
y = [y2 + w_y  for y2 in y]

plt.plot(x, y, "o", c="blue")

degree = range(360)
deg = []
sin = []
cos = []

for i in range(len(degree)):
    deg.append(np.deg2rad(degree[i]))

for i in range(len(degree)):
    cos.append(np.cos(deg[i]))
    sin.append(np.sin(deg[i]))

x_dash = []
y_dash = []

for t in range (len(deg)):
    for i in range (len(x)):
        rot_x = (x[i] * cos[t]) - (y[i] * sin[t])
        rot_y = (x[i] * sin[t]) + (y[i] * cos[t])
        x_dash.append(rot_x)
        y_dash.append(rot_y)

tes_x = [ [(x[i] * cos[t]) - (y[i] * sin[t]) for i in range (len(x))] for t in range (len(deg))]

plt.plot(x_dash, y_dash, "o", c="red")
plt.show()

tes_max = [max(tes_x[i])+w_x for i in range(len(tes_x))]
tes_min = [min(tes_x[i])+w_x for i in range(len(tes_x))]

print(tes_max)
print(tes_min)