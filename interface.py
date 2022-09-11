import os
import re
import sys
from time import sleep

from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

import dwdmDir as dw
from PyQt5 import QtCore, QtWidgets
import desgn
from pathlib import Path
import pathFinding as pf
import pandas as pd
from threading import *

class ExampleApp(QtWidgets.QMainWindow, desgn.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.enterBtn.clicked.connect(self.openToListen)
        self.startButton.clicked.connect(self.thread)
        self.saveButton.clicked.connect(self.saveListen)
        self.addButton.clicked.connect(self.openNodes)
        self.dwdmBtn.clicked.connect(self.openDWDM)
        self.checkBox.clicked.connect(self.check)

        self.setWindowTitle("C.H.A.I")

        self.excel_data_df = pd.DataFrame()
        self.save_df = pd.DataFrame()

        self.errorLabel.setStyleSheet("QLabel {color : red;}")
        self.startButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.addButton.setEnabled(False)
        self.outareabtn.setChecked(True)
        self.dwdmBtn.setEnabled(False)

        self.pos = 0



    def check(self):
        if (self.checkBox.isChecked()):
            self.dwdmBtn.setEnabled(True)
        else:
            self.dwdmBtn.setEnabled(False)

    def thread(self):
        t1 = Thread(target=self.startListen)
        t2 = Thread(target=self.progress)
        t1.start()
        t2.start()

    def progress(self):
        a = self.excel_data_df.shape[0]-1
        while self.pos != a:
            self.errorLabel.setText(str(self.pos) + " из " + str(self.excel_data_df.shape[0]))
            sleep(0.0001)


    def openToListen(self):

        file, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                        'Open File',
                        './',
                        'py Files (*.xlsx);;Text Files (*.xml)')
        if not file:
            return
        self.readfile = file

        self.addButton.setEnabled(True)


    def startListen(self):

        self.addButton.setEnabled(False)
        self.enterBtn.setEnabled(False)
        self.startButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.inareaBtn.setEnabled(False)
        self.outareabtn.setEnabled(False)
        self.dwdmBtn.setEnabled(False)
        self.checkBox.setEnabled(False)

        a = []

        for i in range(self.excel_data_df.shape[0]):
            a.append(i)

        if (self.checkBox.isChecked()):
            self.save_df = pd.DataFrame(index=a, columns=['Путь1', 'Длина1', 'Путь2', 'Длина2', 'Одинаковые узлы','dwdm1','dwdm2','Возможно плохо обработалось'])
        else:
            self.save_df = pd.DataFrame(index=a, columns=['Путь1', 'Длина1', 'Путь2', 'Длина2', 'Одинаковые узлы'])
        error = []
        for i in range(self.excel_data_df.shape[0]):

            self.pos = i
            dotA = self.excel_data_df.iloc[i,:]
            print(i)
            if(len(dotA[0]) > 0 and len(dotA[1]) > 0):
                self.errorLabel.setText("-")

                sdh = dotA[0]
                mn = dotA[1]

                try:
                    a,b = pf.check(self.readfile,sdh,mn)
                except ValueError as e:
                    self.errorLabel.setText(str(e))
                    return

                if (a == False or b == False):
                    allData = [0, 0, 0, 0, 0, 0]
                    check = 0
                    for i in range(self.save_df.shape[0]):
                        if (str(self.save_df.iat[i, 0]).lower() == 'nan'):
                            for b in range(self.save_df.shape[1]):
                                self.save_df.iat[i, b] = allData[b]
                                check += 1
                        if (check == 5):
                            break
                    continue
            else:
                self.errorLabel.setText("Введите узлы SDH или Main node в правом нижнем углу")
                return

            if(a and b):
                if (self.checkBox.isChecked()):
                    firstPathD,SecndPathD,sameNudesdwdm = dw.dwdm(self.data,sdh,mn)
                    if(firstPathD == 0):
                        allData = [0, 0, 0, 0, 0, 0, 0, 0]
                        check = 0
                        for i in range(self.save_df.shape[0]):
                            if (str(self.save_df.iat[i, 0]).lower() == 'nan'):
                                for b in range(self.save_df.shape[1]):
                                    self.save_df.iat[i, b] = allData[b]
                                    check += 1
                            if (check == 7):
                                break
                        continue
                    else:
                        fullpath1,flen,error1 = dw.repath(self.readfile,firstPathD,self.data)
                        fullpath2,slen,error1 = dw.repath(self.readfile, SecndPathD,self.data)
                        fullpath1,fullpath2,flen,slen = dw.bestchoice(fullpath1,fullpath2,flen,slen)

                    if(error1 > 0):
                        error.append(i)

                    if sdh not in fullpath1:
                        fullpath1.insert(0, sdh)
                    if mn not in fullpath1:
                        fullpath1.append(mn)

                    if sdh not in fullpath2:
                        fullpath2.insert(0, sdh)
                    if mn not in fullpath2:
                        fullpath2.append(mn)

                    nodes = []
                    pf.checkSameNode(fullpath1,fullpath2,nodes)

                    if sdh in nodes:
                        nodes.remove(sdh)
                    if mn in nodes:
                        nodes.remove(mn)

                    allData = [fullpath1,flen,fullpath2,slen,nodes,firstPathD,SecndPathD,error]

                    check = 0

                    for i in range(self.save_df.shape[0]):
                        if (str(self.save_df.iat[i, 0]).lower() == 'nan'):
                            for b in range(self.save_df.shape[1]-1):
                                self.save_df.iat[i, b] = allData[b]
                                check += 1
                        if (check == 7):
                            break
                    self.save_df.iat[0, 7] = allData[7]

                if(self.outareabtn.isChecked() and self.checkBox.isChecked() == False):
                        self.firstPath, self.fLen, self.secondPath, self.sLen, self.sameNudes, self.trueLen = \
                            pf.start(self.readfile, sdh,mn)

                        allData = [self.firstPath, self.fLen, self.secondPath, self.sLen, self.sameNudes, self.trueLen]
                        check = 0
                        for i in range(self.save_df.shape[0]):
                            if (str(self.save_df.iat[i, 0]).lower() == 'nan'):
                                for b in range(self.save_df.shape[1]):
                                    self.save_df.iat[i, b] = allData[b]
                                    if (self.trueLen != 0):
                                        self.save_df.iat[i, 3] = self.trueLen
                                    check+=1
                            if (check == 5):
                                break

                if (self.inareaBtn.isChecked() and self.checkBox.isChecked() == False):
                        self.firstPath, self.fLen, self.secondPath, self.sLen, self.sameNudes, self.trueLen = \
                            pf.startInArea(self.readfile, sdh,mn)

                        allData = [self.firstPath, self.fLen, self.secondPath, self.sLen, self.sameNudes, self.trueLen]
                        check = 0
                        for i in range(self.save_df.shape[0]):
                            if (str(self.save_df.iat[i, 0]).lower() == 'nan'):
                                for b in range(self.save_df.shape[1]):
                                    self.save_df.iat[i, b] = allData[b]
                                    if (self.trueLen != 0):
                                        self.save_df.iat[i, 3] = self.trueLen
                                    check += 1
                            if (check == 5):
                                break

            else:
                self.errorLabel.setText("Проверьте правильность ввода узлов.(Возможно пробел на конце)")
                return
            sleep(0.0001)

        self.errorLabel.setText("Пути найдены можно сохранять")

        self.saveButton.setEnabled(True)
        self.enterBtn.setEnabled(True)
        self.inareaBtn.setEnabled(True)
        self.outareabtn.setEnabled(True)
        self.dwdmBtn.setEnabled(False)
        self.checkBox.setEnabled(True)
        self.checkBox.setCheckState(False)

    def saveListen(self):
         file2, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                        'Open File',
                        './',
                        'py Files (*.xlsx);;Text Files (*.xml)')
         if not file2:
             return
         writer = pd.ExcelWriter(file2)
         save = self.save_df
         save.to_excel(writer)
         writer.save()
         self.errorLabel.setText("Сохранение прошло успешно")
         self.saveButton.setEnabled(False)

    def openNodes(self):
        file2, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                        'Open File',
                        './',
                        'py Files (*.xlsx);;Text Files (*.xml)')
        if not file2:
            return
        self.startButton.setEnabled(True)
        self.excel_data_df = pd.read_excel(file2)

    def openDWDM(self):
        file2, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                        'Open File',
                        './',
                        'py Files (*.xlsx);;Text Files (*.xml)')
        if not file2:
            return
        self.startButton.setEnabled(True)
        self.data = file2






def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp() # Создаём объект класса ExampleApp
    window.setFixedSize(800,600)
    window.show()  # Показываем окно
    app.exec_()  #и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()