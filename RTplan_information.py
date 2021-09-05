import pydicom

df = pydicom.read_file("RTplan.dcm")  # 取得したいRTplanのファイル名をRTplanにする

beam_number = df.FractionGroupSequence[0].NumberOfBeams  # Arc数取得

cp_list = []
for i in range(beam_number):
    cp = df.BeamSequence[i].NumberOfControlPoints
    cp_list.append(cp)
