import pydicom
import matplotlib.pyplot as plt
import matplotlib.style
from mpl_toolkits.mplot3d import Axes3D
matplotlib.style.use('ggplot')

df = pydicom.read_file("RTplan.dcm")

# stracture読み込み必要

origin = input('DICOMoriginを入力してください : ')

b = a["Skin"]
b1 = a["PTV_66"]

list_y = list(b.keys())
list_y1 = list(b1.keys())
tmp_a = []
tmp_b = []
tmp_c = []
tmp_a1 = []
tmp_b1 = []
tmp_c1 = []
    
for r in list_y :
    for i in range (len(b[r][0])):
        tmp_a.append(b[r][0][i][0])
        tmp_b.append(b[r][0][i][1])
        tmp_c.append(origin + r)

for r in list_y1 :
    for i in range (len(b1[r][0])):
        tmp_a1.append(b1[r][0][i][0])
        tmp_b1.append(b1[r][0][i][1])
        tmp_c1.append(origin + r)


fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, projection='3d')
ax.plot(tmp_a,tmp_b,tmp_c)
ax.plot(tmp_a1,tmp_b1,tmp_c1, color='blue')
ax.view_init(elev=0, azim=270)
plt.show()

fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, projection='3d')
ax.plot(tmp_a,tmp_b,tmp_c)
ax.plot(tmp_a1,tmp_b1,tmp_c1, color='blue')
ax.view_init(elev=20, azim=200)
plt.show()