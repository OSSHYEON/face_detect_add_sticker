import cv2, os, sys, datetime
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow
from ChooseEffect import EffectWidget
from ChooseFilter import FilterWidget
from Camera import Thread, Thread_2



ui = uic.loadUiType("snow.ui")[0]

class SnowApp(QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.thread_2 = Thread_2()
        self.thread = Thread(self)

        self.thread_2.start()
        self.thread.start()

        self.thread_2.det_frame.connect(self.setImage)
        self.thread_2.det_frame.connect(self.capture)
        self.second = EffectWidget(self, self.thread_2)

        self.now = datetime.datetime.now().strftime("%m-%d_%H-%M-%S-%f")



    def setImage(self, frame):

        if frame.size == 0:
            pass

        else:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb_frame = cv2.resize(rgb_frame, (400,400), fx=0.5, fy=0.5)
            h, w, c = rgb_frame.shape
            bytes_per_line = w * c
            cvt2qt = QImage(rgb_frame, w, h, bytes_per_line, QImage.Format_RGB888)

            self.lbl_cam_2.setPixmap(QPixmap.fromImage(cvt2qt).scaled(h, w, Qt.KeepAspectRatio))


    def effect(self):
        self.second.move(700, 200)
        self.second.show()


    def capture(self, frame):
        save_path = "./captured_picture/"
        if not os.path.isdir(save_path):
            os.makedirs(save_path)
            cv2.imwrite(save_path + str(self.now)+".png", frame)

        else:
            cv2.imwrite(save_path + str(self.now) + ".png", frame)



    def filter(self):
        self.third.move(1200, 200)
        self.third.show()
