from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
import os, cv2

# 이미지 찾아서 읽기
dir = "./images"
img_list = []
img_extension = '.png'

for root, dir, files in os.walk(dir):
    if len(files) > 0:
        for file_name in files:
            if os.path.splitext(file_name)[1] in img_extension:
                img_path = root + '/' + file_name
                img_list.append(img_path)

for idx,i in enumerate(img_list):
    globals()['num_{}'.format(idx)] = i




class EffectWidget(QDialog):

    def __init__(self, parent=None, thread2=None):
        super(EffectWidget, self).__init__(parent)
        loadUi("select.ui", self)
        self.parent = parent
        self.thread = thread2


    # 각 버튼 클릭하면 위에서 읽어온 이미지를 self.mask에 담는다
    def mask_effect_slot(self):
        self.mask = cv2.imread(num_0, cv2.IMREAD_UNCHANGED) # alpha channel 까지 읽어오기
        self.thread.mask = self.mask


    def sweetpotato_effect(self):
        self.mask = cv2.imread(num_2, cv2.IMREAD_UNCHANGED)
        self.thread.mask = self.mask


    def lip_effect(self):
        self.mask = cv2.imread(num_8, cv2.IMREAD_UNCHANGED)
        self.thread.mask = self.mask


    def pig_effect(self):
        self.mask = cv2.imread(num_1, cv2.IMREAD_UNCHANGED)
        self.thread.mask = self.mask



    def disguise_effect(self):
        self.mask = cv2.imread(num_4, cv2.IMREAD_UNCHANGED)
        self.thread.mask = self.mask


    def tarantula_effect(self):
        self.mask = cv2.imread(num_3, cv2.IMREAD_UNCHANGED)
        self.thread.mask = self.mask