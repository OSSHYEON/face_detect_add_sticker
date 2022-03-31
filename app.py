import sys
from PyQt5.QtWidgets import QApplication
from QtUi import SnowApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SnowApp()
    win.setWindowTitle("OSSNOW")
    win.show()
    sys.exit(app.exec())