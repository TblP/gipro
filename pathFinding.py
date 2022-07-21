import numpy as np

import dijkstra as dj
import pandas as pd

def overPrice(firstPath,allNudes):
    for i in range(len(firstPath) - 1):
        allNudes[firstPath[i]].update([(firstPath[i + 1], allNudes[firstPath[i]].get(firstPath[i + 1]) + 9000)])
        allNudes[firstPath[i + 1]].update([(firstPath[i], allNudes[firstPath[i + 1]].get(firstPath[i]) + 9000)])

def checkForSameNode2(allnudes,startpos,endpos,secondpath):
    overPrice(secondpath,allnudes)
    alternative = dj.shortest_path(allnudes, start=startpos, end=endpos)
    alternative2 = dj.dijkstra(allnudes, start=startpos, end=endpos)
    altLen = alternative2[0].get(endpos)
    return alternative,altLen

def overPriceIndNode(firstPath,allNudes):
    for i in range(len(firstPath)):
        n = list(allNudes[firstPath[i]].keys())
        for b in range(len(allNudes[firstPath[i]])):
            allNudes[firstPath[i]].update([(n[b], allNudes[firstPath[i]].get(n[b]) + 9000)])

def clearFirstPath(firstPath,allNudes):
    for i in range(len(firstPath) - 1):
        allNudes[firstPath[i]].update([(firstPath[i + 1], allNudes[firstPath[i]].get(firstPath[i + 1]) - 9000)])

def checkForSameNode(samen,allnudes,startpos,endpos,secondpath,firstpath):
    clearFirstPath(firstpath,allnudes)
    overPriceIndNode(samen,allnudes)
    alternative = dj.shortest_path(allnudes, start=startpos, end=endpos)
    alternative2 = dj.dijkstra(allnudes, start=startpos, end=endpos)
    altLen = alternative2[0].get(endpos)
    alternativeSameNode = []
    return checkSameNode(alternative,secondpath,alternativeSameNode), alternative,altLen

def checkSameNode(firstPath,secondPath,sameNudes):
    for i in range(0, len(firstPath)):
        for b in range(0, len(secondPath)):
            if (firstPath[i] == secondPath[b]):
                sameNudes.append(firstPath[i])
                break
            else:
                continue
    return sameNudes

def zapolnenie(df,allNudes):
    for i in range(df.shape[0]):
        allNudes[df['№ т.А'][i]].update([(df['№ т.Б'][i], df['Длина, км'][i])])

    for i in range(df.shape[0]):
        allNudes[df['№ т.Б'][i]].update([(df['№ т.А'][i], df['Длина, км'][i])])

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

        zapolnenie(df,allNudes)

        allNEdes = allNudes.copy()

        firstPath = dj.shortest_path(allNEdes,start=startpos,end=endpos)
        FTest = dj.dijkstra(allNEdes,start=startpos,end=endpos)
        fLen = FTest[0].get(endpos)

        overPrice(firstPath,allNudes)

        STest = dj.dijkstra(allNEdes,start=startpos,end=endpos)
        sLen = STest[0].get(endpos)
        secondPath = dj.shortest_path(allNEdes,start=startpos,end=endpos)

        sameNudes = []
        trueLen = STest[0].get(endpos)

        sameNudes = checkSameNode(firstPath,secondPath,sameNudes)

        sLen -= len(sameNudes) * 9000
        while sLen < 0:
            sLen += 9000
        before = 0
        if (len(sameNudes) > 0):
            if startpos in sameNudes:
                sameNudes.remove(startpos)
                before +=1
            if endpos in sameNudes:
                sameNudes.remove(endpos)
                before += 2
            sameNodes,alt,altLen = checkForSameNode(sameNudes,allNudes,startpos,endpos,secondPath,firstPath)
            if(len(np.intersect1d(sameNudes, sameNodes)) == 0):
                sameNudes = sameNodes
                firstPath = alt
                fLen = altLen
            if startpos not in sameNudes:
                if before == 1 or before == 3:
                    sameNudes.append(startpos)
            if endpos not in sameNudes:
                if before == 2 or before == 3:
                    sameNudes.append(endpos)


        trueLen -= len(sameNudes) * 9000
        while trueLen < 0:
            trueLen += 9000
        if(len(secondPath) == 2 and trueLen > 9000):
            trueLen -= 9000

        if startpos in sameNudes:
            sameNudes.remove(startpos)
        if endpos in sameNudes:
            sameNudes.remove(endpos)

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

    except:
        raise ValueError("bad file")

    df = Connect.copy()

    df = df[["№ т.А", "Регион т.А", "№ т.Б", "Регион т.Б", "Длина, км"]]

    for i in range(df.shape[0]):
        if (df.iloc[i, 0] == startpos):
            a = df.iloc[i, 1]
            break
        if (df.iloc[i, 2] == startpos):
            a = df.iloc[i, 3]
            break

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

    """for i in range(len(firstPath) - 1):

        allNudez[firstPath[i]].update([(firstPath[i + 1], allNudez[firstPath[i]].get(firstPath[i + 1]) + 9000)])
        allNudez[firstPath[i + 1]].update([(firstPath[i], allNudez[firstPath[i + 1]].get(firstPath[i]) + 9000)])"""
    overPrice(firstPath, allNEdes)
    # print(dj.shortest_path(allNEdes,start='N09404',end='N09373'))
    STest = dj.dijkstra(allNEdes, start=startpos, end=endpos)
    sLen = STest[0].get(endpos)
    secondPath = dj.shortest_path(allNEdes, start=startpos, end=endpos)

    sameNudes = []
    trueLen = STest[0].get(endpos)
    sameNudes = checkSameNode(firstPath, secondPath, sameNudes)

    sLen -= len(sameNudes) * 9000
    while sLen < 0:
        sLen += 9000
    before = 0
    if startpos in sameNudes:
        sameNudes.remove(startpos)
        before += 1
    if endpos in sameNudes:
        sameNudes.remove(endpos)
        before += 2
    if (len(sameNudes) > 0):
        sameNodes, alt, altLen = checkForSameNode(sameNudes, allNudez, startpos, endpos, secondPath, firstPath)
        if (len(np.intersect1d(sameNudes, sameNodes)) == 0):
            sameNudes = sameNodes
            firstPath = alt
            fLen = altLen
        if startpos not in sameNudes:
            if before == 1 or before == 3:
                sameNudes.append(startpos)
        if endpos not in sameNudes:
            if before == 2 or before == 3:
                sameNudes.append(endpos)

    trueLen -= len(sameNudes) * 9000
    while trueLen < 0:
        trueLen += 9000

    if (secondPath == firstPath):
        trueLen = fLen
        sLen = fLen

    if startpos in sameNudes:
        sameNudes.remove(startpos)
    if endpos in sameNudes:
        sameNudes.remove(endpos)

    if (len(sameNudes) == 0):
        trueLen = 0





    return firstPath, fLen, secondPath, sLen, sameNudes, trueLen

#print(startInArea('Data.xlsx','N09373','N09404'))