import cv2 as cv
import mediapipe as mp
import numpy as np
import pyautogui
import time
class BackEnd:

    def __init__(self) -> None:
        self.f=False
        pass
    
    def function(self):
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
    
    def stop(self):
        self.f = False
