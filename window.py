from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import QTimer
from ui.baseui import Ui_MainWindow


class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Timer = QTimer()   # 可用于进度条的更新

        self.tagEdit.textChanged.connect(self.tagEdit_changed)
        self.downloadButton.clicked.connect()


    def tagEdit_changed(self):
        print("内容发生变化")


    def downloadButton_clicked(self):
        print("开始下载")