import sys
import cv2
import math
import cv2 as cv
import mediapipe as mp
import numpy as np
import pyautogui
import time
from PySide6 import QtWidgets
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QSize, QTimer
from PySide6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, QLabel, QVBoxLayout
from PySide6.QtGui import QIcon, QImage, QPixmap
from PySide6.QtUiTools import QUiLoader


face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks = True)
leftEye = [362, 382, 381, 381, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
left_iris = [474, 475, 476, 477]
right_iris = [469, 470, 471, 472]
rightEye = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
LHLeft = [33]
LHRight = [133]
RHLeft = [362]
RHRight = [263]

from MainWindow import Ui_Visionary

class MainWindow(QtWidgets.QMainWindow, Ui_Visionary):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.video_size = QSize(420, 340)
        self.TEXT.setText('Kindly Press Start to open the Webcam')
        self.Start.pressed.connect(self.start_camera)
        self.Stop.pressed.connect(self.stop_camera)
        self.f = False
        pass
    
    def stop_camera(self):
        self.TEXT.setText('Kindly Press Start to open the Webcam')
        self.f = False

    def start_camera(self):
        """Initialize camera.
        """ 
        self.f = True
        self.TEXT.setText('Kindly Press Stop to close the Webcam')
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(0)

    def display_video_stream(self):
        """Read frame from camera and repaint QLabel widget.
        """
        if self.f:
            self.image_label.setHidden(False)  
            _, frame = self.capture.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)
            image = QImage(frame, frame.shape[1], frame.shape[0], 
                            frame.strides[0], QImage.Format_RGB888)
            self.image_label.setPixmap(QPixmap.fromImage(image))   
            self.image_label.setAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter) 
            face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks = True)
            screen_w, screen_h = pyautogui.size()
            fl, fr = False, False
            f1, f2 = True, True
            scale = 25
            height, width, channels = frame.shape
            centerX,centerY=int(height/2),int(width/2)
            radiusX,radiusY= int(scale*height/100),int(scale*width/100)
            minX,maxX=centerX-radiusX,centerX+radiusX
            minY,maxY=centerY-radiusY,centerY+radiusY
            cropped = frame[minX:maxX, minY:maxY]
            frame = cv.resize(cropped, (width, height))
            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            output = face_mesh.process(rgb_frame)
            landmark_points = output.multi_face_landmarks
            #print(landmark_points)
            frame_h, frame_w, __ = frame.shape
            if landmark_points:
                landmarks = landmark_points[0].landmark
                for id, landmark in enumerate(landmarks[474:478]):
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    cv.circle(frame, (x, y), 3, (0, 255, 0))
                    if id == 1:
                        screen_x = screen_w / frame_w * x
                        screen_y = screen_h / frame_h * y
                        pyautogui.moveTo(screen_x, screen_y)
                left = [landmarks[145], landmarks[159]]
                right =  [landmarks[374], landmarks[386]]
                for landmark in left:
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    cv.circle(frame, (x, y), 3, (0, 255, 255))
                    #print(left[0].y - left[1].y, 'left')
                    #print(fl, f1)
                if (left[0].y - left[1].y) < 0.02:
                    if fl and f1:
                        pyautogui.mouseDown()
                        f1=False
                    elif not fl:
                        pyautogui.click()
                        fl=True
                        #pyautogui.sleep(1)
                elif fl and (left[0].y - left[1].y) > 0.02 and not f1:
                    fl=False
                    f1=True
                    pyautogui.mouseUp()
        else:
            self.image_label.setHidden(True)  


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec_()