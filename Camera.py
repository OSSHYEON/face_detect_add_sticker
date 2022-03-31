import cv2, dlib
from PyQt5.QtCore import QThread, pyqtSignal
from numpy import ndarray
import queue



BUF_SIZE = 307200
q = queue.Queue(BUF_SIZE)

ret = int



class Thread(QThread):

    video_emit = pyqtSignal(ndarray)


    def run(self):
        global cap

        cap = cv2.VideoCapture(0)

        while True:

            ret, frame = cap.read()
            frame = cv2.resize(frame, (300,200))

            if ret:
                q.put(frame)



class Thread_2(QThread):
    det_frame = pyqtSignal(ndarray)

    def __init__(self):
        super().__init__()
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("./shape_predictor_68_face_landmarks.dat")
        self.mask = None  # second widget에서 버튼을 클릭하면 이미지를 받아온다.


    def run(self):

        while True:

            if not q.empty():

                frame = q.get() # 큐에 담은 영상 꺼내기
                dets = self.detector(frame, 1)


                if self.mask is None:
                    self.det_frame.emit(frame)  # 효과 선택하지 않았을 때는 가공하지 않은 영상 송출

                else:
                    try:

                        for det in dets:
                            x_1 = det.left()
                            x_2 = det.right()

                            self.land = self.predictor(frame, det)

                            h, w, c = self.mask.shape

                            self.mask_x1 = self.land.parts()[67].x - int((x_2 - x_1) / 3)
                            self.mask_x2 = self.land.parts()[67].x + int((x_2 - x_1) / 3)

                            self.mask_w = self.mask_x2 - self.mask_x1
                            self.mask_h = int(h / w * self.mask_w)

                            self.mask_y1 = self.land.parts()[67].y - int(self.mask_h / 2)
                            self.mask_y2 = self.land.parts()[67].y + int(self.mask_h / 2)

                            self.mask = cv2.resize(self.mask, (self.mask_w, self.mask_h))

                            overlay_alpha = self.mask[:, :, 3:4] / 255.0
                            background_alpha = 1.0 - overlay_alpha

                            frame[self.mask_y1:self.mask_y2, self.mask_x1:self.mask_x2] = overlay_alpha * self.mask[:, :,:3] + background_alpha * frame[self.mask_y1:self.mask_y2,self.mask_x1:self.mask_x2]

                            self.det_frame.emit(frame)  # 스티커 합친 프레임 송출


                    except:
                        continue







