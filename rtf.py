import pydicom

df = pydicom.read_file("RTplan.dcm")  # 取得したいRTplanのファイル名をRTplanにする

beam_number = df.FractionGroupSequence[0].NumberOfBeams  # Arc数取得

cp_list = []
for i in range(beam_number):
    cp = df.BeamSequence[i].NumberOfControlPoints
    cp_list.append(cp)

cp_sum = sum(cp_list)


def beamnumber_split(tosplitdata):
    '''dataをbeamnumber(Arc数)ごとに分割してListに保存'''

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


def cp_beamnumber_split(tosplitdata):
    '''dataをbeamnumber(Arc数-1)ごとに分割してListに保存'''

    separate = []
    start = 0
    newArray = []
    for i in range(beam_number):
        if i == 0:
            separate.append(int(cp_list[i])-1)
            cp = int(cp_list[i])-1
        else:
            separate.append(cp+int(cp_list[i])-1)
            cp = cp+int(cp_list[i])-1
    for sp in separate:
        newArray.append(tosplitdata[start:sp])
        start = sp
    return newArray


def mlc_beamnumber_split(tosplitdata):
    '''dataをMLCごとに分割してListに保存'''

    separate = []
    start = 0
    newArray = []
    for i in range(beam_number):
        if i == 0:
            separate.append(60)
            mlc = 60
        else:
            separate.append(int(mlc)+60)
            mlc = int(mlc) + 60
    for sp in separate:
        newArray.append(tosplitdata[start:sp])
        start = sp
    return newArray


def xjaw_position():
    '''Xjawのデータを算出'''

    x_position = []
    for bi in range(beam_number):
        for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
            jaw = df.BeamSequence[bi].ControlPointSequence[cj].BeamLimitingDevicePositionSequence[0].LeafJawPositions
            x_position.append(jaw)
    return x_position


def yjaw_position():
    '''Yjawのデータを算出'''

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


def Weight_data():  # Weight_data
    weight_data = []
    for bi in range(beam_number):
        for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
            weight = df.BeamSequence[bi].ControlPointSequence[cj].CumulativeMetersetWeight
            weight_data.append(weight)
    return weight_data


def MU_cp(mu, weight):  # MU/CP
    mu_cp = []
    for bi in range(beam_number):
        for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
            mu_cp.append(mu[bi]*weight[bi][cj])
    return mu_cp


def list_sub(sub_list):
    sublist = []
    for bi in range(beam_number):
        for cj in range(int(df.BeamSequence[bi].NumberOfControlPoints)-1):
            sublist.append(sub_list[bi][cj+1] - sub_list[bi][cj])
        sublist.append(0)
    return sublist


def list_sub_JTCS(sub_list):
    sublist_x1 = []
    sublist_x2 = []
    for bi in range(beam_number):
        for cj in range(int(df.BeamSequence[bi].NumberOfControlPoints)-1):
            sublist_x1.append(abs(sub_list[bi][cj+1][0] - sub_list[bi][cj][0]))
            sublist_x2.append(abs(sub_list[bi][cj+1][1] - sub_list[bi][cj][1]))
    return sublist_x1, sublist_x2


def beamnumber_split_JTCS(tosplitdata):  # dataをbeamnumberごとに分割
    separate = []
    newArray = []
    cp_list_JTCS = []
    for i in range(beam_number):
        cp_list_JTCS.append(int(cp_list[i])-1)
    for i in range(beam_number):
        if i == 0:
            separate.append(int(cp_list_JTCS[i]))
            cp = int(cp_list_JTCS[i])
        else:
            separate.append(cp+int(cp_list_JTCS[i]))
            cp = cp+int(cp_list_JTCS[i])
    for i in range(2):
        start = 0
        for sp in separate:
            newArray.append(tosplitdata[i][start:sp])
            start = sp
    return newArray


def ARC_sum(sum_data):
    Sum_data = []
    for i in range(len(sum_data)):
        Sum_data.append(sum(sum_data[i]))
    return Sum_data


def ARC_JTCS(arc_data):
    Arc_data = []
    for i in range(beam_number):
        Arc_data.append((arc_data[i] + arc_data[i+2]) /
                        (int(df.BeamSequence[i].NumberOfControlPoints)-1))
    return Arc_data
