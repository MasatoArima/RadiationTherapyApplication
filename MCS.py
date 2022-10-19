import pydicom
import rtf
import numpy as np

df = pydicom.read_file("RTplan.dcm")  # 取得したいRTplanのファイル名をRTplanにする

beam_number = df.FractionGroupSequence[0].NumberOfBeams  # Arc数取得
Jaw_ref = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75,
           80, 85, 90, 95, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
Jaw_ref2 = [0, -5, -10, -15, -20, -25, -30, -35, -40, -45, -50, -55, -60, -65, -70, -
            75, -80, -85, -90, -95, -100, -110, -120, -130, -140, -150, -160, -170, -180, -190, -200]

cp_list = []
for i in range(beam_number):
    cp = df.BeamSequence[i].NumberOfControlPoints
    cp_list.append(cp)

cp_sum = sum(cp_list)

xjaw = rtf.beamnumber_split(rtf.xjaw_position())
yjaw = rtf.beamnumber_split(rtf.yjaw_position())
mlc = rtf.beamnumber_split(rtf.MLC_position())
mu = rtf.MU_data()
total_mu = sum(mu)
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
y2jaw = rtf.beamnumber_split(y2jaw)

tmp = []
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
            if y2jaw[bi][cj] == mk:
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
            if y2jaw[bi][cj] == mk:
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

mlc_b_bank.append(tmp)
mlc_b_bank.pop(0)

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
    Bsum_Leaf.append((y1_b_bank[i])+(y2_b_bank[i]))
    Bmax_Leaf.append(max((Bsum_Leaf[i])))
    Bmin_Leaf.append(min((Bsum_Leaf[i])))
    Bsub_Leaf.append((Bmax_Leaf[i])-(Bmin_Leaf[i]))

sum_list_A = []
sum_list_B = []

for j in range(cp_sum):
    list_A = []
    list_B = []
    sum_list_A.append(list_A)
    sum_list_B.append(list_B)
    for r in range(len(mlc_a_bank[j])):
        list_A.append(Asub_Leaf[j]-mlc_a_bank[j][r])
    for r in range(len(mlc_b_bank[j])):
        list_B.append(Bsub_Leaf[j]-mlc_b_bank[j][r])

# SUM
sum_A = []
sum_B = []
count_A = []
count_B = []

for j in range(cp_sum):
    sum_A.append(sum(sum_list_A[j]))
    sum_B.append(sum(sum_list_B[j]))
    count_A.append(len(mlc_a_bank[j]))
    count_B.append(len(mlc_b_bank[j]))


sum_max_A = []
sum_max_B = []
for j in range(cp_sum):
    sum_max_A.append(count_A[j]*Asub_Leaf[j])
    sum_max_B.append(count_B[j]*Bsub_Leaf[j])

LSV_A = []
LSV_B = []
for j in range(cp_sum):
    LSV_A.append(sum_A[j]/sum_max_A[j])
    LSV_B.append(sum_B[j]/sum_max_B[j])

LSV_CP = []
for j in range(cp_sum):
    LSV_CP.append(LSV_A[j]*LSV_B[j])


# AAV
y1_a_bank_aav = []
y1_b_bank_aav = []
y2_a_bank_aav = []
y2_b_bank_aav = []
cat_y1jaw = []
for bi in range(beam_number):
    for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
        cat_y1jaw.append(29 - y1jaw[bi][cj])

cat_y1jaw = rtf.beamnumber_split(cat_y1jaw)

# Y１_Abank(0~30)
for bi in range(beam_number):
    for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
        y1_a_bank_aav.append(tmp)
        tmp = []
        for r in range(30):
            if (cat_y1jaw[bi][cj]) > r:
                tmp.append(0)
            elif (cat_y1jaw[bi][cj]) == r:
                for h in range((30-(30-r)), 30, 1):
                    tmp.append(mlc[bi][cj][h])
            else:
                break

y1_a_bank_aav.append(tmp)
y1_a_bank_aav.pop(0)

# Y1_Bbank(60~90)
for bi in range(beam_number):
    for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
        y1_b_bank_aav.append(tmp)
        tmp = []
        for r in range(30):
            if cat_y1jaw[bi][cj] > r:
                tmp.append(0)
            elif cat_y1jaw[bi][cj] == r:
                for h in range((89-(29-r)), 90, 1):
                    tmp.append(mlc[bi][cj][h])
            else:
                break

