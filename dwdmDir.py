import copy
import os
import shutil
import openpyxl as op
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

def correctSample(correctnodes,first,second,path,path2,file):

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

    name = os.path.basename(correctnodes)
    url = os.path.dirname(os.path.realpath(__file__))
    url += r'\{0}'.format(name)
    if(os.path.exists(url)):
        a = url
    else:
        a = shutil.copy(correctnodes,
                        str(os.path.dirname(os.path.realpath(__file__))), follow_symlinks=True)

    try:
        data_df = pd.read_excel(a, sheet_name='nodes')
        data_df2 = pd.read_excel(a, sheet_name='edges')
    except:
        raise ValueError("bad file")
    '''
   df2 = data_df2.copy()

   li1 = df2['№ т.А'].tolist()
   li2 = df2['№ т.Б'].tolist()
   li3 = li1 + li2
   li3 = list(set(li3))

   allNudes2 = dict(zip(li3, [dict() for i in range(len(li3))]))

   pf.zapolnenie(df2, allNudes2)
   '''


    list5 = data_df[['№ узла','Тип узла']]
    g = 0
    q = 0
    b = 0
    u = 0
    node = []
    needDel = []
    pf.checkSameNode(path,path2,node)
    if(len(path) > 0):
        start = first
        while b != len(path):

            ab = list5[list5['№ узла'] == path[b]].index
            ab = ab.to_list()

            if ((list5.iloc[ab[0], 1] == 'OADM' or list5.iloc[ab[0], 1] == 'SDH') and (list5.iloc[ab[0], 0] != first and list5.iloc[ab[0],0 ] != second)):
                checkpoints = pf.dj.shortest_path(allNudes, start, list5.iloc[ab[0], 0])

                if(len(checkpoints) == 2):
                    b += 1
                    start = list5.iloc[ab[0], 0]
                else:
                    if list5.iloc[ab[0], 0] not in node:
                        list5 = list5.drop(index=[ab[0]])
                        list5 = list5.reset_index(drop=True)
                        b += 1
                        g += 1
                    else:
                        needDel.append(list5.iloc[ab[0], 0])
                        b += 1
            elif list5.iloc[ab[0],0 ] == second:
                checkpoints = pf.dj.shortest_path(allNudes, start, list5.iloc[ab[0], 0])
                if (len(checkpoints) != 2):
                    ab = list5[list5['№ узла'] == start].index
                    ab = ab.to_list()
                    list5 = list5.drop(index=[ab[0]])
                    list5 = list5.reset_index(drop=True)
                    b += 1
                    g += 1
                else:
                    b += 1
            else:
                b += 1
    if (len(path2) > 0):
        start = first
        while q != len(path2):
            ab = list5[list5['№ узла'] == path2[q]].index
            ab = ab.to_list()

            if ((list5.iloc[ab[0], 1] == 'OADM' or list5.iloc[ab[0], 1] == 'SDH') and (
                list5.iloc[ab[0], 0] != first and list5.iloc[ab[0], 0] != second)):
                checkpoints = pf.dj.shortest_path(allNudes, start, list5.iloc[ab[0], 0])
                if (len(checkpoints) == 2):
                    q += 1
                    start = list5.iloc[ab[0], 0]
                else:
                    if list5.iloc[ab[0], 0] not in node:
                        list5 = list5.drop(index=[ab[0]])
                        list5 = list5.reset_index(drop=True)
                        q += 1
                        g += 1
                    else:
                        needDel.append(list5.iloc[ab[0], 0])
                        q += 1
            elif list5.iloc[ab[0],0 ] == second:
                checkpoints = pf.dj.shortest_path(allNudes, start, list5.iloc[ab[0], 0])
                if (len(checkpoints) != 2):
                    ab = list5[list5['№ узла'] == start].index
                    ab = ab.to_list()
                    list5 = list5.drop(index=[ab[0]])
                    list5 = list5.reset_index(drop=True)
                    q += 1
                    g += 1
                else:
                    q += 1
            else:
                q += 1

            '''
            try:
                if(list5.iloc[b, 1] == 'OADM' or list5.iloc[b, 1] == 'SDH'):
                    a = pf.dj.shortest_path(allNudes, start=first, end=list5.iloc[b, 0])
                    for l in range(len(a[:-1])):
                        io = pf.dj.shortest_path(allNudes2, start=a[l], end=a[l+1])

                        for i in io[1:-1]:
                            ab = list5[list5['№ узла'] == i].index
                            
                            ab = ab.to_list()

                            if(list5.iloc[ab[0], 1] == 'OADM' or list5.iloc[ab[0], 1] == 'SDH'):
                                for i in range(len(allNudes2)-1):
                                    if list5.iloc[b, 0] in allNudes2.keys():
                                        del allNudes2[list5.iloc[b, 0]]
                                for value in allNudes2.values():
                                    if list5.iloc[b, 0] in value:
                                        value.pop(list5.iloc[b, 0])
                                list5 = list5.drop(index=[ab[0]])
                                list5 = list5.reset_index(drop=True)
                                u += 1

                        if(u > 0 and u < len(a[1:-2])):
                            g += 1

                        if(u == len(a[1:-2])):
                            list5 = list5.drop(index=[b])
                            list5 = list5.reset_index(drop=True)
                            u = 0
                            g += 1
                    b += 1
                else:
                    b+=1
            except KeyError:
                a = 'error'
                list5 = list5.drop(index=[b])
                list5 = list5.reset_index(drop=True)
                g += 1
            '''
        '''
                while i != list5.shape[0]:
            if(list5.iloc[i,0] not in path and (list5.iloc[i, 1] == 'OADM' or list5.iloc[i, 1] == 'SDH')):
                list5 = list5.drop(index=[i])
                list5 = list5.reset_index(drop=True)
                g += 1
            if (list5.iloc[i, 0] not in path2 and (list5.iloc[i, 1] == 'OADM' or list5.iloc[i, 1] == 'SDH')):
                list5 = list5.drop(index=[i])
                list5 = list5.reset_index(drop=True)
                g += 1
            else:
                i += 1
        '''

    again = []
    again.clear()
    for i in range(len(needDel) - 1):
        if (needDel[i] == needDel[i + 1]):
            again.append(needDel[i])
    if (len(again) > 0):
        for i in range(len(again)):
            needDel.remove(again[i])


    if (len(needDel) > 0):
        for need in needDel:
            delit = list5[list5['№ узла'] == need].index
            delit = delit.to_list()
            list5 = list5.drop(index=[delit[0]])
            list5 = list5.reset_index(drop=True)
            g += 1

    if(g>0):
        g = 0
        wb = op.load_workbook(a)
        pfd = wb['nodes']
        wb.remove(pfd)
        wb.save(a)

        with pd.ExcelWriter(a, 'openpyxl', mode='a') as writer:
            writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
            list5.to_excel(writer, 'nodes')
        '''
        if first not in path:
            path.insert(0, first)
        if second not in path:
            path.append(second)
        if second not in path2:
            path2.insert(0, first)
        if second not in path2:
            path2.append(second) 
        '''


        return a
    else:
        '''
        if first not in path:
            path.insert(0, first)
        if second not in path:
            path.append(second)
        if second not in path2:
            path2.insert(0, first)
        if second not in path2:
            path2.append(second)
            '''
        return None

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


