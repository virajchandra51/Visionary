import sys
import cv2
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

from MainWindow import Ui_Visionary

class MainWindow(QtWidgets.QMainWindow, Ui_Visionary):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.video_size = QSize(320, 240)
        self.TEXT.setText('Kindly Press Start to open the Webcam')
        self.Start.pressed.connect(self.start_camera)
        self.Stop.pressed.connect(self.stop_camera)
        self.f=False
        pass
    
    def start_camera(self):
        self.f=True
        face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks = True)
        self.capture =  cv.VideoCapture(0)
        screen_w, screen_h = pyautogui.size()
        fl, fr = False, False
        f1, f2 = True, True
        scale = 25

        while self.f:

            _, frame = self.capture.read()
            frame = cv.flip(frame, 1)

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

                """print(right[0].y - right[1].y, 'right')
                if (right[0].y - right[1].y) < 0.02:
                    if fr and f2:
                        pyautogui.mouseDown(button='right')
                        f2=False
                    elif not fr:
                        pyautogui.click(button='right')
                        fr=True
                        #pyautogui.sleep(1)
                elif fr and (right[0].y - right[1].y) > 0.02 and not f2:
                    fr=False
                    f2=True
                    pyautogui.mouseUp(button='right')"""
                
                        

            cv.imshow('Eye controlled mouse', frame)
            cv.waitKey(1)

            if cv.waitKey(20) and 0xFF==ord('d'):
                break

        self.capture.release()
        cv.destroyAllWindows()
    
    def stop_camera(self):
        self.TEXT.setText('Kindly Press Start to open the Webcam')
        self.f = False

    def setup_camera(self):
        """Initialize camera.
    """
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
        _, frame = self.capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        image = QImage(frame, frame.shape[1], frame.shape[0], 
                        frame.strides[0], QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(image))   
        self.image_label.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter) 

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec_()