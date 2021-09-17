import pydicom
import rtf

df = pydicom.read_file("RTplan.dcm")  # 取得したいRTplanのファイル名をRTplanにする

beam_number = df.FractionGroupSequence[0].NumberOfBeams  # Arc数取得

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
no_normalization_mu_cp = rtf.beamnumber_split(rtf.MU_cp(mu, weight))
mu_cp = rtf.beamnumber_split(rtf.CP_weight_normalize(no_normalization_mu_cp))
print(len(mu_cp))