def repath(file,path,file3):
    error = 0
    fullpath = []
    Len = []
    file2 = file
    for i in range(len(path) - 1):
        a = False
        firstPath, fLen, secondPath, sLen, sameNudes, trueLen = pf.start(file2, path[i], path[i + 1])
        while a == False:
            file2 = correctSample(file2, path[i], path[i+1],firstPath,secondPath,file3)
            if(file2 != None):
                try:
                    firstPath, fLen, secondPath, sLen, sameNudes, trueLen = pf.start(file2, path[i], path[i + 1])
                except KeyError:
                    a = True
                    file2 = file
                    error = 1
            if(file2 == None):
                a = True
                file2 = file

        again = 0
        for inArray in range(len(fullpath) - 1):
            for i in range(len(firstPath) - 1):
                if (firstPath[i] in fullpath[inArray]):
                    again += 1
                if(again > len(fullpath[inArray])):
                    again = 9000
        if again >= 9000:
            if(len(sameNudes) > 0):
                endpath = firstPath[firstPath.index(sameNudes[len(sameNudes) - 2]):]
                firstPath = secondPath[:secondPath.index(sameNudes[len(sameNudes) - 2])]
                for element in endpath:
                    firstPath.append(element)
                fLen = redistance(file,firstPath)


        again = 0
        for inArray in range(len(fullpath) - 1):
            for i in range(len(secondPath) - 1):
                if (secondPath[i] in fullpath[inArray]):
                    again += 1
                if(again > len(fullpath[inArray])):
                    again = 9000
        if again == 9000:
            if (len(sameNudes) > 0):
                endpath = secondPath[secondPath.index(sameNudes[len(sameNudes)-2]):]
                secondPath = firstPath[:firstPath.index(sameNudes[len(sameNudes)-2])]
                for element in endpath:
                    secondPath.append(element)
                sLen = redistance(file, secondPath)



        fullpath.append(firstPath)
        fullpath.append(secondPath)

        Len.append(fLen)
        Len.append(sLen)

        name = os.path.basename(file)
        url = os.path.dirname(os.path.realpath(__file__))
        url += r'\{0}'.format(name)
        if (os.path.exists(url)):
            os.remove(url)
    return fullpath, Len , error

