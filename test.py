import pydicom
import matplotlib.pyplot as plt
import matplotlib.style
from mpl_toolkits.mplot3d import Axes3D
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