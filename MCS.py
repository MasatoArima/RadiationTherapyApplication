from old_mcs import Asum_Leaf
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


# Y2のJawサイズを0~30の数値に変換
y2jaw = []
y1jaw = []
for bi in range(beam_number):
    for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
        for jk in range(len(Jaw_ref)):
            if Jaw_ref[jk] < yjaw[bi][cj][1] <= Jaw_ref[jk+1]:
                y2jaw.append(jk)
            if Jaw_ref2[jk] > yjaw[bi][cj][0] >= Jaw_ref2[jk+1]:
                y1jaw.append(jk)

y1jaw = rtf.beamnumber_split(y1jaw)


tmp =[]
y1_a_bank = []
y1_b_bank = []
y2_a_bank = []
y2_b_bank = []
# Y１_Abank(0~30)
for bi in range(beam_number):
    for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
        for mk in range(30):
            if y1jaw[bi][cj] == mk:
                y1_a_bank.append(tmp)
                tmp = []
                for ml in range(30):
                    if mk == ml:
                        for h in range((29-ml), 30, 1):
                            tmp.append(mlc[bi][cj][h])

y1_a_bank.append(tmp)
y1_a_bank.pop(0)

# Y1_Bbank(60~90)
for bi in range(beam_number):
    for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
        for mk in range(30):
            if y1jaw[bi][cj] == mk:
                y1_b_bank.append(tmp)
                tmp = []
                for ml in range(30):
                    if mk == ml:
                        for h in range((89-ml), 90, 1):
                            tmp.append(mlc[bi][cj][h])

y1_b_bank.append(tmp)
y1_b_bank.pop(0)

# Y2_Abank(30~60)
for bi in range(beam_number):
    for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
        for mk in range(30):
            if y1jaw[bi][cj] == mk:
                y2_a_bank.append(tmp)
                tmp = []
                for ml in range(30):
                    if mk == ml:
                        for h in range(30, (31+ml), 1):
                            tmp.append(mlc[bi][cj][h])

y2_a_bank.append(tmp)
y2_a_bank.pop(0)

# Y2_Bbank(90~120)
for bi in range(beam_number):
    for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
        for mk in range(30):
            if y1jaw[bi][cj] == mk:
                y2_b_bank.append(tmp)
                tmp = []
                for ml in range(30):
                    if mk == ml:
                        for h in range(90, (91+ml), 1):
                            tmp.append(mlc[bi][cj][h])

y2_b_bank.append(tmp)
y2_b_bank.pop(0)

# AbankとBbank
lsv_a = []
lsv_b = []
for i in range(cp_sum):
    lsv_a.append(y1_a_bank[i] + y2_a_bank[i])
    lsv_b.append(y1_b_bank[i] + y2_b_bank[i])

# LSV
mlc_a_bank = []
mlc_b_bank = []
for i in range(cp_sum):
    mlc_a_bank.append(tmp)
    tmp = []
    for j in range(len(lsv_a[i])-1):
        a1 = (lsv_a[i][j])
        a2 = (lsv_a[i][j+1])
        tmp.append(abs(a1-a2))

mlc_a_bank.append(tmp)
mlc_a_bank.pop(0)

for i in range(cp_sum):
    mlc_b_bank.append(tmp)
    tmp = []
    for r in range(len(lsv_b[i])-1):
        b1 = (lsv_b[i][r])
        b2 = (lsv_b[i][r+1])
        tmp.append(abs(b1-b2))

mlc_a_bank.append(tmp)
mlc_a_bank.pop(0)

mlc_a_bank = rtf.beamnumber_split(mlc_a_bank)
mlc_b_bank = rtf.beamnumber_split(mlc_b_bank)

# Abank & Bbank特徴値取得
Asum_Leaf = []
Amax_Leaf = []
Amin_Leaf = []
Asub_Leaf = []
Bsum_Leaf = []
Bmax_Leaf = []
Bmin_Leaf = []
Bsub_Leaf = []
for i in range(cp_sum):
    Asum_Leaf.append((y1_a_bank[i])+(y2_a_bank[i]))
    Amax_Leaf.append(max((Asum_Leaf[i])))
    Amin_Leaf.append(min((Asum_Leaf[i])))
    Asub_Leaf.append((Amax_Leaf[i])-(Amin_Leaf[i]))
    Bsum_Leaf.append((y1_b_bank[i])+(Ly2_b_bank[i]))
    Bmax_Leaf.append(max((Bsum_Leaf[i])))
    Bmin_Leaf.append(min((Bsum_Leaf[i])))
    Bsub_Leaf.append((Bmax_Leaf[i])-(Bmin_Leaf[i]))

print(len(mlc_a_bank))
print(len(mlc_b_bank))