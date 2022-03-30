import cv2, dlib
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from ChooseEffect import EffectWidget
from ChooseFilter import FilterWidget
from Camera import Thread, Thread_3
import sys


ui = uic.loadUiType("snow.ui")[0]

class SnowApp(QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.thread_3 = Thread_3()
        self.thread = Thread(self)

        self.thread_3.start()
        self.thread.start()

        self.thread.video_emit.connect(self.setImage)
        self.thread_3.det_frame.connect(self.setImage_2)
        self.second = EffectWidget(self, self.thread_3)


    def setImage(self, frame):


        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, c = rgb_frame.shape
        bytes_per_line = w * c

        cvt2qt = QImage(rgb_frame, w, h, bytes_per_line, QImage.Format_RGB888)

        self.lbl_cam.setPixmap(QPixmap.fromImage(cvt2qt))


    def setImage_2(self, frame):

        if frame.size == 0:
            pass

        else:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, c = rgb_frame.shape
            bytes_per_line = w * c

            cvt2qt = QImage(rgb_frame, w, h, bytes_per_line, QImage.Format_RGB888)

            self.lbl_cam_2.setPixmap(QPixmap.fromImage(cvt2qt))



    def effect(self):
        self.second.move(700, 200)
        self.second.show()




    def capture(self):
        pass

    def filter(self):
        self.third.move(1200, 200)
        self.third.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SnowApp()
    win.setWindowTitle("OSSNOW")
    win.show()
    sys.exit(app.exec())