y1_b_bank_aav.append(tmp)
y1_b_bank_aav.pop(0)

# Y2_Abank(30~60)
for bi in range(beam_number):
    for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
        y2_a_bank_aav.append(tmp)
        tmp = []
        for r in range(30):
            if y2jaw[bi][cj] > r:
                pass
            elif y2jaw[bi][cj] == r:
                for h in range(30, (31+r), 1):
                    tmp.append(mlc[bi][cj][h])
            else:
                tmp.append(0)

y2_a_bank_aav.append(tmp)
y2_a_bank_aav.pop(0)

# Y2_Bbank(90~120)
for bi in range(beam_number):
    for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
        y2_b_bank_aav.append(tmp)
        tmp = []
        for r in range(30):
            if y2jaw[bi][cj] > r:
                pass
            elif y2jaw[bi][cj] == r:
                for h in range(90, (91+r), 1):
                    tmp.append(mlc[bi][cj][h])
            else:
                tmp.append(0)

y2_b_bank_aav.append(tmp)
y2_b_bank_aav.pop(0)

# AbankとBbank
lsv_a_aav = []
lsv_b_aav = []
for i in range(cp_sum):
    lsv_a_aav.append(y1_a_bank_aav[i] + y2_a_bank_aav[i])
    lsv_b_aav.append(y1_b_bank_aav[i] + y2_b_bank_aav[i])

lsv_a_aav = rtf.beamnumber_split(lsv_a_aav)
lsv_b_aav = rtf.beamnumber_split(lsv_b_aav)

lsv_a_aav_x = []
lsv_b_aav_x = []
for bi in range(beam_number):
    for mk in range(60):
        lsv_a_aav_x.append(tmp)
        tmp = []
        for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
            tmp.append(lsv_a_aav[bi][cj][mk])

lsv_a_aav_x.append(tmp)
lsv_a_aav_x.pop(0)
lsv_a_aav_x = rtf.mlc_beamnumber_split(lsv_a_aav_x)
# print(lsv_a_aav_x[0][10])

for bi in range(beam_number):
    for mk in range(60):
        lsv_b_aav_x.append(tmp)
        tmp = []
        for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
            tmp.append(lsv_b_aav[bi][cj][mk])

lsv_b_aav_x.append(tmp)
lsv_b_aav_x.pop(0)
lsv_b_aav_x = rtf.mlc_beamnumber_split(lsv_b_aav_x)

lsv_Amin = []
lsv_Bmin = []

for i in range(beam_number):
    for j in range(60):
        lsv_Amin.append(min(lsv_a_aav_x[i][j]))
        lsv_Bmin.append(max(lsv_b_aav_x[i][j]))

lsv_Amin = rtf.mlc_beamnumber_split(lsv_Amin)
lsv_Bmin = rtf.mlc_beamnumber_split(lsv_Bmin)

lsv_Amin = np.array(lsv_Amin)
lsv_Bmin = np.array(lsv_Bmin)

AAV_min = []

for i in range(beam_number):
    for j in range(60):
        AAV_min = (lsv_Amin)-(lsv_Bmin)


lsv_a = rtf.beamnumber_split(lsv_a)
lsv_b = rtf.beamnumber_split(lsv_b)

AAV_sub = []
for i in range(beam_number):
    for j in range(df.BeamSequence[i].NumberOfControlPoints):
        tmp = []
        AAV_sub.append(tmp)
        for r in range(len(lsv_a[i][j])):
            tmp.append(lsv_a[i][j][r]-lsv_b[i][j][r])

sum_AAV = []
for ci in range(cp_sum):
    sum_AAV.append(sum(AAV_sub[ci]))


y1_a_bank_aav_out = []
y1_b_bank_aav_out = []
y2_a_bank_aav_out = []
y2_b_bank_aav_out = []

# Y１_Abank(0~30)
for bi in range(beam_number):
    for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
        y1_a_bank_aav_out.append(tmp)
        tmp = []
        for r in range(30):
            if (cat_y1jaw[bi][cj]) > r:
                tmp.append(1000.0)
            elif (cat_y1jaw[bi][cj]) == r:
                for h in range((30-(30-r)), 30, 1):
                    tmp.append(mlc[bi][cj][h])
            else:
                break

