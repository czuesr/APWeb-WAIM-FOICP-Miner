# -*- coding: utf-8 -*-

import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QCoreApplication
import utils
from getOntology import *
from load_data import *

minJaccard = 0.6
OntologyToChar = {'A': "Hotel", 'B': "Hostel", 'C': "Airport", 'D': "Railway_Station", 'E': "Car_Parks", 'F': "Park",
                  'G': "Gymnasium", 'H': "Bubble_tea_shop",
                  'I': "Clothes_Shop", 'J': "Animal_Shop", 'K': "National_Scenic_spots", 'L': "Provincial_Scenic_spots",
                  'M': "Chinese_Restaurant", 'N': "Western_Restaurant"}

listsNum = ['1st', '2nd', '3rd ', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th',
            '15th', '16th', '17th', '18th', '19th', '20th', '21th', '22th']


class Ui_MainWindow(QtWidgets.QMainWindow):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1302, 806)
        MainWindow.setStyleSheet("background.png")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.inOntoButt = QtWidgets.QPushButton(self.centralwidget)
        self.inOntoButt.setGeometry(QtCore.QRect(750, 30, 131, 31))
        self.inOntoButt.setObjectName("inOntoButt")
        self.inOntoButt.clicked.connect(self.openfile)

        self.inDataButt = QtWidgets.QPushButton(self.centralwidget)
        self.inDataButt.setGeometry(QtCore.QRect(750, 80, 131, 31))
        self.inDataButt.setObjectName("inDataButt")
        self.inDataButt.clicked.connect(self.openfile1)

        self.textEditOnto = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditOnto.setGeometry(QtCore.QRect(210, 30, 541, 31))
        self.textEditOnto.setObjectName("textEditOnto")
        self.textEditOnto.setPlaceholderText("Please choose the ontology file")

        self.textEditData = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditData.setGeometry(QtCore.QRect(210, 80, 541, 31))
        self.textEditData.setObjectName("textEditData")
        self.textEditData.setPlaceholderText("Please choose the data file")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 30, 181, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(90, 60, 101, 61))
        self.label_2.setObjectName("label_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(930, 30, 131, 31))
        self.pushButton_3.setStyleSheet("color: green;\n"
                                        "font: 12pt \"Adobe Heiti Std\";")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.startInteractively)

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(1120, 30, 131, 31))
        self.pushButton_4.setStyleSheet("font: 12pt \"Adobe Heiti Std\";\n"
                                        "color: red;")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.stopInteraction)

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(940, 80, 301, 41))
        self.pushButton_5.setStyleSheet("font: 12pt \"Adobe Heiti Std\";\n"
                                        "color: purple;")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.buildTree)

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 180, 81, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 480, 81, 31))
        self.label_4.setObjectName("label_4")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(60, 210, 1191, 261))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setFontFamily("黑体")  # 字体设置为黑体
        self.textEdit.setFontPointSize(13)
        self.textEdit.append("FOICP-Miner is starting...")

        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(60, 520, 1191, 261))
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.setFontFamily("黑体")  # 字体设置为黑体
        self.textEdit_2.setFontPointSize(13)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.stop_flag = False  # Initialize stop flag

    def openfile(self):
        self.textEdit.append("Selecting fuzzyontology file...")
        openfile_name = QFileDialog.getOpenFileName(None, 'choose fuzzyontology file',
                                                    'F:\pythonITEM\pycharmITem\FuzzOntoInteractively')

        self.textEditOnto.setText(openfile_name[0])
        self.textEdit.append("Selecting fuzzyontology file successfully.")

    def openfile1(self):
        self.textEdit.append("Selecting dataset file...")
        openfile_name = QFileDialog.getOpenFileName(None, 'choose data file',
                                                    'F:\pythonITEM\pycharmITem\FuzzOntoInteractively')
        self.textEditData.setText(openfile_name[0])
        self.textEdit.append("Selecting dataset file successfully.")

    def startInteractively(self):
        self.stop_flag = False  # Reset stop flag before starting
        self.textEdit.append("FOICP-Miner is running...")
        lastInterDic = {}  # 保存每一次交互的结果
        dicOntology = getOntology().getOntology()
        datafile = "frequentData3.data"
        data = load_data(datafile).get_data()
        reNum = len(data)
        favList = []
        print('原data的长度', reNum)
        countInter = 0
        while len(data) != 0:
            if self.stop_flag:
                self.textEdit.append("FOICP-Miner has been stopped.")
                break
            maxList, maxDic = utils.GetMaximalConcepts(dicOntology, data)
            data.remove(maxList)
            recommendList = []  # 保存交互到界面上的模式 每一轮要清零
            recommendList.append(maxList)
            backRecommList = utils.recommendPatterns(dicOntology, data, maxDic)
            for tempitem in backRecommList:
                data.remove(list(tempitem))
                recommendList.append(tempitem)
            self.textEdit.append("The user is interacting in the " + listsNum[countInter] + " round...")

            dicResponse, recoDic = utils.connetInteractively(recommendList)
            self.textEdit.append("The " + listsNum[countInter] + " selection is over...")

            dicResponse1 = {}
            listRound = []
            for key, value in dicResponse.items():
                dicResponse1[tuple(recoDic[key])] = value
                if value == 1:
                    listRound.append(list(key))
            self.textEdit.append("In the " + listsNum[countInter] + " round,you choose" + str(listRound))

            lastInterDic, data = utils.FilterPatterns(data, dicResponse1, lastInterDic, dicOntology, minJaccard)
            self.textEdit.append("The number of remaining patterns: " + str(len(data)))
            countInter = countInter + 1

        if not self.stop_flag:
            self.textEdit.append("The interaction process ends...")
            for key1, value1 in lastInterDic.items():
                if value1 == 1:
                    favList.append(list(key1))
            self.textEdit_2.append('the origianl frequent patterns: ' + str(reNum))
            self.textEdit_2.append("The number of frequent patterns after interaction: " + str(len(favList)))
            outlist = []
            for i in favList:
                inList = []
                for j in i:
                    inList.append(OntologyToChar[j])
                self.textEdit_2.append(str(inList))
        else:
            self.textEdit.append("Interaction was stopped prematurely.")
            for key1, value1 in lastInterDic.items():
                if value1 == 1:
                    favList.append(list(key1))
            self.textEdit_2.append('the origianl frequent patterns: ' + str(reNum))
            self.textEdit_2.append("The number of frequent patterns after interaction: " + str(len(favList)))
            outlist = []
            for i in favList:
                inList = []
                for j in i:
                    inList.append(OntologyToChar[j])
                self.textEdit_2.append(str(inList))

    def stopInteraction(self):
        self.stop_flag = True

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FOICP-Miner"))
        MainWindow.setWindowIcon(QIcon('OIP.jpg'))
        self.inOntoButt.setText(_translate("MainWindow", "Browse..."))
        self.inDataButt.setText(_translate("MainWindow", "Browse..."))
        self.label.setText(_translate("MainWindow",
                                      "<html><head/><body><p><span style=\" font-size:16pt; color:black;\">FuzzyOntology:</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-size:16pt; color:black;\">Dataset:</span></p></body></html>"))
        self.pushButton_3.setText(_translate("MainWindow", "Start"))
        self.pushButton_4.setText(_translate("MainWindow", "Stop"))
        self.pushButton_5.setText(_translate("MainWindow", "Visualize_Fuzzy_Ontoloy_Tree"))
        self.label_3.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-size:12pt;\">status:</span></p></body></html>"))
        self.label_4.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-size:12pt;\">results:</span></p></body></html>"))

    def buildTree(self):
        import FuzzyOntologyTree
        self.textEdit.append("FuzzyOntology_Tree is visualizing......")
        self.one = FuzzyOntologyTree.DemoTreeView()
        self.one.show()
        self.textEdit.append("Visualizing is over...")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
