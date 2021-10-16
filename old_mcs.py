import pydicom
import os
import xlwt
import xlrd
import subprocess
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import pylab as plt
import tkinter as tk
from tkinter import *
import tkinter.filedialog as fd
import datetime
import os
import pickle
import time
import tkinter.messagebox
import openpyxl
import csv
import struct
import os.path as osp
import sys
from tkinter import filedialog

import csv
import struct
import os.path as osp
import sys
try:
    # Python 3.x
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename, askopenfilenames, askdirectory
except ImportError:
    # Python 2.x
    from Tkinter import Tk
    from tkFileDialog import askopenfilename, askopenfilenames, askdirectory

def button1_clicked():
    filename = filedialog.askopenfilename(
        title="planを開く",
        filetypes=[("", "*.dcm")],
        initialdir="./"
    )
    dirname = os.path.dirname(filename)
    print(dirname)
    print(filename)

    with pydicom.dcmread(filename, force=True) as df:
        print("OK")
    # df = pydicom.read_file("filename")

    # list
    data_Jaw_X = []
    data_Jaw_Y = []
    data_MLC = []
    data_MU = []
    MU = []
    MU1 = []
    MU2 = []
    MU3 = []
    MU4 = []
    data_Weight = []
    Y2jaw = []
    Y1jaw = []
    LSV_catjaw1 = []
    LSV_catjaw2 = []
    LSV_catYjaw1 = []
    LSV_catYjaw2 = []
    LSV_catYjaw3 = []
    LSV_catYjaw4 = []
    LSV_jaw1 = []
    LSV_jaw2 = []
    LSV_jaw4 = []
    LSV_jaw3 = []
    LSV_A = []
    LSV_B = []
    data_Weight = []
    data_MU = []
    F1 = []
    F2 = []
    F3 = []
    F4 = []
    MLC_Abank = []
    MLC_Abank_F1 = []
    MLC_Abank_F2 = []
    MLC_Abank_F3 = []
    MLC_Abank_F4 = []
    lista = []
    lista1 = []
    lista2 = []
    lista3 = []
    lista4 = []
    listb = []
    listb1 = []
    listb2 = []
    listb3 = []
    listb4 = []
    MLC_Bbank = []
    MLC_Bbank_F1 = []
    MLC_Bbank_F2 = []
    MLC_Bbank_F3 = []
    MLC_Bbank_F4 = []
    Asum_Leaf = []
    Asub_Leaf = []
    Amax_Leaf = []
    Amin_Leaf = []
    Bsum_Leaf = []
    Bsub_Leaf = []
    Bmax_Leaf = []
    Bmin_Leaf = []
    sub_Leaf_F1A = []
    sub_Leaf_F1B = []
    sub_Leaf_F2A = []
    sub_Leaf_F2B = []
    sub_Leaf_F3A = []
    sub_Leaf_F3B = []
    sub_Leaf_F4A = []
    sub_Leaf_F4B = []
    sum_F1_A_MLC = []
    sum_F2_A_MLC = []
    sum_F3_A_MLC = []
    sum_F4_A_MLC = []
    sum_F1_B_MLC = []
    sum_F2_B_MLC = []
    sum_F3_B_MLC = []
    sum_F4_B_MLC = []
    sum_F1_A = []
    sum_F2_A = []
    sum_F3_A = []
    sum_F4_A = []
    sum_F1_B = []
    sum_F2_B = []
    sum_F3_B = []
    sum_F4_B = []
    count_F1_A = []
    count_F2_A = []
    count_F3_A = []
    count_F4_A = []
    count_F1_B = []
    count_F2_B = []
    count_F3_B = []
    count_F4_B = []
    sum_max_F1_A = []
    sum_max_F2_A = []
    sum_max_F3_A = []
    sum_max_F4_A = []
    sum_max_F1_B = []
    sum_max_F2_B = []
    sum_max_F3_B = []
    sum_max_F4_B = []
    LSV_F1A = []
    LSV_F2A = []
    LSV_F3A = []
    LSV_F4A = []
    LSV_F1B = []
    LSV_F2B = []
    LSV_F3B = []
    LSV_F4B = []
    LSV_F1_CP = []
    LSV_F2_CP = []
    LSV_F3_CP = []
    LSV_F4_CP = []
    MLC_data_F1A = []
    MLC_data_F2A = []
    MLC_data_F3A = []
    MLC_data_F4A = []
    MLC_data_F1B = []
    MLC_data_F2B = []
    MLC_data_F3B = []
    MLC_data_F4B = []
    AAV_sub_F1 = []
    AAV_sub_F2 = []
    AAV_sub_F3 = []
    AAV_sub_F4 = []
    sum_F1_AAV = []
    sum_F2_AAV = []
    sum_F3_AAV = []
    sum_F4_AAV = []
    count_F1_AAV = []
    count_F2_AAV = []
    count_F3_AAV = []
    count_F4_AAV = []
    sub_min_F1A = []
    sub_min_F2A = []
    sub_min_F3A = []
    sub_min_F4A = []
    sub_min_F1B = []
    sub_min_F2B = []
    sub_min_F3B = []
    sub_min_F4B = []
    sub_maxmin_F1A = []
    sub_maxmin_F2A = []
    sub_maxmin_F3A = []
    sub_maxmin_F4A = []
    sub_maxmin_F1B = []
    sub_maxmin_F2B = []
    sub_maxmin_F3B = []
    sub_maxmin_F4B = []
    AAV_min_F1 = []
    AAV_min_F2 = []
    AAV_min_F3 = []
    AAV_min_F4 = []
    Asum_Leaf = []
    Asub_Leaf = []
    Amax_Leaf = []
    Amin_Leaf = []
    Bsum_Leaf = []
    Bsub_Leaf = []
    Bmax_Leaf = []
    Bmin_Leaf = []
    sub_Leaf_F1A = []
    sub_Leaf_F1B = []
    sub_Leaf_F2A = []
    sub_Leaf_F2B = []
    sub_Leaf_F3A = []
    sub_Leaf_F3B = []
    sub_Leaf_F4A = []
    sub_Leaf_F4B = []
    AAV_F1 = []
    AAV_F2 = []
    AAV_F3 = []
    AAV_F4 = []
    CP_W1 = []
    CP_W2 = []
    CP_W3 = []
    CP_W4 = []
    CP_W1_F1 = []
    CP_W2_F2 = []
    CP_W3_F3 = []
    CP_W4_F4 = []
    AAVF1 = []
    AAVF2 = []
    AAVF3 = []
    AAVF4 = []
    LSVF1 = []
    LSVF2 = []
    LSVF3 = []
    LSVF4 = []
    MCS1 = []
    MCS2 = []
    MCS3 = []
    MCS4 = []
    MCSF1 = []
    MCSF2 = []
    MCSF3 = []
    MCSF4 = []
    MCS_F1 = []
    MCS_F2 = []
    MCS_F3 = []
    MCS_F4 = []
    MCS = []
    CP_sum = []
    # test欄
    # Jawtracking非対応
    # 4arcまで対応
    # df = pydicom.read_file("default.dcm")
    FILE = dirname + '/' + 'DICOM_data.xls'
    book = xlwt.Workbook()
    beam_number = df.FractionGroupSequence[0].NumberOfBeams
    data_name = ['Jaw_position', 'MLC_position',
                    'MU_data', 'weight_data', 'MU_CP', 'MCS', 'JTCS']
    for i in range(len(data_name)):
        data_name[i] = book.add_sheet(data_name[i])

    for i in range(beam_number):
        CP = df.BeamSequence[i].NumberOfControlPoints
        CP_sum.append(CP)

    CP_sum = sum(CP_sum)

    if beam_number == 1:
        F1_CP = df.BeamSequence[0].NumberOfControlPoints
    elif beam_number == 2:
        F1_CP = df.BeamSequence[0].NumberOfControlPoints
        F2_CP = df.BeamSequence[1].NumberOfControlPoints
    elif beam_number == 3:
        F1_CP = df.BeamSequence[0].NumberOfControlPoints
        F2_CP = df.BeamSequence[1].NumberOfControlPoints
        F3_CP = df.BeamSequence[2].NumberOfControlPoints
    elif beam_number == 4:
        F1_CP = df.BeamSequence[0].NumberOfControlPoints
        F2_CP = df.BeamSequence[1].NumberOfControlPoints
        F3_CP = df.BeamSequence[2].NumberOfControlPoints
        F4_CP = df.BeamSequence[3].NumberOfControlPoints

    for i in range(4):
        for j in range(5):
            data_name[j+2].write(0, i, ("F"+str(i+1)))

    data_name[0].write(0, 0, str('X1'))
    data_name[0].write(0, 1, str('X2'))
    data_name[0].write(0, 2, str('Y1'))
    data_name[0].write(0, 3, str('Y2'))
    data_name[5].write(0, 4, str('All'))
    data_name[6].write(0, 4, str('All'))

    for i in range(60):
        data_name[1].write(0, i, ("A"+str(i+1)))
        data_name[1].write(0, (i+60), ("B"+str(i+1)))

    # jaw
    for i in range(beam_number):
        for j in range(df.BeamSequence[i].NumberOfControlPoints):
            jaw_X = df.BeamSequence[i].ControlPointSequence[j].BeamLimitingDevicePositionSequence[0].LeafJawPositions
            data_Jaw_X.append(jaw_X)
            jaw_Y = df.BeamSequence[i].ControlPointSequence[j].BeamLimitingDevicePositionSequence[1].LeafJawPositions
            data_Jaw_Y.append(jaw_Y)

    for i in range(CP_sum):
        data_name[0].write(i+1, 0, str(data_Jaw_X[i][0]))
        data_name[0].write(i+1, 1, str(data_Jaw_X[i][1]))
        data_name[0].write(i+1, 2, str(data_Jaw_Y[i][0]))
        data_name[0].write(i+1, 3, str(data_Jaw_Y[i][1]))

    # MLC position
    for i in range(beam_number):
        for j in range(df.BeamSequence[i].NumberOfControlPoints):
            mlc_position = df.BeamSequence[i].ControlPointSequence[
                j].BeamLimitingDevicePositionSequence[2].LeafJawPositions
            data_MLC.append(mlc_position)

    for i in range(CP_sum):
        for j in range(120):  # 120➡MLC枚数
            data_name[1].write(i+1, j, str(data_MLC[i][j]))

    # MU_data
    for i in range(beam_number):
        MU = df.FractionGroupSequence[0].ReferencedBeamSequence[i].BeamMeterset
        data_MU.append(MU)

    for i in range(beam_number):
        if i == 0:
            MU1 = data_MU[0]
        elif i == 1:
            MU2 = data_MU[1]
        elif i == 2:
            MU3 = data_MU[2]
        elif i == 3:
            MU4 = data_MU[3]

    for i in range(beam_number):
        data_name[2].write(1, i, str(data_MU[i]))

    MU = sum(data_MU)

    # Weight_data
    for i in range(beam_number):
        for j in range(df.BeamSequence[i].NumberOfControlPoints):
            weight = df.BeamSequence[i].ControlPointSequence[j].CumulativeMetersetWeight
            data_Weight.append(weight)

    for i in range(beam_number):
        if i == 0:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                data_name[3].write(j+1, 0, str(data_Weight[j]))
        elif i == 1:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                data_name[3].write(j+1, 1, str(data_Weight[F1_CP+j]))
        elif i == 2:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                data_name[3].write(j+1, 2, str(data_Weight[F1_CP+F2_CP+j]))
        elif i == 3:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                data_name[3].write(
                    j+1, 3, str(data_Weight[F1_CP+F2_CP+F3_CP+j]))

    # MU/CP
    for i in range(beam_number):
        if i == 0:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                F1.append(data_MU[0]*data_Weight[j])
        elif i == 1:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                F2.append(data_MU[1]*data_Weight[F1_CP+j])
        elif i == 2:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                F3.append(data_MU[2]*data_Weight[F1_CP+F2_CP+j])
        elif i == 3:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                F4.append(data_MU[3]*data_Weight[F1_CP+F2_CP+F3_CP+j])

    for i in range(beam_number):
        if i == 0:
            for j in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
                data_name[4].write(j+1, 0, str(F1[j+1] - F1[j]))
                CP_W1.append(F1[j+1] - F1[j])
        elif i == 1:
            for j in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
                data_name[4].write(j+1, 1, str(F2[j+1] - F2[j]))
                CP_W2.append(F2[j+1] - F2[j])
        elif i == 2:
            for j in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
                data_name[4].write(j+1, 2, str(F3[j+1] - F3[j]))
                CP_W3.append(F3[j+1] - F3[j])
        elif i == 3:
            for j in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
                data_name[4].write(j+1, 3, str(F4[j+1] - F4[j]))
                CP_W4.append(F4[j+1] - F4[j])

    CP_W1.append(0)
    CP_W2.append(0)
    CP_W3.append(0)
    CP_W4.append(0)

    # MCS
    Jaw_ref = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75,
                80, 85, 90, 95, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
    Jaw_ref2 = [0, -5, -10, -15, -20, -25, -30, -35, -40, -45, -50, -55, -60, -65, -70, -
                75, -80, -85, -90, -95, -100, -110, -120, -130, -140, -150, -160, -170, -180, -190, -200]

    # Y2のJawサイズを0~30の数値に変換
    for i in range(CP_sum):
        for j in range(len(Jaw_ref)):
            if Jaw_ref[j] < data_Jaw_Y[i][1] <= Jaw_ref[j+1]:
                Y2jaw.append(j)

    # Y1のJawサイズを0~30の数値に変換
    for i in range(CP_sum):
        for j in range(len(Jaw_ref2)):
            if Jaw_ref2[j] > data_Jaw_Y[i][0] >= Jaw_ref2[j+1]:
                Y1jaw.append(j)

    # Y１_Abank(0~30)
    for i in range(CP_sum):
        for j in range(30):
            if Y1jaw[i] == j:
                LSV_catYjaw2.append(LSV_catjaw2)
                LSV_catjaw2 = []
                for k in range(30):
                    if j == k:
                        for h in range((29-k), 30, 1):
                            LSV_catjaw2.append(data_MLC[i][h])

    LSV_catYjaw2.append(LSV_catjaw2)
    LSV_catYjaw2.pop(0)

    # Y1_Bbank(60~90)
    for i in range(CP_sum):
        for j in range(30):
            if Y1jaw[i] == j:
                LSV_catYjaw3.append(LSV_catjaw2)
                LSV_catjaw2 = []
                for k in range(30):
                    if j == k:
                        for h in range((89-k), 90, 1):
                            LSV_catjaw2.append(data_MLC[i][h])

    LSV_catYjaw3.append(LSV_catjaw2)
    LSV_catYjaw3.pop(0)

    # Y2_Abank(30~60)
    for i in range(CP_sum):
        for j in range(30):
            if Y2jaw[i] == j:
                LSV_catYjaw1.append(LSV_catjaw1)
                LSV_catjaw1 = []
                for k in range(30):
                    if j == k:
                        for h in range(30, (31+k), 1):
                            LSV_catjaw1.append(data_MLC[i][h])

    LSV_catYjaw1.append(LSV_catjaw1)
    LSV_catYjaw1.pop(0)

    # Y2_Bbank(90~120)
    for i in range(CP_sum):
        for j in range(30):
            if Y2jaw[i] == j:
                LSV_catYjaw4.append(LSV_catjaw1)
                LSV_catjaw1 = []
                for k in range(30):
                    if j == k:
                        for h in range(90, (91+k), 1):
                            LSV_catjaw1.append(data_MLC[i][h])

    LSV_catYjaw4.append(LSV_catjaw1)
    LSV_catYjaw4.pop(0)

    # AbankとBbank
    for i in range(CP_sum):
        LSV_A.append(LSV_catYjaw2[i]+LSV_catYjaw1[i])
        LSV_B.append(LSV_catYjaw3[i]+LSV_catYjaw4[i])

    # LSV
    for i in range(CP_sum):
        MLC_Abank.append(lista)
        lista = []
        for j in range(len(LSV_A[i])-1):
            a1 = (LSV_A[i][j])
            a2 = (LSV_A[i][j+1])
            lista.append(abs(a1-a2))

    MLC_Abank.append(lista)
    MLC_Abank.pop(0)

    for i in range(CP_sum):
        MLC_Bbank.append(listb)
        listb = []
        for r in range(len(LSV_B[i])-1):
            b1 = (LSV_B[i][r])
            b2 = (LSV_B[i][r+1])
            listb.append(abs(b1-b2))

    MLC_Bbank.append(listb)
    MLC_Bbank.pop(0)

    for i in range(beam_number):
        if i == 0:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                MLC_Abank_F1.append(MLC_Abank[j])
                MLC_Bbank_F1.append(MLC_Bbank[j])
        elif i == 1:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                MLC_Abank_F2.append(MLC_Abank[F1_CP+j])
                MLC_Bbank_F2.append(MLC_Bbank[F1_CP+j])
        elif i == 2:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                MLC_Abank_F3.append(MLC_Abank[F1_CP+F2_CP+j])
                MLC_Bbank_F3.append(MLC_Bbank[F1_CP+F2_CP+j])
        elif i == 3:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                MLC_Abank_F4.append(MLC_Abank[F1_CP+F2_CP+F3_CP+j])
                MLC_Bbank_F4.append(MLC_Bbank[F1_CP+F2_CP+F3_CP+j])

    # Abank
    for i in range(CP_sum):
        Asum_Leaf.append((LSV_catYjaw2[i])+(LSV_catYjaw1[i]))
        Amax_Leaf.append(max((Asum_Leaf[i])))
        Amin_Leaf.append(min((Asum_Leaf[i])))
        Asub_Leaf.append((Amax_Leaf[i])-(Amin_Leaf[i]))

    # Bbank
    for i in range(CP_sum):
        Bsum_Leaf.append((LSV_catYjaw3[i])+(LSV_catYjaw4[i]))
        Bmax_Leaf.append(max((Bsum_Leaf[i])))
        Bmin_Leaf.append(min((Bsum_Leaf[i])))
        Bsub_Leaf.append((Bmax_Leaf[i])-(Bmin_Leaf[i]))

    for i in range(beam_number):
        if i == 0:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                sub_Leaf_F1A.append(Asub_Leaf[j])
                sub_Leaf_F1B.append(Bsub_Leaf[j])
        elif i == 1:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                sub_Leaf_F2A.append(Asub_Leaf[F1_CP+j])
                sub_Leaf_F2B.append(Bsub_Leaf[F1_CP+j])
        elif i == 2:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                sub_Leaf_F3A.append(Asub_Leaf[F1_CP+F2_CP+j])
                sub_Leaf_F3B.append(Bsub_Leaf[F1_CP+F2_CP+j])
        elif i == 3:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                sub_Leaf_F4A.append(Asub_Leaf[F1_CP+F2_CP+F3_CP+j])
                sub_Leaf_F4B.append(Bsub_Leaf[F1_CP+F2_CP+F3_CP+j])

    for i in range(beam_number):
        if i == 0:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                lista1 = []
                listb1 = []
                sum_F1_A_MLC.append(lista1)
                sum_F1_B_MLC.append(listb1)
                for r in range(len(MLC_Abank_F1[j])):
                    lista1.append(sub_Leaf_F1A[j]-MLC_Abank_F1[j][r])
                for r in range(len(MLC_Bbank_F1[j])):
                    listb1.append(sub_Leaf_F1B[j]-MLC_Bbank_F1[j][r])
        elif i == 1:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                lista2 = []
                listb2 = []
                sum_F2_A_MLC.append(lista2)
                sum_F2_B_MLC.append(listb2)
                for r in range(len(MLC_Abank_F2[j])):
                    lista2.append(sub_Leaf_F2A[j]-MLC_Abank_F2[j][r])
                for r in range(len(MLC_Bbank_F2[j])):
                    listb2.append(sub_Leaf_F2B[j]-MLC_Bbank_F2[j][r])
        elif i == 2:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                lista3 = []
                listb3 = []
                sum_F3_A_MLC.append(lista3)
                sum_F3_B_MLC.append(listb3)
                for r in range(len(MLC_Abank_F3[j])):
                    lista3.append(sub_Leaf_F3A[j]-MLC_Abank_F3[j][r])
                for r in range(len(MLC_Bbank_F3[j])):
                    listb3.append(sub_Leaf_F3B[j]-MLC_Bbank_F3[j][r])
        elif i == 3:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                lista4 = []
                listb4 = []
                sum_F4_A_MLC.append(lista4)
                sum_F4_B_MLC.append(listb4)
                for r in range(len(MLC_Abank_F4[j])):
                    lista4.append(sub_Leaf_F4A[j]-MLC_Abank_F4[j][r])
                for r in range(len(MLC_Bbank_F4[j])):
                    listb4.append(sub_Leaf_F4B[j]-MLC_Bbank_F4[j][r])

    # SUM
    for i in range(beam_number):
        if i == 0:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                sum_F1_A.append(sum(sum_F1_A_MLC[j]))
                sum_F1_B.append(sum(sum_F1_B_MLC[j]))
        elif i == 1:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                sum_F2_A.append(sum(sum_F2_A_MLC[j]))
                sum_F2_B.append(sum(sum_F2_B_MLC[j]))
        elif i == 2:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                sum_F3_A.append(sum(sum_F3_A_MLC[j]))
                sum_F3_B.append(sum(sum_F3_B_MLC[j]))
        elif i == 3:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                sum_F4_A.append(sum(sum_F4_A_MLC[j]))
                sum_F4_B.append(sum(sum_F4_B_MLC[j]))

    for i in range(beam_number):
        if i == 0:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                count_F1_A.append(len(MLC_Abank_F1[j]))
                count_F1_B.append(len(MLC_Bbank_F1[j]))
        elif i == 1:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                count_F2_A.append(len(MLC_Abank_F2[j]))
                count_F2_B.append(len(MLC_Bbank_F2[j]))
        elif i == 2:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                count_F3_A.append(len(MLC_Abank_F3[j]))
                count_F3_B.append(len(MLC_Bbank_F3[j]))
        elif i == 3:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                count_F4_A.append(len(MLC_Abank_F4[j]))
                count_F4_B.append(len(MLC_Bbank_F4[j]))

    for i in range(beam_number):
        if i == 0:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                sum_max_F1_A.append(count_F1_A[j]*sub_Leaf_F1A[j])
                sum_max_F1_B.append(count_F1_B[j]*sub_Leaf_F1B[j])
        elif i == 1:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                sum_max_F2_A.append(count_F2_A[j]*sub_Leaf_F2A[j])
                sum_max_F2_B.append(count_F2_B[j]*sub_Leaf_F2B[j])
        elif i == 2:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                sum_max_F3_A.append(count_F3_A[j]*sub_Leaf_F3A[j])
                sum_max_F3_B.append(count_F3_B[j]*sub_Leaf_F3B[j])
        elif i == 3:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                sum_max_F4_A.append(count_F4_A[j]*sub_Leaf_F4A[j])
                sum_max_F4_B.append(count_F4_B[j]*sub_Leaf_F4B[j])

    for i in range(beam_number):
        if i == 0:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                LSV_F1A.append(sum_F1_A[j]/sum_max_F1_A[j])
                LSV_F1B.append(sum_F1_B[j]/sum_max_F1_B[j])
        elif i == 1:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                LSV_F2A.append(sum_F2_A[j]/sum_max_F2_A[j])
                LSV_F2B.append(sum_F2_B[j]/sum_max_F2_B[j])
        elif i == 2:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                LSV_F3A.append(sum_F3_A[j]/sum_max_F3_A[j])
                LSV_F3B.append(sum_F3_B[j]/sum_max_F3_B[j])
        elif i == 3:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                LSV_F4A.append(sum_F4_A[j]/sum_max_F4_A[j])
                LSV_F4B.append(sum_F4_B[j]/sum_max_F4_B[j])

    for i in range(beam_number):
        if i == 0:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                LSV_F1_CP.append(LSV_F1A[j]*LSV_F1B[j])
        elif i == 1:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                LSV_F2_CP.append(LSV_F2A[j]*LSV_F2B[j])
        elif i == 2:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                LSV_F3_CP.append(LSV_F3A[j]*LSV_F3B[j])
        elif i == 3:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                LSV_F4_CP.append(LSV_F4A[j]*LSV_F4B[j])

    # AAV
    Y1jaw_mlc = []
    Y2jaw_mlc = []
    LSV_catjawA1 = []
    LSV_catYjawA1 = []
    LSV_catjawA2 = []
    LSV_catYjawA2 = []
    LSV_catjawA3 = []
    LSV_catYjawA3 = []
    LSV_catjawA4 = []
    LSV_catYjawA4 = []
    for i in range(len(Y1jaw)):
        Y1jaw_mlcA = 29 - Y1jaw[i]
        Y1jaw_mlc.append(Y1jaw_mlcA)
        Y1jaw_mlcB = 29 - Y1jaw[i]
        Y2jaw_mlc.append(Y1jaw_mlcB)

    # Y１_Abank(0~30)
    for i in range(CP_sum):
        LSV_catYjawA2.append(LSV_catjawA2)
        LSV_catjawA2 = []
        for r in range(30):
            if (Y1jaw_mlc[i]) > r:
                LSV_catjawA2.append(0)
            elif (Y1jaw_mlc[i]) == r:
                for h in range((30-(30-r)), 30, 1):
                    LSV_catjawA2.append(data_MLC[i][h])
            else:
                break

    LSV_catYjawA2.append(LSV_catjawA2)
    LSV_catYjawA2.pop(0)

    # Y1_Bbank(60~90)
    for i in range(CP_sum):
        LSV_catYjawA3.append(LSV_catjawA3)
        LSV_catjawA3 = []
        for r in range(30):
            if Y1jaw_mlc[i] > r:
                LSV_catjawA3.append(0)
            elif Y1jaw_mlc[i] == r:
                for h in range((89-(29-r)), 90, 1):
                    LSV_catjawA3.append(data_MLC[i][h])
            else:
                break

    LSV_catYjawA3.append(LSV_catjawA3)
    LSV_catYjawA3.pop(0)

    # Y2_Abank(30~60)
    for i in range(CP_sum):
        LSV_catYjawA1.append(LSV_catjawA1)
        LSV_catjawA1 = []
        for r in range(30):
            if Y2jaw[i] > r:
                pass
            elif Y2jaw[i] == r:
                for h in range(30, (31+r), 1):
                    LSV_catjawA1.append(data_MLC[i][h])
            else:
                LSV_catjawA1.append(0)

    LSV_catYjawA1.append(LSV_catjawA1)
    LSV_catYjawA1.pop(0)

    # Y2_Bbank(90~120)
    for i in range(CP_sum):
        LSV_catYjawA4.append(LSV_catjawA4)
        LSV_catjawA4 = []
        for r in range(30):
            if Y2jaw[i] > r:
                pass
            elif Y2jaw[i] == r:
                for h in range(90, (91+r), 1):
                    LSV_catjawA4.append(data_MLC[i][h])
            else:
                LSV_catjawA4.append(0)

    LSV_catYjawA4.append(LSV_catjawA4)
    LSV_catYjawA4.pop(0)

    # AbankとBbank
    LSV_A1x = []
    LSV_A2x = []
    LSV_A3x = []
    LSV_A4x = []
    LSV_B1x = []
    LSV_B2x = []
    LSV_B3x = []
    LSV_B4x = []

    for i in range(beam_number):
        if i == 0:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                LSV_A1x.append(LSV_catYjawA2[j]+LSV_catYjawA1[j])
                LSV_B1x.append(LSV_catYjawA3[j]+LSV_catYjawA4[j])
        elif i == 1:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                LSV_A2x.append(
                    LSV_catYjawA2[F1_CP+j]+LSV_catYjawA1[F1_CP+j])
                LSV_B2x.append(
                    LSV_catYjawA3[F1_CP+j]+LSV_catYjawA4[F1_CP+j])
        elif i == 2:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                LSV_A3x.append(
                    LSV_catYjawA2[F1_CP+F2_CP+j]+LSV_catYjawA1[F1_CP+F2_CP+j])
                LSV_B3x.append(
                    LSV_catYjawA3[F1_CP+F2_CP+j]+LSV_catYjawA4[F1_CP+F2_CP+j])
        elif i == 3:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                LSV_A4x.append(
                    LSV_catYjawA2[F1_CP+F2_CP+F3_CP+j]+LSV_catYjawA1[F1_CP+F2_CP+F3_CP+j])
                LSV_B4x.append(
                    LSV_catYjawA3[F1_CP+F2_CP+F3_CP+j]+LSV_catYjawA4[F1_CP+F2_CP+F3_CP+j])

    lsv_A1x = []
    lsv_A2x = []
    lsv_A3x = []
    lsv_A4x = []
    lsv_B1x = []
    lsv_B2x = []
    lsv_B3x = []
    lsv_B4x = []
    lsv_A1xx = []
    lsv_A2xx = []
    lsv_A3xx = []
    lsv_A4xx = []
    lsv_B1xx = []
    lsv_B2xx = []
    lsv_B3xx = []
    lsv_B4xx = []
    for i in range(beam_number):
        if i == 0:
            for k in range(60):
                lsv_A1x.append(lsv_A1xx)
                lsv_A1xx = []
                lsv_B1x.append(lsv_B1xx)
                lsv_B1xx = []
                for j in range(df.BeamSequence[i].NumberOfControlPoints):
                    lsv_A1xx.append(LSV_A1x[j][k])
                    lsv_B1xx.append(LSV_B1x[j][k])
            lsv_A1x.append(lsv_A1xx)
            lsv_A1x.pop(0)
            lsv_B1x.append(lsv_B1xx)
            lsv_B1x.pop(0)
        elif i == 1:
            for k in range(60):
                lsv_A2x.append(lsv_A2xx)
                lsv_A2xx = []
                lsv_B2x.append(lsv_B2xx)
                lsv_B2xx = []
                for j in range(df.BeamSequence[i].NumberOfControlPoints):
                    lsv_A2xx.append(LSV_A2x[j][k])
                    lsv_B2xx.append(LSV_B2x[j][k])
            lsv_A2x.append(lsv_A2xx)
            lsv_A2x.pop(0)
            lsv_B2x.append(lsv_B2xx)
            lsv_B2x.pop(0)
        elif i == 2:
            for k in range(60):
                lsv_A3x.append(lsv_A3xx)
                lsv_A3xx = []
                lsv_B3x.append(lsv_B3xx)
                lsv_B3xx = []
                for j in range(df.BeamSequence[i].NumberOfControlPoints):
                    lsv_A3xx.append(LSV_A3x[j][k])
                    lsv_B3xx.append(LSV_B3x[j][k])
            lsv_A3x.append(lsv_A3xx)
            lsv_A3x.pop(0)
            lsv_B3x.append(lsv_B3xx)
            lsv_B3x.pop(0)
        elif i == 3:
            for k in range(60):
                lsv_A4x.append(lsv_A4xx)
                lsv_A4xx = []
                lsv_B4x.append(lsv_B4xx)
                lsv_B4xx = []
                for j in range(df.BeamSequence[i].NumberOfControlPoints):
                    lsv_A4xx.append(LSV_A4x[j][k])
                    lsv_B4xx.append(LSV_B4x[j][k])
            lsv_A4x.append(lsv_A4xx)
            lsv_A4x.pop(0)
            lsv_B4x.append(lsv_B4xx)
            lsv_B4x.pop(0)

    lsv_A1min = []
    lsv_A2min = []
    lsv_A3min = []
    lsv_A4min = []
    lsv_B1max = []
    lsv_B2max = []
    lsv_B3max = []
    lsv_B4max = []

    for i in range(beam_number):
        if i == 0:
            for j in range(60):
                lsv_A1min.append(min(lsv_A1x[j]))
                lsv_B1max.append(max(lsv_B1x[j]))
        elif i == 1:
            for j in range(60):
                lsv_A2min.append(min(lsv_A2x[j]))
                lsv_B2max.append(max(lsv_B2x[j]))
        elif i == 2:
            for j in range(60):
                lsv_A3min.append(min(lsv_A3x[j]))
                lsv_B3max.append(max(lsv_B3x[j]))
        elif i == 3:
            for j in range(60):
                lsv_A4min.append(min(lsv_A4x[j]))
                lsv_B4max.append(max(lsv_B4x[j]))

    lsv_A1min = np.array(lsv_A1min)
    lsv_A2min = np.array(lsv_A2min)
    lsv_A3min = np.array(lsv_A3min)
    lsv_A4min = np.array(lsv_A4min)
    lsv_B1max = np.array(lsv_B1max)
    lsv_B2max = np.array(lsv_B2max)
    lsv_B3max = np.array(lsv_B3max)
    lsv_B4max = np.array(lsv_B4max)
    for i in range(beam_number):
        if i == 0:
            AAV_min_F1 = (lsv_A1min)-(lsv_B1max)
        elif i == 1:
            AAV_min_F2 = (lsv_A2min)-(lsv_B2max)
        elif i == 2:
            AAV_min_F3 = (lsv_A3min)-(lsv_B3max)
        elif i == 3:
            AAV_min_F4 = (lsv_A4min)-(lsv_B4max)

    for i in range(beam_number):
        if i == 0:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                MLC_data_F1A.append(LSV_A[j])
                MLC_data_F1B.append(LSV_B[j])
        elif i == 1:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                MLC_data_F2A.append(LSV_A[F1_CP+j])
                MLC_data_F2B.append(LSV_B[F1_CP+j])
        elif i == 2:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                MLC_data_F3A.append(LSV_A[F1_CP+F2_CP+j])
                MLC_data_F3B.append(LSV_B[F1_CP+F2_CP+j])
        elif i == 3:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                MLC_data_F4A.append(LSV_A[F1_CP+F2_CP+F3_CP+j])
                MLC_data_F4B.append(LSV_B[F1_CP+F2_CP+F3_CP+j])

    for i in range(beam_number):
        if i == 0:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                lista1 = []
                AAV_sub_F1.append(lista1)
                for r in range(len(MLC_data_F1A[j])):
                    lista1.append(MLC_data_F1A[j][r]-MLC_data_F1B[j][r])
        elif i == 1:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                lista2 = []
                AAV_sub_F2.append(lista2)
                for r in range(len(MLC_data_F2A[j])):
                    lista2.append(MLC_data_F2A[j][r]-MLC_data_F2B[j][r])
        elif i == 2:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                lista3 = []
                AAV_sub_F3.append(lista3)
                for r in range(len(MLC_data_F3A[j])):
                    lista3.append(MLC_data_F3A[j][r]-MLC_data_F3B[j][r])
        elif i == 3:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                lista4 = []
                AAV_sub_F4.append(lista4)
                for r in range(len(MLC_data_F4A[j])):
                    lista4.append(MLC_data_F4A[j][r]-MLC_data_F4B[j][r])

    # SUM
    for i in range(beam_number):
        if i == 0:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                sum_F1_AAV.append(sum(AAV_sub_F1[j]))
        elif i == 1:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                sum_F2_AAV.append(sum(AAV_sub_F2[j]))
        elif i == 2:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                sum_F3_AAV.append(sum(AAV_sub_F3[j]))
        elif i == 3:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                sum_F4_AAV.append(sum(AAV_sub_F4[j]))

    Y1jaw_mlca = []
    Y2jaw_mlca = []
    LSV_catjawA1a = []
    LSV_catYjawA1a = []
    LSV_catjawA2a = []
    LSV_catYjawA2a = []
    LSV_catjawA3a = []
    LSV_catYjawA3a = []
    LSV_catjawA4a = []
    LSV_catYjawA4a = []
    for i in range(len(Y1jaw)):
        Y1jaw_mlcA = 29 - Y1jaw[i]
        Y1jaw_mlca.append(Y1jaw_mlcA)
        Y1jaw_mlcB = 29 - Y1jaw[i]
        Y2jaw_mlca.append(Y1jaw_mlcB)

    # Y１_Abank(0~30)
    for i in range(CP_sum):
        LSV_catYjawA2a.append(LSV_catjawA2a)
        LSV_catjawA2a = []
        for r in range(30):
            if (Y1jaw_mlc[i]) > r:
                LSV_catjawA2a.append(1000.0)
            elif (Y1jaw_mlc[i]) == r:
                for h in range((30-(30-r)), 30, 1):
                    LSV_catjawA2a.append(data_MLC[i][h])
            else:
                break

    LSV_catYjawA2a.append(LSV_catjawA2a)
    LSV_catYjawA2a.pop(0)

    # Y1_Bbank(60~90)
    for i in range(CP_sum):
        LSV_catYjawA3a.append(LSV_catjawA3a)
        LSV_catjawA3a = []
        for r in range(30):
            if Y1jaw_mlc[i] > r:
                LSV_catjawA3a.append(1000.0)
            elif Y1jaw_mlc[i] == r:
                for h in range((89-(29-r)), 90, 1):
                    LSV_catjawA3a.append(data_MLC[i][h])
            else:
                break

    LSV_catYjawA3a.append(LSV_catjawA3a)
    LSV_catYjawA3a.pop(0)

    # Y2_Abank(30~60)
    for i in range(CP_sum):
        LSV_catYjawA1a.append(LSV_catjawA1a)
        LSV_catjawA1a = []
        for r in range(30):
            if Y2jaw[i] > r:
                pass
            elif Y2jaw[i] == r:
                for h in range(30, (31+r), 1):
                    LSV_catjawA1a.append(data_MLC[i][h])
            else:
                LSV_catjawA1a.append(1000.0)

    LSV_catYjawA1a.append(LSV_catjawA1a)
    LSV_catYjawA1a.pop(0)

    # Y2_Bbank(90~120)
    for i in range(CP_sum):
        LSV_catYjawA4a.append(LSV_catjawA4a)
        LSV_catjawA4a = []
        for r in range(30):
            if Y2jaw[i] > r:
                pass
            elif Y2jaw[i] == r:
                for h in range(90, (91+r), 1):
                    LSV_catjawA4a.append(data_MLC[i][h])
            else:
                LSV_catjawA4a.append(1000.0)

    LSV_catYjawA4a.append(LSV_catjawA4a)
    LSV_catYjawA4a.pop(0)

    LSV_A1xa = []
    LSV_A2xa = []
    LSV_A3xa = []
    LSV_A4xa = []
    LSV_B1xa = []
    LSV_B2xa = []
    LSV_B3xa = []
    LSV_B4xa = []

    for i in range(beam_number):
        if i == 0:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                LSV_A1xa.append(LSV_catYjawA2a[j]+LSV_catYjawA1a[j])
                LSV_B1xa.append(LSV_catYjawA3a[j]+LSV_catYjawA4a[j])
        elif i == 1:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                LSV_A2xa.append(
                    LSV_catYjawA2a[F1_CP+j]+LSV_catYjawA1a[F1_CP+j])
                LSV_B2xa.append(
                    LSV_catYjawA3a[F1_CP+j]+LSV_catYjawA4a[F1_CP+j])
        elif i == 2:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                LSV_A3xa.append(
                    LSV_catYjawA2a[F1_CP+F2_CP+j]+LSV_catYjawA1a[F1_CP+F2_CP+j])
                LSV_B3xa.append(
                    LSV_catYjawA3a[F1_CP+F2_CP+j]+LSV_catYjawA4a[F1_CP+F2_CP+j])
        elif i == 3:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                LSV_A4xa.append(
                    LSV_catYjawA2a[F1_CP+F2_CP+F3_CP+j]+LSV_catYjawA1a[F1_CP+F2_CP+F3_CP+j])
                LSV_B4xa.append(
                    LSV_catYjawA3a[F1_CP+F2_CP+F3_CP+j]+LSV_catYjawA4a[F1_CP+F2_CP+F3_CP+j])

    aavsum1 = []
    aavsum1_2 = []
    aavsum2 = []
    aavsum2_2 = []
    aavsum3 = []
    aavsum3_2 = []
    aavsum4 = []
    aavsum4_2 = []

    for i in range(beam_number):
        if i == 0:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                aavsum1.append(aavsum1_2)
                aavsum1_2 = []
                for k in range(60):
                    if LSV_A1xa[j][k] == (1000.0):
                        pass
                    elif LSV_A1xa[j][k] != (1000.0):
                        aavsum1_2.append(AAV_min_F1[k])
            aavsum1.append(aavsum1_2)
            aavsum1.pop(0)
        elif i == 1:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                aavsum2.append(aavsum1_2)
                aavsum2_2 = []
                for k in range(60):
                    if LSV_A2xa[j][k] == (1000.0):
                        pass
                    elif LSV_A2xa[j][k] != (1000.0):
                        aavsum2_2.append(AAV_min_F2[k])
            aavsum2.append(aavsum2_2)
            aavsum2.pop(0)
        elif i == 2:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                aavsum3.append(aavsum3_2)
                aavsum3_2 = []
                for k in range(60):
                    if LSV_A3xa[j][k] == (1000.0):
                        pass
                    elif LSV_A3xa[j][k] != (1000.0):
                        aavsum3_2.append(AAV_min_F3[k])
            aavsum3.append(aavsum3_2)
            aavsum3.pop(0)
        elif i == 3:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                aavsum4.append(aavsum4_2)
                aavsum4_2 = []
                for k in range(60):
                    if LSV_A4xa[j][k] == (1000.0):
                        pass
                    elif LSV_A4xa[j][k] != (1000.0):
                        aavsum4_2.append(AAV_min_F4[k])
            aavsum4.append(aavsum4_2)
            aavsum4.pop(0)

    aavsum1x = []
    aavsum2x = []
    aavsum3x = []
    aavsum4x = []

    for i in range(beam_number):
        if i == 0:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                aavsum1x.append(sum(aavsum1[i]))
        elif i == 1:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                aavsum2x.append(sum(aavsum2[i]))
        elif i == 2:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                aavsum3x.append(sum(aavsum3[i]))
        elif i == 3:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                aavsum4x.append(sum(aavsum4[i]))

    for i in range(beam_number):
        if i == 0:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                AAV_F1.append(sum_F1_AAV[j]/(aavsum1x[j]))
        elif i == 1:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                AAV_F2.append(sum_F2_AAV[j]/(aavsum2x[j]))
        elif i == 2:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                AAV_F3.append(sum_F3_AAV[j]/(aavsum3x[j]))
        elif i == 3:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                AAV_F4.append(sum_F4_AAV[j]/(aavsum4x[j]))

    for i in range(beam_number):
        if i == 0:
            for j in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
                CP_W1_F1.append((CP_W1[j]+CP_W1[j+1])/MU1)
        elif i == 1:
            for j in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
                CP_W2_F2.append((CP_W2[j]+CP_W2[j+1])/MU2)
        elif i == 2:
            for j in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
                CP_W3_F3.append((CP_W3[j]+CP_W3[j+1])/MU3)
        elif i == 3:
            for j in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
                CP_W4_F4.append((CP_W4[j]+CP_W4[j+1])/MU4)

    for i in range(beam_number):
        if i == 0:
            for j in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
                AAVF1.append((AAV_F1[j]+AAV_F1[j+1])/2)
                LSVF1.append((LSV_F1_CP[j]+LSV_F1_CP[j+1])/2)
        elif i == 1:
            for j in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
                AAVF2.append((AAV_F2[j]+AAV_F2[j+1])/2)
                LSVF2.append((LSV_F2_CP[j]+LSV_F2_CP[j+1])/2)
        elif i == 2:
            for j in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
                AAVF3.append((AAV_F3[j]+AAV_F3[j+1])/2)
                LSVF3.append((LSV_F3_CP[j]+LSV_F3_CP[j+1])/2)
        elif i == 3:
            for j in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
                AAVF4.append((AAV_F4[j]+AAV_F4[j+1])/2)
                LSVF4.append((LSV_F4_CP[j]+LSV_F4_CP[j+1])/2)

    for i in range(beam_number):
        if i == 0:
            for j in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
                MCS1.append(AAVF1[j]*LSVF1[j]*CP_W1_F1[j])
        elif i == 1:
            for j in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
                MCS2.append(AAVF2[j]*LSVF2[j]*CP_W2_F2[j])
        elif i == 2:
            for j in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
                MCS3.append(AAVF3[j]*LSVF3[j]*CP_W3_F3[j])
        elif i == 3:
            for j in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
                MCS4.append(AAVF4[j]*LSVF4[j]*CP_W4_F4[j])

    for i in range(beam_number):
        if i == 0:
            MCSF1 = sum(MCS1)
        elif i == 1:
            MCSF2 = sum(MCS2)
        elif i == 2:
            MCSF3 = sum(MCS3)
        elif i == 3:
            MCSF4 = sum(MCS4)

    for i in range(beam_number):
        if i == 0:
            MCS_F1 = (MCSF1*(MU1/MU))
        elif i == 1:
            MCS_F2 = (MCSF2*(MU2/MU))
        elif i == 2:
            MCS_F3 = (MCSF3*(MU3/MU))
        elif i == 3:
            MCS_F4 = (MCSF4*(MU4/MU))

    if beam_number == 1:
        MCS = (MCS_F1)
    elif beam_number == 2:
        MCS = (MCS_F1+MCS_F2)
    elif beam_number == 3:
        MCS = (MCS_F1+MCS_F2+MCS_F3)
    elif beam_number == 4:
        MCS = (MCS_F1+MCS_F2+MCS_F3+MCS_F4)

    if beam_number == 1:
        data_name[5].write(1, 0, str(MCS_F1))
        data_name[5].write(1, 4, str(MCS))
    elif beam_number == 2:
        data_name[5].write(1, 0, str(MCS_F1))
        data_name[5].write(1, 1, str(MCS_F2))
        data_name[5].write(1, 4, str(MCS))
    elif beam_number == 3:
        data_name[5].write(1, 0, str(MCS_F1))
        data_name[5].write(1, 1, str(MCS_F2))
        data_name[5].write(1, 2, str(MCS_F3))
        data_name[5].write(1, 4, str(MCS))
    elif beam_number == 4:
        data_name[5].write(1, 0, str(MCS_F1))
        data_name[5].write(1, 1, str(MCS_F2))
        data_name[5].write(1, 2, str(MCS_F3))
        data_name[5].write(1, 3, str(MCS_F4))
        data_name[5].write(1, 4, str(MCS))

    jaw_x1 = []
    jaw_x2 = []
    Jaw_X1_1 = []
    Jaw_X1_2 = []
    Jaw_X1_3 = []
    Jaw_X1_4 = []
    Jaw_X2_1 = []
    Jaw_X2_2 = []
    Jaw_X2_3 = []
    Jaw_X2_4 = []
    Jaw_X1_1SUM = []
    Jaw_X1_2SUM = []
    Jaw_X1_3SUM = []
    Jaw_X1_4SUM = []
    Jaw_X2_1SUM = []
    Jaw_X2_2SUM = []
    Jaw_X2_3SUM = []
    Jaw_X2_4SUM = []

    Arc1 = []
    Arc2 = []
    Arc3 = []
    Arc4 = []

    # Jawデータ読み込み
    jaw_x1 = []
    jaw_x2 = []
    for i in range(beam_number):
        for j in range(df.BeamSequence[i].NumberOfControlPoints):
            jaw_X1 = df.BeamSequence[i].ControlPointSequence[j].BeamLimitingDevicePositionSequence[0].LeafJawPositions[0]
            jaw_x1.append(jaw_X1)
            jaw_X2 = df.BeamSequence[i].ControlPointSequence[j].BeamLimitingDevicePositionSequence[0].LeafJawPositions[1]
            jaw_x2.append(jaw_X2)

    # X1,X2のデータ取得
    for i in range(beam_number):
        if i == 0:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                Jaw_X1_1.append(jaw_x1[j])
                Jaw_X2_1.append(jaw_x2[j])
        elif i == 1:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                Jaw_X1_2.append(jaw_x1[F1_CP+j])
                Jaw_X2_2.append(jaw_x2[F1_CP+j])
        elif i == 2:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                Jaw_X1_3.append(jaw_x1[F1_CP+F2_CP+j])
                Jaw_X2_3.append(jaw_x2[F1_CP+F2_CP+j])
        elif i == 3:
            for j in range(df.BeamSequence[i].NumberOfControlPoints):
                Jaw_X1_4.append(jaw_x1[F1_CP+F2_CP+F3_CP+j])
                Jaw_X2_4.append(jaw_x2[F1_CP+F2_CP+F3_CP+j])

    # n-(n+1)を実施
    for i in range(beam_number):
        if i == 0:
            for j in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
                Jaw_X1_1SUM.append(abs(Jaw_X1_1[j]-Jaw_X1_1[j+1]))
                Jaw_X2_1SUM.append(abs(Jaw_X2_1[j]-Jaw_X2_1[j+1]))
        elif i == 1:
            for j in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
                Jaw_X1_2SUM.append(abs(Jaw_X1_2[j]-Jaw_X1_2[j+1]))
                Jaw_X2_2SUM.append(abs(Jaw_X2_2[j]-Jaw_X2_2[j+1]))
        elif i == 2:
            for j in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
                Jaw_X1_3SUM.append(abs(Jaw_X1_3[j]-Jaw_X1_3[j+1]))
                Jaw_X2_3SUM.append(abs(Jaw_X2_3[j]-Jaw_X2_3[j+1]))
        elif i == 3:
            for j in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
                Jaw_X1_4SUM.append(abs(Jaw_X1_4[j]-Jaw_X1_4[j+1]))
                Jaw_X2_4SUM.append(abs(Jaw_X2_4[j]-Jaw_X2_4[j+1]))

    # Arcごとの合算を算出
    for i in range(beam_number):
        if i == 0:
            Jaw_X1_1SUMx = sum(Jaw_X1_1SUM)
            Jaw_X2_1SUMx = sum(Jaw_X2_1SUM)
        elif i == 1:
            Jaw_X1_2SUMx = sum(Jaw_X1_2SUM)
            Jaw_X2_2SUMx = sum(Jaw_X2_2SUM)
        elif i == 2:
            Jaw_X1_3SUMx = sum(Jaw_X1_3SUM)
            Jaw_X2_3SUMx = sum(Jaw_X2_3SUM)
        elif i == 3:
            Jaw_X1_4SUMx = sum(Jaw_X1_4SUM)
            Jaw_X2_4SUMx = sum(Jaw_X2_4SUM)

    # ArcごとのAVERAGEを算出
    for i in range(beam_number):
        if i == 0:
            Jaw_X1_1SUMs = Jaw_X1_1SUMx / len(Jaw_X1_1SUM)
            Jaw_X2_1SUMs = Jaw_X2_1SUMx / len(Jaw_X1_1SUM)
        elif i == 1:
            Jaw_X1_2SUMs = Jaw_X1_2SUMx / len(Jaw_X1_2SUM)
            Jaw_X2_2SUMs = Jaw_X2_2SUMx / len(Jaw_X1_2SUM)
        elif i == 2:
            Jaw_X1_3SUMs = Jaw_X1_3SUMx / len(Jaw_X1_3SUM)
            Jaw_X2_3SUMs = Jaw_X2_3SUMx / len(Jaw_X1_3SUM)
        elif i == 3:
            Jaw_X1_4SUMs = Jaw_X1_4SUMx / len(Jaw_X1_4SUM)
            Jaw_X2_4SUMs = Jaw_X2_4SUMx / len(Jaw_X1_4SUM)

    # ArcごとのJTCSを算出
    for i in range(beam_number):
        if i == 0:
            Arc1 = Jaw_X1_1SUMs + Jaw_X2_1SUMs
        elif i == 1:
            Arc2 = Jaw_X1_2SUMs + Jaw_X2_2SUMs
        elif i == 2:
            Arc3 = Jaw_X1_3SUMs + Jaw_X2_3SUMs
        elif i == 3:
            Arc4 = Jaw_X1_4SUMs + Jaw_X2_4SUMs

    for i in range(beam_number):
        if i == 0:
            JTCS1 = Arc1/(int(df.BeamSequence[i].NumberOfControlPoints)-1)
        elif i == 1:
            JTCS2 = Arc2/(int(df.BeamSequence[i].NumberOfControlPoints)-1)
        elif i == 2:
            JTCS3 = Arc3/(int(df.BeamSequence[i].NumberOfControlPoints)-1)
        elif i == 3:
            JTCS4 = Arc4/(int(df.BeamSequence[i].NumberOfControlPoints)-1)

    # PLANのJTCSを算出
    if i == 0:
        JTCSall = (JTCS1)/beam_number
    elif i == 1:
        JTCSall = (JTCS1+JTCS2)/beam_number
    elif i == 2:
        JTCSall = (JTCS1+JTCS2+JTCS3)/beam_number
    elif i == 3:
        JTCSall = (JTCS1+JTCS2+JTCS3+JTCS4)/beam_number

    if beam_number == 1:
        data_name[6].write(1, 0, str(JTCS1))
        data_name[6].write(1, 4, str(JTCSall))
    elif beam_number == 2:
        data_name[6].write(1, 0, str(JTCS1))
        data_name[6].write(1, 1, str(JTCS2))
        data_name[6].write(1, 4, str(JTCSall))
    elif beam_number == 3:
        data_name[6].write(1, 0, str(JTCS1))
        data_name[6].write(1, 1, str(JTCS2))
        data_name[6].write(1, 2, str(JTCS3))
        data_name[6].write(1, 4, str(JTCSall))
    elif beam_number == 4:
        data_name[6].write(1, 0, str(JTCS1))
        data_name[6].write(1, 1, str(JTCS2))
        data_name[6].write(1, 2, str(JTCS3))
        data_name[6].write(1, 3, str(JTCS4))
        data_name[6].write(1, 4, str(JTCSall))

    book.save(FILE)

root = tk.Tk()  # メインウィンドウの作成
root.geometry('250x150')  # ウィンドウのサイズを設定
root.title('DICOM_Data')  # ウィンドウのタイトルを設定

def callback():
    if tk.messagebox.askyesno('Quit?', '終了する?'):
        root.destory()
        root.protocol('WM_DELETE_WINDOW', callback)

menubar = tk.Menu(root)
root.config(menu=menubar)
filemenu = tk.Menu(menubar)
menubar.add_cascade(label='ファイル', menu=filemenu)
filemenu.add_command(label='閉じる', command=callback)

button1 = tk.Button(root, text='RTplan解析',
                    command=button1_clicked).place(x=86, y=25)

root.mainloop()