y1_a_bank_aav_out.append(tmp)
y1_a_bank_aav_out.pop(0)

# Y1_Bbank(60~90)
for bi in range(beam_number):
    for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
        y1_b_bank_aav_out.append(tmp)
        tmp = []
        for r in range(30):
            if cat_y1jaw[bi][cj] > r:
                tmp.append(1000.0)
            elif cat_y1jaw[bi][cj] == r:
                for h in range((89-(29-r)), 90, 1):
                    tmp.append(mlc[bi][cj][h])
            else:
                break

y1_b_bank_aav_out.append(tmp)
y1_b_bank_aav_out.pop(0)

# Y2_Abank(30~60)
for bi in range(beam_number):
    for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
        y2_a_bank_aav_out.append(tmp)
        tmp = []
        for r in range(30):
            if y2jaw[bi][cj] > r:
                pass
            elif y2jaw[bi][cj] == r:
                for h in range(30, (31+r), 1):
                    tmp.append(mlc[bi][cj][h])
            else:
                tmp.append(1000.0)

y2_a_bank_aav_out.append(tmp)
y2_a_bank_aav_out.pop(0)

# Y2_Bbank(90~120)
for bi in range(beam_number):
    for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
        y2_b_bank_aav_out.append(tmp)
        tmp = []
        for r in range(30):
            if y2jaw[bi][cj] > r:
                pass
            elif y2jaw[bi][cj] == r:
                for h in range(90, (91+r), 1):
                    tmp.append(mlc[bi][cj][h])
            else:
                tmp.append(1000.0)

y2_b_bank_aav_out.append(tmp)
y2_b_bank_aav_out.pop(0)

# AbankとBbank
lsv_a_aav_out = []
lsv_b_aav_out = []
for i in range(cp_sum):
    lsv_a_aav_out.append(y1_a_bank_aav_out[i] + y2_a_bank_aav_out[i])
    lsv_b_aav_out.append(y1_b_bank_aav_out[i] + y2_b_bank_aav_out[i])

lsv_a_aav_out = rtf.beamnumber_split(lsv_a_aav_out)
lsv_b_aav_out = rtf.beamnumber_split(lsv_b_aav_out)

aav_sum = []
for i in range(beam_number):
    for j in range(df.BeamSequence[i].NumberOfControlPoints):
        aav_sum.append(tmp)
        tmp = []
        for k in range(60):
            if lsv_a_aav_out[i][j][k] == (1000.0):
                pass
            elif lsv_a_aav_out[i][j][k] != (1000.0):
                tmp.append(AAV_min[i][k])
    aav_sum.append(tmp)
    aav_sum.pop(0)

aav_sum = rtf.beamnumber_split(aav_sum)

aav_sum_all = []
for i in range(beam_number):
    for j in range(df.BeamSequence[i].NumberOfControlPoints):
        aav_sum_all.append(sum(aav_sum[i][j]))

AAV = []
for ci in range(cp_sum):
    AAV.append(sum_AAV[ci]/(aav_sum_all[ci]))

AAV = rtf.beamnumber_split(AAV)
LSV_CP = rtf.beamnumber_split(LSV_CP)

cp_w = []
AAV_F = []
LSV_F = []

for bi in range(beam_number):
    for cj in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
        AAV_F.append((AAV[bi][cj]+AAV[bi][cj+1])/2)
        LSV_F.append((LSV_CP[bi][cj]+LSV_CP[bi][cj+1])/2)
        cp_w.append((mu_cp[bi][cj]+mu_cp[bi][cj+1])/mu[bi])

AAV_F = rtf.cp_beamnumber_split(AAV_F)
LSV_F = rtf.cp_beamnumber_split(LSV_F)
cp_w = rtf.cp_beamnumber_split(cp_w)

MCS_sum = []
for i in range(beam_number):
    for j in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
        MCS_sum.append(AAV_F[i][j]*LSV_F[i][j]*cp_w[i][j])

MCS_sum = rtf.cp_beamnumber_split(MCS_sum)

MCS_F = []
for i in range(beam_number):
    MCS_F.append(sum(MCS_sum[i])*(mu[i]/total_mu))

MCS = sum(MCS_F)
print(MCS)
