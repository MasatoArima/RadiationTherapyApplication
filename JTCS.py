import pydicom
import rtf

df = pydicom.read_file("RTplan.dcm")  # 取得したいRTplanのファイル名をRTplanにする

beam_number = df.FractionGroupSequence[0].NumberOfBeams  # Arc数取得

cp_list = []
for i in range(beam_number):
    cp = df.BeamSequence[i].NumberOfControlPoints
    cp_list.append(cp)

cp_sum = sum(cp_list)

# Xjawのみ
xjaw = rtf.beamnumber_split(rtf.xjaw_position())
# x1.arc1 : x1.arc2 : x2.arc1 : x2.arc2
xjaw_sub = rtf.beamnumber_split_JTCS(rtf.list_sub_JTCS(xjaw))
xjaw_arc_sum = rtf.ARC_sum(xjaw_sub)
jtcs_arc = rtf.ARC_JTCS(xjaw_arc_sum)
jtcs = sum(jtcs_arc)/beam_number

