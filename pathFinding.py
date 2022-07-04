import numpy as np

import dijkstra as dj
import pandas as pd

def start(file,startpos,endpos):

        try:
            Connect = pd.read_excel(file, sheet_name='edges')
            data_df = pd.read_excel(file, sheet_name='nodes')
        except:
            raise ValueError("bad file")

        df = data_df.copy()
        list = df['№ узла'].tolist()

        allNudes = dict(zip(list,[dict() for i in range(len(list))]))

        df = Connect.copy()


        for i in range(df.shape[0]):
            allNudes[df['№ т.А'][i]].update([(df['№ т.Б'][i] , df['Длина, км'][i])])

        for i in range(df.shape[0]):
            allNudes[df['№ т.Б'][i]].update([(df['№ т.А'][i] , df['Длина, км'][i])])


        allNEdes = allNudes.copy()
        firstPath = dj.shortest_path(allNEdes,start=startpos,end=endpos)
        FTest = dj.dijkstra(allNEdes,start=startpos,end=endpos)
        fLen = FTest[0].get(endpos)

        for i in range(0,len(firstPath)-1):
            #print(firstPath[i])
            #print(allNudes[firstPath[i]])
            #print(allNudes[firstPath[i]].get(firstPath[i+1]))

            allNudes[firstPath[i]].update([(firstPath[i+1] , allNudes[firstPath[i]].get(firstPath[i+1]) + 9000)])

            #print(allNudes[firstPath[i]])

        #print(dj.shortest_path(allNEdes,start='N09404',end='N09373'))
        STest = dj.dijkstra(allNEdes,start=startpos,end=endpos)
        sLen = STest[0].get(endpos)
        secondPath = dj.shortest_path(allNEdes,start=startpos,end=endpos)

        sameNudes = []
        trueLen = STest[0].get(endpos)
        for i in range(1, len(firstPath) - 1):
            for b in range(1, len(secondPath) - 1):
                if (firstPath[i] == secondPath[b]):
                    sameNudes.append(firstPath[i])
                    trueLen -= 9000
                    break
                else:
                    continue
        if (len(sameNudes) == 0):
            trueLen = 0


        return firstPath,fLen,secondPath,sLen,sameNudes,trueLen

def check(file,startpos,endpos):
    s = False
    e = False
    data_df = pd.read_excel(file, sheet_name='nodes')
    df = data_df.copy()
    listNode = df['№ узла'].tolist()
    for i in range(len(listNode)):
        if(listNode[i] == startpos ):
            s = True
        if(listNode[i] == endpos):
            e = True
    return s,e


def startInArea(file,startpos,endpos):
    try:
        Connect = pd.read_excel(file, sheet_name='edges')
        data_df = pd.read_excel(file, sheet_name='nodes')
    except:
        raise ValueError("bad file")

    df = data_df.copy()
    list = df['№ узла'].tolist()

    allNudes = dict(zip(list, [dict() for i in range(len(list))]))

    df = Connect.copy()

    df = df[["№ т.А", "Регион т.А", "№ т.Б", "Регион т.Б", "Длина, км"]]

    for i in range(df.shape[0]):
        if (df.iloc[i, 0] == "N09373"):
            a = df.iloc[i, 1]

    df_filter = df["Регион т.А"].isin([a])
    areaNudes = df[df_filter]
    list2 = areaNudes['№ т.А'].tolist()
    df_filter = df["Регион т.Б"].isin([a])
    areaNudes = areaNudes[df_filter]
    list2 += areaNudes['№ т.Б'].tolist()

    list2 = set(list2)

    allNudez = dict(zip(list2, [dict() for i in range(len(list2))]))
    areaNudes.reset_index(drop=True, inplace=True)

    for i in range(areaNudes.shape[0]):
        allNudez[areaNudes['№ т.А'][i]].update([(areaNudes['№ т.Б'][i], areaNudes['Длина, км'][i])])

    for i in range(areaNudes.shape[0]):
        allNudez[areaNudes['№ т.Б'][i]].update([(areaNudes['№ т.А'][i], areaNudes['Длина, км'][i])])

    allNEdes = allNudez.copy()
    firstPath = dj.shortest_path(allNEdes, start=startpos, end=endpos)
    FTest = dj.dijkstra(allNEdes, start=startpos, end=endpos)
    fLen = FTest[0].get(endpos)

    for i in range(0, len(firstPath) - 1):
        # print(firstPath[i])
        # print(allNudes[firstPath[i]])
        # print(allNudes[firstPath[i]].get(firstPath[i

        allNudez[firstPath[i]].update([(firstPath[i + 1], allNudez[firstPath[i]].get(firstPath[i + 1]) + 9000)])

        # print(allNudes[firstPath[i]])

    # print(dj.shortest_path(allNEdes,start='N09404',end='N09373'))
    STest = dj.dijkstra(allNEdes, start=startpos, end=endpos)
    sLen = STest[0].get(endpos)
    secondPath = dj.shortest_path(allNEdes, start=startpos, end=endpos)

    sameNudes = []
    trueLen = STest[0].get(endpos)
    for i in range(1, len(firstPath) - 1):
        for b in range(1, len(secondPath) - 1):
            if (firstPath[i] == secondPath[b]):
                sameNudes.append(firstPath[i])
                trueLen -= 9000
                break
            else:
                continue
    if (len(sameNudes) == 0):
        trueLen = 0

    return firstPath, fLen, secondPath, sLen, sameNudes, trueLen

#print(startInArea('Data.xlsx','N09373','N09404'))