import pydicom
import matplotlib.pyplot as plt
import matplotlib.style
matplotlib.style.use('ggplot')

df = pydicom.read_file("tes1.dcm")

a = df.ROIContourSequence[1].ContourSequence[0].ContourData
b = df.ROIContourSequence[1].ContourSequence[1].ContourData
fig, axes = plt.subplots(2)
axes[0].plot(a, label='legend label')
axes[1].plot(b, label='legend label')
plt.show()



# stracture読み込み必要

b = a["BODY"]

list_z = list(b.keys())

tmp_a = []
tmp_b = []
tmp_c = []
    
for r in list_z :
    for i in range (len(b[r][0])):
        tmp_a.append(b[r][0][i][0])
        tmp_b.append(b[r][0][i][1])
        tmp_c.append(r)
    


from mpl_toolkits.mplot3d import Axes3D
# Figureを追加
fig = plt.figure(figsize=(8, 8))

# 3DAxesを追加
ax = fig.add_subplot(111, projection='3d')


# Axesのタイトルを設定
ax.scatter(tmp_a,tmp_b,tmp_c)
plt.xlim(-500, 500)
plt.ylim(-200, 200)
plt.show()