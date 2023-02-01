from MainWindow import Ui_Visionary
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


face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
leftEye = [362, 382, 381, 381, 374, 373, 390,
    249, 263, 466, 388, 387, 386, 385, 384, 398]
left_iris = [474, 475, 476, 477]
right_iris = [469, 470, 471, 472]
rightEye = [33, 7, 163, 144, 145, 153, 154,
    155, 133, 173, 157, 158, 159, 160, 161, 246]
LHLeft = [33]
LHRight = [133]
RHLeft = [362]
RHRight = [263]
scale = 25
font = cv2.FONT_HERSHEY_SIMPLEX
org = (200, 50)
org1 = (130, 50)
fontScale = 1
color = (0, 0, 0)
thickness = 2


class MainWindow(QtWidgets.QMainWindow, Ui_Visionary):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.video_size = QSize(420, 340)
        self.TEXT.setText('Kindly Press Start to open the Webcam')
        self.Start.pressed.connect(self.start_camera)
        self.Stop.pressed.connect(self.stop_camera)
        self.f = False
        self.cnt = 0
        self.leftEyeCalibration, self.rightEyeCalibration = [], []
        self.leftEyeClosed, self.rightEyeClosed = 0, 0
        self.cntBlink = 0
        self.f1 = False
        my_pixmap = QPixmap("./logo.png")
        my_icon = QIcon(my_pixmap)
        self.setWindowIcon(my_icon)
        self.fl = False
        self.f2 = True
        self.headControl = True
        self.Check.toggled.connect(self.head_control)

    def head_control(self):
        if self.headControl:
            self.headControl = False
        else:
            self.headControl = True
        
    def stop_camera(self):
        self.TEXT.setText('Kindly Press Start to open the Webcam')
        self.cntBlink = 0
        self.f = False
        self.f1 = False

    def start_camera(self):
        """Initialize camera.
        """
        self.cnt = 0
        self.f = True
        self.f1 = True
        self.TEXT.setText('Kindly Press Stop to close the Webcam')
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())
        self.timer = QTimer()
        if self.headControl:
            self.timer.timeout.connect(self.display_video_stream)
        else:
            self.timer.timeout.connect(self.display_video_stream1)

        self.timer.start(0)


    def display_video_stream1(self):

        if self.f1:
            self.image_label.setHidden(False)
            screen_w, screen_h = pyautogui.size()
            
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
                #right =  [landmarks[374], landmarks[386]]
                for landmark in left:
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    cv.circle(frame, (x, y), 3, (0, 255, 255))
                    #print(left[0].y - left[1].y, 'left')
                    #print(fl, f1)
                if (left[0].y - left[1].y) < 0.02:
                    if self.fl and self.f2:
                        pyautogui.mouseDown()
                        self.f2=False
                    elif not self.fl:
                        pyautogui.click()
                        self.fl=True
                        #pyautogui.sleep(1)
                elif self.fl and (left[0].y - left[1].y) > 0.02 and not self.f2:
                    self.fl=False
                    self.f2=True
                    pyautogui.mouseUp()

            image = QImage(frame, frame.shape[1], frame.shape[0], 
                            frame.strides[0], QImage.Format_BGR888)
            self.image_label.setPixmap(QPixmap.fromImage(image))   
            self.image_label.setAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            
        else:
            self.image_label.setHidden(True)



    def display_video_stream(self):
        """Read frame from camera and repaint QLabel widget.
        """
        if self.f:
            self.image_label.setHidden(False)
            _, frame = self.capture.read()
            frame = cv.flip(frame, 1)
            height, width, channels = frame.shape

            centerX, centerY = int(height/2), int(width/2)
            radiusX, radiusY = int(scale*height/100), int(scale*width/100)

            minX, maxX = centerX-radiusX, centerX+radiusX
            minY, maxY = centerY-radiusY, centerY+radiusY

            cropped = frame[minX:maxX, minY:maxY]
            frame = cv.resize(cropped, (width, height))
            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            output = face_mesh.process(rgb_frame)
            landmark_points = output.multi_face_landmarks
            frame_h, frame_w = frame.shape[:2]
            if landmark_points:
                landmarks = landmark_points[0].landmark

                xc1, yc1 = landmarks[475].x * \
                    frame_w, landmarks[475].y * frame_h
                xc2, yc2 = landmarks[477].x * \
                    frame_w, landmarks[477].y * frame_h
                # print(xc1+xc2)
                xc, yc = (xc1+xc2)/2, (yc1+yc2)/2
                xl, yl = landmarks[362].x * frame_w, landmarks[362].y * frame_h
                xr, yr = landmarks[263].x * frame_w, landmarks[263].y * frame_h
                xret, yret = landmarks[386].x * \
                    frame_w, landmarks[386].y * frame_h
                xreb, yreb = landmarks[374].x * \
                    frame_w, landmarks[374].y * frame_h
                xlet, ylet = landmarks[159].x * \
                    frame_w, landmarks[159].y * frame_h
                xleb, yleb = landmarks[145].x * \
                    frame_w, landmarks[145].y * frame_h
                landmark = landmarks[1]
                """if f:
                    xinit, yinit = int(
                        landmark.x * frame_w), int(landmark.y * frame_h)
                    f=0
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                if y - yinit > 25:
                    pyautogui.move(0, 30)
                elif yinit - y > 20:
                    pyautogui.move(0, -30)"""

                # 477 159
                left = [landmarks[145], landmarks[159]]
                right = [landmarks[374], landmarks[386]]
                p1, p2 = landmarks[477], landmarks[374]

                # print(p1.y * frame_h - p2.y * frame_h)

                # print(left[0].y - left[1].y, 'left')

                if self.cnt <= 100:
                    frame = cv2.putText(frame, 'Close left eye', org, font,
                   fontScale, color, thickness, cv2.LINE_AA)
                    self.cnt += 1
                    cv.circle(frame, (int(xret), int(yret)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xreb), int(yreb)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xlet), int(ylet)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xleb), int(yleb)), 3, (0, 255, 0))

                elif self.cnt <= 200:
                    a = 1
                    cv.circle(frame, (int(xret), int(yret)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xreb), int(yreb)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xlet), int(ylet)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xleb), int(yleb)), 3, (0, 255, 0))
                    self.leftEyeCalibration.append(left[0].y-left[1].y)
                    self.leftEyeClosed = max(self.leftEyeCalibration)

                    if a == 1:
                        frame = cv2.putText(frame, 'Close left eye : CALIBRATING', org1, font,
                       fontScale, color, thickness, cv2.LINE_AA)
                    else:
                        frame = cv2.putText(frame, 'Close left eye', org1, font,
                       fontScale, color, thickness, cv2.LINE_AA)
                    if self.cnt % 20 == 0: a = 1-a
                    self.cnt += 1

                elif self.cnt <= 300:
                    cv.circle(frame, (int(xret), int(yret)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xreb), int(yreb)), 3, (0,255,0))
                    cv.circle(frame, (int(xlet), int(ylet)), 3, (0,255,0))
                    cv.circle(frame, (int(xleb), int(yleb)), 3, (0,255,0))
                    frame = cv2.putText(frame, 'Close right eye', org, font, 
                    fontScale, color, thickness, cv2.LINE_AA)
                    self.cnt+=1
                
                elif self.cnt<=400:
                    a=1
                    cv.circle(frame, (int(xret), int(yret)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xreb), int(yreb)), 3, (0,255,0))
                    cv.circle(frame, (int(xlet), int(ylet)), 3, (0,255,0))
                    cv.circle(frame, (int(xleb), int(yleb)), 3, (0,255,0))
                    self.rightEyeCalibration.append(right[0].y-right[1].y)
                    self.rightEyeClosed = max(self.rightEyeCalibration)

                    if a==1:
                        frame = cv2.putText(frame, 'Close right eye: CALIBRATING', org1, font, 
                   fontScale, color, thickness, cv2.LINE_AA)
                    else:
                        frame = cv2.putText(frame, 'Close right eye', org, font, 
                   fontScale, color, thickness, cv2.LINE_AA)
                    if self.cnt%20==0: a=1-a
                    self.cnt+=1
                
                else:
                    
                    # cv.circle(frame, (xinit, yinit), 20, (0,255,0))
                    iris_pos = self.iris_position([xc, yc] , [xr, yr] , [xl, yl] , [xret, yret] , [xreb, yreb])
                    if p1.y * frame_h - p2.y * frame_h < -0.8:
                        iris_pos = 'up'
                        pyautogui.move(0, -30)
                    if iris_pos == 'right':
                        pyautogui.move(30,0)
                    elif iris_pos == 'left':
                        pyautogui.move(-30,0)
                    
                    # print((left[0].y - left[1].y), self.leftEyeClosed, "left")
                    # print((right[0].y - right[1].y), self.rightEyeClosed, "right")
                    if (left[0].y - left[1].y) < self.leftEyeClosed and (right[0].y - right[1].y) < self.rightEyeClosed:
                        self.cntBlink+=1
                        if self.cntBlink>5:
                            pyautogui.move(0,30)

                    elif (left[0].y - left[1].y) < self.leftEyeClosed:
                        self.cntBlink+=1
                        if self.cntBlink>5:
                            pyautogui.click()
                            pyautogui.sleep(1)
                        

                    elif (right[0].y - right[1].y) < self.rightEyeClosed:
                        self.cntBlink+=1
                        if self.cntBlink>5:
                            pyautogui.click(button='right')
                            pyautogui.sleep(1)
                    else:
                        self.cntBlink = 0

            image = QImage(frame, frame.shape[1], frame.shape[0], 
                            frame.strides[0], QImage.Format_BGR888)
            self.image_label.setPixmap(QPixmap.fromImage(image))   
            self.image_label.setAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                    
            
        else:
            self.image_label.setHidden(True)
            
            
    def iris_position(self, iris_center, right_point, left_point, top_point, bottom_point):
        ctrd = self.distance(iris_center, right_point)
        totald = self.distance(right_point, left_point)

        center_bot_diff = self.distance(iris_center, bottom_point)
        top_bot_diff = self.distance(top_point, bottom_point)

        ratio1 = ctrd / totald
        ratio2 = center_bot_diff / top_bot_diff

        iris_position = ""
        # print(ratio1)
        if ratio1<=0.38:
            iris_position = "right"
        elif ratio1>0.60:
            iris_position = "left"
        else:    
            iris_position  = "center"

        return iris_position
    
    def distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        distance = math.sqrt((x2-x1)**2+(y2-y1)**2)
        return distance     


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()