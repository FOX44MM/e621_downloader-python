import sys

from PyQt6.QtWidgets import QApplication

from window import MainUI

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 启动程序 将程序的命令行参数传入
    # app.setStyle("Fusion")  # 设置程序的风格为Fusion

    Main_Window = MainUI()
    Main_Window.show()


    sys.exit(app.exec())  # qt程序完整的退出