def bestchoice(q,w,fl,sl):
    path = []
    path2 = []
    l1 = 0
    l2 = 0
    n = min(len(q),len(w))
    b = 1
    for i in range(0, n, 2):
        if i > 0:
            if ((path[0] == q[0][0] and path[len(path) - 1] == q[len(q)-1][len(q[len(q)-1])-1]) or (
                    path2[0] == w[0][0] and path2[len(path2) - 1] == w[len(w)-1][len(w[len(w)-1])-1])):
                b = 1
            else:
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
                if (len(np.intersect1d(path, w[i])) <= b):
                    path2 += w[i]
                    l2 += sl[i]
                elif (len(np.intersect1d(path, w[i + 1])) <= b):
                    path2 += w[i + 1]
                    l2 += sl[i+1]
                else:
                    if(len(np.intersect1d(path, w[i])) < len(np.intersect1d(path, w[i + 1]))):
                        path2 += w[i]
                        l2 += sl[i]
                    else:
                        path2 += w[i+1]
                        l2 += sl[i+1]
        if (len(w) < len(q)):
            for i in range(len(w), len(q), 2):
                if (len(np.intersect1d(path2, q[i])) <= b):
                    path += q[i]
                    l1 += fl[i]
                elif (len(np.intersect1d(path2, q[i + 1])) <= b):
                    path += q[i + 1]
                    l1 += fl[i + 1]
                else:
                    if(len(np.intersect1d(path, q[i])) < len(np.intersect1d(path, q[i + 1]))):
                        path += q[i]
                        l1 += fl[i]
                    else:
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


def redistance(file,path):
    ln = 0
    try:
        Connect = pd.read_excel(file, sheet_name='edges')
    except:
        raise ValueError("bad file")
    list5 = Connect[['№ т.А', '№ т.Б','Длина, км']]
    for i in range(len(path)-1):
        for b in range(list5.shape[0]):
            if(list5.iloc[b, 0] == path[i]) and (list5.iloc[b, 1] == path[i+1]):
                ln += list5.iloc[b, 2]
                break
            if (list5.iloc[b, 1] == path[i]) and (list5.iloc[b, 0] == path[i + 1]):
                ln += list5.iloc[b, 2]
                break

    return ln




