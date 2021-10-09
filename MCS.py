import pydicom
import rtf
import numpy as np

df = pydicom.read_file("RTplan.dcm")  # 取得したいRTplanのファイル名をRTplanにする

beam_number = df.FractionGroupSequence[0].NumberOfBeams  # Arc数取得
Jaw_ref = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
Jaw_ref2 = [0, -5, -10, -15, -20, -25, -30, -35, -40, -45, -50, -55, -60, -65, -70, -75, -80, -85, -90, -95, -100, -110, -120, -130, -140, -150, -160, -170, -180, -190, -200]

cp_list = []
for i in range(beam_number):
    cp = df.BeamSequence[i].NumberOfControlPoints
    cp_list.append(cp)

cp_sum = sum(cp_list)

xjaw = rtf.beamnumber_split(rtf.xjaw_position())
yjaw = rtf.beamnumber_split(rtf.yjaw_position())
mlc = rtf.beamnumber_split(rtf.MLC_position())
mu = rtf.MU_data()
weight = rtf.beamnumber_split(rtf.Weight_data())
no_sub_mu_cp = rtf.beamnumber_split(rtf.MU_cp(mu, weight))
mu_cp = rtf.beamnumber_split(rtf.list_sub(no_sub_mu_cp))

xjaw =tolist(xjaw)
yjaw =tolist(yjaw)
Y2jaw = []
Y1jaw = []
# Y2のJawサイズを0~30の数値に変換
for ci in range(cp_sum):
    for j in range(len(Jaw_ref)):
        if Jaw_ref[j] < yjaw[ci][1] <= Jaw_ref[j+1]:
            Y2jaw.append(j)
        if Jaw_ref2[j] > yjaw[ci][0] >= Jaw_ref2[j+1]:
            Y1jaw.append(j)

# Y1のJawサイズを0~30の数値に変換
# for i in range(cp_sum):
#     for j in range(len(Jaw_ref2)):
#         if Jaw_ref2[j] > data_Jaw_Y[i][0] >= Jaw_ref2[j+1]:
#             Y1jaw.append(j)

print(Y2jaw)
print(Y1jaw)