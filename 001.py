import cv2 as cv
import numpy as np
import mediapipe as mp
import pyautogui
import math

# 475 477 center right iris
# 362 left edge left eye
# 263 right edge left eye
# 159 left eye top
# 145 left eye bottom
# 386 left eye top
# 374 left eye bottom

face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks = True)
leftEye = [362, 382, 381, 381, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
left_iris = [474, 475, 476, 477]
right_iris = [469, 470, 471, 472]
rightEye = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
LHLeft = [33]
LHRight = [133]
RHLeft = [362]
RHRight = [263]



def calibrate(capture):
    cnt = 0
    while cnt <= 30:
        rt, frame = capture.read()
        if not rt:
            break

        frame  = cv.flip(frame, 1)
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w = frame.shape[:2]
        if landmark_points:
            landmarks = landmark_points[0].landmark

            xret, yret = landmarks[159].x * frame_w, landmarks[159].y * frame_h
            xreb, yreb = landmarks[145].x * frame_w, landmarks[145].y * frame_h
            
            xc, yc = (xc1+xc2)/2, (yc1+yc2)/2
            xl, yl = landmarks[362].x * frame_w, landmarks[362].y * frame_h
            xr, yr = landmarks[263].x * frame_w, landmarks[263].y * frame_h


def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2-x1)**2+(y2-y1)**2)
    return distance

def iris_position(iris_center, right_point, left_point, top_point, bottom_point):
    ctrd = distance(iris_center, right_point)
    totald = distance(right_point, left_point)

    center_bot_diff = distance(iris_center, bottom_point)
    top_bot_diff = distance(top_point, bottom_point)

    ratio1 = ctrd / totald
    ratio2 = center_bot_diff / top_bot_diff

    iris_position = ""
    if ratio1<=0.37:
        iris_position = "right"
    elif ratio1>0.60:
        iris_position = "left"
    else:    
        iris_position  = "center"

    return iris_position    


capture = cv.VideoCapture(0)
#calibrate(capture)
f=1
cnt_left_click = 0

while True:
    rt, frame = capture.read()
    if not rt:
        break

    frame  = cv.flip(frame, 1)
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w = frame.shape[:2]
    if landmark_points:
        landmarks = landmark_points[0].landmark

        xc1, yc1 = landmarks[475].x * frame_w, landmarks[475].y * frame_h
        xc2, yc2 = landmarks[477].x * frame_w, landmarks[477].y * frame_h
        #print(xc1+xc2)
        xc, yc = (xc1+xc2)/2, (yc1+yc2)/2
        xl, yl = landmarks[362].x * frame_w, landmarks[362].y * frame_h
        xr, yr = landmarks[263].x * frame_w, landmarks[263].y * frame_h
        xret, yret = landmarks[386].x * frame_w, landmarks[386].y * frame_h
        xreb, yreb = landmarks[374].x * frame_w, landmarks[374].y * frame_h
        xlet, ylet = landmarks[159].x * frame_w, landmarks[159].y * frame_h
        xleb, yleb = landmarks[145].x * frame_w, landmarks[145].y * frame_h
        landmark = landmarks[1]
        """if f:
            xinit, yinit = int(landmark.x * frame_w), int(landmark.y * frame_h)
            f=0
        x = int(landmark.x * frame_w)
        y = int(landmark.y * frame_h)
        if y - yinit > 25:
            pyautogui.move(0, 30)
        elif yinit - y > 20:
            pyautogui.move(0, -30)"""

        #477 159
        left = [landmarks[145], landmarks[159]]
        right =  [landmarks[374], landmarks[386]]
        p1, p2  = landmarks[477], landmarks[374]
        cv.circle(frame, (int(xret), int(yret)), 3, (0,255,0))
        cv.circle(frame, (int(xreb), int(yreb)), 3, (0,255,0))
        print(p1.y * frame_h - p2.y * frame_h)
        
        #print(left[0].y - left[1].y, 'left')

        if p1.y * frame_h - p2.y * frame_h < 0:
            pyautogui.move(0, -30)
        #cv.circle(frame, (xinit, yinit), 20, (0,255,0))
        iris_pos = iris_position([xc, yc] , [xr, yr] , [xl, yl] , [xret, yret] , [xreb, yreb])
        if iris_pos == 'right':
            pyautogui.move(30,0)
        elif iris_pos == 'left':
            pyautogui.move(-30,0)

        if (left[0].y - left[1].y) < 0.01 and (right[0].y - right[1].y) < 0.01:
            pyautogui.move(0,30)

        elif (left[0].y - left[1].y) < 0.01:
            pyautogui.click()
            
            pyautogui.sleep(1)
        


    cv.imshow('Eye controlled mouse', frame)
    cv.waitKey(1)

capture.release()
cv.desroyAllWindows()

