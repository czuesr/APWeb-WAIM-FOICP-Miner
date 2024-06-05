import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTreeView,
                             QAbstractItemView, QHeaderView, QStyleFactory)


class DemoTreeView(QMainWindow):
    def __init__(self, parent=None):
        super(DemoTreeView, self).__init__(parent)

        # 设置窗口标题
        self.setWindowTitle('FuzzyOntology')
        # 设置窗口大小
        self.resize(520, 360)
        self.setWindowIcon(QIcon('R-C.jpg'))

        self.initUi()

    def initUi(self):

        # 设置表头信息
        model = QStandardItemModel(self)
        model.setHorizontalHeaderLabels(['     ', ' '])

        # 添加条目
        itemProject = QStandardItem('POI in Beijing')
        model.appendRow(itemProject)
        model.setItem(0, 1, QStandardItem('membership_value'))

        # 添加子条目
        item1 = QStandardItem('Accommodation_Service')
        itemProject.appendRow(item1)
        itemProject.setChild(0, 1, QStandardItem('1.0'))
        itemGroup1 = QStandardItem('Hotel')
        item1.appendRow(itemGroup1)
        item1.setChild(0,1,QStandardItem('1.0'))
        itemGroup2 = QStandardItem('Hostel')
        item1.appendRow(itemGroup2)
        item1.setChild(1,1, QStandardItem('1.0'))
        # 继续添加
        item2 = QStandardItem('Traffic')
        itemProject.appendRow(item2)
        itemProject.setChild(1, 1, QStandardItem('1.0'))
        itemGroup3 = QStandardItem('Airport')
        item2.appendRow(itemGroup3)
        item2.setChild(0, 1, QStandardItem('0.7'))
        itemGroup4 = QStandardItem('Railway_Station')
        item2.appendRow(itemGroup4)
        item2.setChild(1, 1, QStandardItem('1.0'))
        itemGroup7 = QStandardItem('Car_Parks')
        item2.appendRow(itemGroup7)
        item2.setChild(2, 1, QStandardItem('1.0'))

        item3 = QStandardItem('Sports_and_Recreation')
        itemProject.appendRow(item3)
        itemProject.setChild(2, 1, QStandardItem('1.0'))
        itemGroup5 = QStandardItem('Park')
        item3.appendRow(itemGroup5)
        item3.setChild(0, 1, QStandardItem('0.4'))
        itemGroup6 = QStandardItem('Gymnasium')
        item3.appendRow(itemGroup6)
        item3.setChild(1, 1, QStandardItem('1.0'))

        item4 = QStandardItem('Shopping_Service')
        itemProject.appendRow(item4)
        itemProject.setChild(3, 1, QStandardItem('1.0'))
        itemGroup11 = QStandardItem('Bubble_tea_shop')
        item4.appendRow(itemGroup11)
        item4.setChild(0, 1, QStandardItem('0.5'))
        itemGroup12 = QStandardItem('Clothes_Shop')
        item4.appendRow(itemGroup12)
        item4.setChild(1, 1, QStandardItem('1.0'))
        itemGroup13 = QStandardItem('Animal_Shop')
        item4.appendRow(itemGroup13)
        item4.setChild(2, 1, QStandardItem('1.0'))
        itemGroup14 = QStandardItem('Airport')
        item4.appendRow(itemGroup14)
        item4.setChild(3, 1, QStandardItem('0.3'))

        item5 = QStandardItem('Sights')
        itemProject.appendRow(item5)
        itemProject.setChild(4, 1, QStandardItem('1.0'))
        itemGroup15 = QStandardItem('Park')
        item5.appendRow(itemGroup15)
        item5.setChild(0, 1, QStandardItem('0.6'))
        itemGroup16 = QStandardItem('National_Scenic_spots')
        item5.appendRow(itemGroup16)
        item5.setChild(1, 1, QStandardItem('1.0'))
        itemGroup17 = QStandardItem('Provincial_Scenic_spots')
        item5.appendRow(itemGroup17)
        item5.setChild(2, 1, QStandardItem('1.0'))

        item6 = QStandardItem('Food_and_Beverages')
        itemProject.appendRow(item6)
        itemProject.setChild(5, 1, QStandardItem('1.0'))
        itemGroup8 = QStandardItem('Chinese_Restaurant')
        item6.appendRow(itemGroup8)
        item6.setChild(0, 1, QStandardItem('1.0'))
        itemGroup9 = QStandardItem('Western_Restaurant')
        item6.appendRow(itemGroup9)
        item6.setChild(1, 1, QStandardItem('1.0'))
        itemGroup10 = QStandardItem('Bubble_tea_shop')
        item6.appendRow(itemGroup10)
        item6.setChild(2, 1, QStandardItem('0.5'))




        treeView = QTreeView(self)
        treeView.setModel(model)
        # 调整第一列的宽度
        treeView.header().resizeSection(0, 240)
        # 设置成有虚线连接的方式
        treeView.setStyle(QStyleFactory.create('windows'))
        # 完全展开
        treeView.expandAll()

        # 显示选中行的信息
        #treeView.selectionModel().currentChanged.connect(self.onCurrentChanged)

        self.model = model
        self.treeView = treeView
        self.setCentralWidget(treeView)

    def onCurrentChanged(self, current, previous):
        txt = '父级:[{}] '.format(str(current.parent().data()))
        txt += '当前选中:[(行{},列{})] '.format(current.row(), current.column())

        name = ''
        info = ''
        if current.column() == 0:
            name = str(current.data())
            info = str(current.sibling(current.row(), 1).data())
        else:
            name = str(current.sibling(current.row(), 0).data())
            info = str(current.data())

        txt += '名称:[{}]  信息:[{}]'.format(name, info)

        self.statusBar().showMessage(txt)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DemoTreeView()
    window.show()
    sys.exit(app.exec())