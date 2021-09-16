import pydicom

df = pydicom.read_file("RTplan.dcm")  # 取得したいRTplanのファイル名をRTplanにする

beam_number = df.FractionGroupSequence[0].NumberOfBeams  # Arc数取得

cp_list = []
for i in range(beam_number):
    cp = df.BeamSequence[i].NumberOfControlPoints
    cp_list.append(cp)

cp_sum = sum(cp_list)


def beamnumber_split(tosplitdata):  # dataをbeamnumberごとに分割
    separate = []
    start = 0
    newArray = []
    for i in range(beam_number):
        if i == 0:
            separate.append(int(cp_list[i]))
            cp = int(cp_list[i])
        else:
            separate.append(cp+int(cp_list[i]))
            cp = cp+int(cp_list[i])
    for sp in separate:
        newArray.append(tosplitdata[start:sp])
        start = sp
    return newArray


def xjaw_position():  # xJawのposition算出
    x_position = []
    for bi in range(beam_number):
        for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
            jaw = df.BeamSequence[bi].ControlPointSequence[cj].BeamLimitingDevicePositionSequence[0].LeafJawPositions
            x_position.append(jaw)
    return x_position


def yjaw_position():  # yJawのposition算出
    y_position = []
    for bi in range(beam_number):
        for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
            jaw = df.BeamSequence[bi].ControlPointSequence[cj].BeamLimitingDevicePositionSequence[1].LeafJawPositions
            y_position.append(jaw)
    return y_position


def MLC_position():  # MLC position
    mlc_position = []
    for bi in range(beam_number):
        for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
            mlc = df.BeamSequence[bi].ControlPointSequence[cj].BeamLimitingDevicePositionSequence[2].LeafJawPositions
            mlc_position.append(mlc)
    return mlc_position


def MU_data():  # MU_data
    mu_data = []
    for bi in range(beam_number):
        MU = df.FractionGroupSequence[0].ReferencedBeamSequence[bi].BeamMeterset
        mu_data.append(MU)
    return mu_data
