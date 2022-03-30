import pickle
from time import time

import cv2, dlib, numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage
from numpy import ndarray

import queue

BUF_SIZE = 307200
q = queue.Queue(BUF_SIZE)

ret = int


class Thread(QThread):
    # ii = int(0)
    video_emit = pyqtSignal(ndarray)

    def __init__(self, thread=None):
        super().__init__()
        self.parent_thread = thread

    def run(self):
        global cap
        global ret
        global frame

        cap = cv2.VideoCapture(0)

        while True:

            ret, frame_r = cap.read()
            # frame_g = cv2.cvtColor(frame_r, cv2.COLOR_BGR2GRAY)
            frame_g = cv2.resize(frame_r, (300,200))

            if ret:
                self.video_emit.emit(frame_r)
                q.put(frame_g)



class Thread_3(QThread):
    det_frame = pyqtSignal(ndarray)


    def __init__(self):
        super().__init__()
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("./shape_predictor_68_face_landmarks.dat")
        self.mask = cv2.imread("./images/mask.png", cv2.IMREAD_UNCHANGED)


    def run(self):

        while True:

            if not q.empty():

                frame = q.get()
                dets = self.detector(frame, 1)

                try:

                    for det in dets:

                        x_1 = det.left()
                        x_2 = det.right()
                        y_1 = det.top()
                        y_2 = det.bottom()

                        # rec = cv2.rectangle(frame, (x_1, y_1), (x_2, y_2), (0, 255, 0), 2)

                        self.land = self.predictor(frame, det)

                        # self.landmarks = []
                        # list_points = list(map(lambda p:(p.x, p.y), self.land.parts()))
                        # self.landmarks.append(list_points)
                        #
                        # for landmark in self.landmarks:
                        #     for idx, point in enumerate(landmark):
                        #         cv2.circle(frame, point, 2, (255, 255, 255), -1)
                        #         cv2.putText(frame, str(idx), point, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1)


                        # for det, self.landmark in zip(dets, self.landmarks):

                            # x = self.landmark[33][0]
                            # y = self.landmark[33][1]

                        h, w, c = self.mask.shape


                        self.mask_x1 = self.land.parts()[67].x - int((x_2 - x_1) / 2)
                        self.mask_x2 = self.land.parts()[67].x + int((x_2 - x_1) / 2)


                        self.mask_w = self.mask_x2 - self.mask_x1
                        self.mask_h = int(h / w * self.mask_w)


                        self.mask_y1 = self.land.parts()[67].y - int(self.mask_h / 2)
                        self.mask_y2 = self.land.parts()[67].y + int(self.mask_h / 2)

                        self.mask = cv2.resize(self.mask, (self.mask_w, self.mask_h))


                        overlay_alpha = self.mask[:, :, 3:4] / 255.0
                        background_alpha = 1.0 - overlay_alpha

                        frame[self.mask_y1:self.mask_y2, self.mask_x1:self.mask_x2] = overlay_alpha * self.mask[:, :,:3] + background_alpha * frame[self.mask_y1:self.mask_y2,self.mask_x1:self.mask_x2]


                        self.det_frame.emit(frame)

                except:
                    pass







