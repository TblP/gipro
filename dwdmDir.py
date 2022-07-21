import copy

import pathFinding as pf
import pandas as pd
import numpy as np
'''def dwdm(file,startpos,endpos):
    try:
        Connect = pd.read_excel(file, sheet_name='Лист1')
    except:
        raise ValueError("bad file")

    df = Connect.copy()
    df.insert(0,'Длина, км',1)

    list1 = df['№ т.А'].tolist()
    list2 = df['№ т.Б'].tolist()
    list3 = list1 + list2
    list3 = list(set(list3))
    allNudes = dict(zip(list3, [dict() for i in range(len(list3))]))

    pf.zapolnenie(df, allNudes)

    firstPathD = pf.dj.shortest_path(allNudes,start=startpos,end=endpos)

    pf.overPrice(firstPathD,allNudes)
    pf.overPriceIndNode(firstPathD,allNudes)

    SecndPathD = pf.dj.shortest_path(allNudes,start=startpos,end=endpos)

    sameNudes = []
    pf.checkSameNode(firstPathD,SecndPathD,sameNudes)

    if startpos in sameNudes:
        sameNudes.remove(startpos)
    if endpos in sameNudes:
        sameNudes.remove(endpos)

    if (len(sameNudes) > 0):
        sameNodes, alt, altLen = pf.checkForSameNode(sameNudes, allNudes, startpos, endpos, SecndPathD, firstPathD)
        if (len(np.intersect1d(sameNudes, sameNodes)) == 0):
            sameNudes = sameNodes
            firstPathD = alt

    return firstPathD,SecndPathD,sameNudes

'''

def dwdm(file,startpos,endpos):
    try:
        Connect = pd.read_excel(file, sheet_name='Лист1')
    except:
        raise ValueError("bad file")

    df = Connect.copy()
    df.insert(0,'Длина, км',1)

    list1 = df['№ т.А'].tolist()
    list2 = df['№ т.Б'].tolist()
    list3 = list1 + list2
    list3 = list(set(list3))
    allNudes = dict(zip(list3, [dict() for i in range(len(list3))]))

    pf.zapolnenie(df, allNudes)

    alnudes2 = copy.deepcopy(allNudes)

    firstPathD = pf.dj.shortest_path(allNudes,start=startpos,end=endpos)

    pf.overPrice(firstPathD,allNudes)
    pf.overPriceIndNode(firstPathD,allNudes)

    SecndPathD = pf.dj.shortest_path(allNudes,start=startpos,end=endpos)

    sameNudes = []
    pf.checkSameNode(firstPathD,SecndPathD,sameNudes)

    if startpos in sameNudes:
        sameNudes.remove(startpos)
    if endpos in sameNudes:
        sameNudes.remove(endpos)

    if (len(sameNudes) > 0):
        sameNodes, alt, altLen = pf.checkForSameNode(sameNudes, allNudes, startpos, endpos, SecndPathD, firstPathD)
        if (len(np.intersect1d(sameNudes, sameNodes)) == 0):
            sameNudes = sameNodes
            firstPathD = alt
        if (len(sameNudes) > 0):
            if startpos in sameNudes:
                sameNudes.remove(startpos)
            if endpos in sameNudes:
                sameNudes.remove(endpos)
            alt, altLen = pf.checkForSameNode2(alnudes2, startpos, endpos, firstPathD)
            SecndPathD = alt
    pf.checkSameNode(firstPathD,SecndPathD,sameNudes)
    return firstPathD,SecndPathD,sameNudes


def repath(file,path):
    fullpath = []
    Len = []
    for i in range(len(path) - 1):
        firstPath, fLen, secondPath, sLen, sameNudes, trueLen = pf.start(file, path[i], path[i + 1])
        fullpath.append(firstPath)
        fullpath.append(secondPath)
        Len.append(fLen)
        Len.append(sLen)
    return fullpath, Len

def bestchoice(q,w,fl,sl):
    path = []
    path2 = []
    l1 = 0
    l2 = 0
    n = min(len(q),len(w))
    b = 0
    for i in range(0, n, 2):
        if i > 0:
            b = 0
        if i == len(q):
            b = 1
        if (len(np.intersect1d(q[i], w[i])) <= b):
            path += q[i]
            l1 += fl[i]
            path2 += w[i]
            l2 += sl[i]
            continue
        elif (len(np.intersect1d(q[i], w[i + 1])) <= b):
            path += q[i]
            l1 += fl[i]
            path2 += w[i + 1]
            l2 += sl[i+1]
            continue
        elif (len(np.intersect1d(q[i + 1], w[i])) <= b):
            path += q[i + 1]
            l1 += fl[i+1]
            path2 += w[i]
            l2 += sl[i]
            continue
        elif (len(np.intersect1d(q[i + 1], w[i + 1])) <= b):
            path += q[i + 1]
            l1 += fl[i+1]
            path2 += w[i + 1]
            l2 += sl[i+1]
            continue
        else:
            a = len(np.intersect1d(q[i], w[i]))
            b = len(np.intersect1d(q[i], w[i + 1]))
            c = len(np.intersect1d(q[i + 1], w[i]))
            d = len(np.intersect1d(q[i + 1], w[i + 1]))
            lng = []
            lng += a, b, c, d
            index = lng.index(min(lng))
            if (index == 0):
                path += q[i]
                l1 += fl[i]
                path2 += w[i]
                l2 += sl[i]
                continue
            if (index == 1):
                path += q[i]
                l1 += fl[i]
                path2 += w[i + 1]
                l2 += sl[i+1]
                continue
            if (index == 2):
                path += q[i + 1]
                l1 += fl[i+1]
                path2 += w[i]
                l2 += sl[i]
                continue
            if (index == 3):
                path += q[i + 1]
                l1 += fl[i + 1]
                path2 += w[i + 1]
                l2 += sl[i + 1]
                continue
    if path2[len(path2) - 1] != path[len(path) - 1]:
        if (len(q) < len(w)):
            for i in range(len(q), len(w), 2):
                if (len(np.intersect1d(path, w[i])) <= 1):
                    path2 += w[i]
                    l2 += sl[i]
                elif (len(np.intersect1d(path, w[i + 1])) <= 1):
                    path2 += w[i + 1]
                    l2 += sl[i+1]
        if (len(w) < len(q)):
            for i in range(len(w), len(q), 2):
                if (len(np.intersect1d(path2, q[i])) <= 1):
                    path += q[i]
                    l1 += fl[i]
                elif (len(np.intersect1d(path2, q[i + 1])) <= 1):
                    path += q[i + 1]
                    l1 += fl[i + 1]

    again = []
    for i in range(len(path) - 1):
        if (path[i] == path[i + 1]):
            again.append(path[i])
    for i in range(len(again)):
        path.remove(again[i])
    again.clear()
    for i in range(len(path2) - 1):
        if (path2[i] == path2[i + 1]):
            again.append(path2[i])
    for i in range(len(again)):
        path2.remove(again[i])



    return path,path2,l1,l2
"""
print(repath(firstPathD))
print(repath(SecndPathD))
"""




