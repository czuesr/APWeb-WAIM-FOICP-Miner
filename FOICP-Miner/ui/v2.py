import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        #窗体标题和尺寸
    def initUI(self):
        self.setWindowTitle("FuzzyOntologyInteractively System")
        #窗体的的尺寸
        self.resize(1050,600)
        #窗体的位置
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        # 创建布局
        layout = QVBoxLayout()
        layout.addLayout(self.init_header())
        # 2.创建上面标题布局
        form_layout = QHBoxLayout()
        # 2.1输入框
        label1 = QLabel()
        label1.setAlignment(Qt.AlignRight)
        label1.setText("FuzzyOntology: ")
        form_layout.addWidget(label1)
        self.txt_asin1 = QLineEdit()
        self.txt_asin1.setPlaceholderText("Please choose the ontology file")
        form_layout.addWidget(self.txt_asin1)
        # 2.2添加按钮
        btn_add = QPushButton("Browse...")
        msg = btn_add.clicked.connect(self.openfile)
        form_layout.addWidget(btn_add)
        layout.addLayout(form_layout)

        layout.addLayout(self.init_form2())
        table_layout = QHBoxLayout()
        #3.1创建表格
        table_widget = QTableWidget(2,8)

        item = QTableWidgetItem()
        item.setText("标题")
        table_widget.setHorizontalHeaderItem(0,item)
        table_widget.setColumnWidth(0,120)

        item = QTableWidgetItem()
        item.setText("网址")
        table_widget.setHorizontalHeaderItem(1, item)
        table_widget.setColumnWidth(1, 400)  #前面第一个参数是索引

        table_layout.addWidget(table_widget)
        layout.addLayout(table_layout)
        # 4.底部菜单
        footer_layout = QHBoxLayout()
        layout.addLayout(footer_layout)
        #弹簧
        layout.addStretch()
        #给窗体设置元素的排列方式
        self.setLayout(layout)
    def init_form2(self):
        # 2.创建上面标题布局

        form_layout = QHBoxLayout()
        # 2.1输入框
        label2 = QLabel()
        label2.setAlignment(Qt.AlignRight)
        label2.setText("DataSet:  ")
        form_layout.addWidget(label2)
        self.txt_asin2 = QLineEdit()
        self.txt_asin2.setPlaceholderText("Please choose the data file")
        form_layout.addWidget(self.txt_asin2)
        # 2.2添加按钮
        btn_add = QPushButton("Browse...")
        btn_add.clicked.connect(self.openfile1)
        form_layout.addWidget(btn_add)
        return form_layout

    #点击添加按钮
    def openfile(self):
        openfile_name = QFileDialog.getOpenFileName(self, 'choose ontology file', 'C:\\')
        self.txt_asin1.setText(openfile_name[0])
    def openfile1(self):
        openfile_name = QFileDialog.getOpenFileName(self, 'choose data file', 'C:\\')
        self.txt_asin2.setText(openfile_name)




    def init_header(self):
        header_layout = QHBoxLayout()
        # 1.1创建按钮 ，加入header_layout
        btn_start = QPushButton("开始")
        header_layout.addWidget(btn_start)
        btn_stop = QPushButton("停止")
        header_layout.addWidget(btn_stop)
        header_layout.addStretch()
        return header_layout



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())