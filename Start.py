import sys
import cv2
from PySide6 import QtWidgets, QtCore
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton
from PySide6.QtGui import QIcon

loader = QUiLoader()
class tehseencode(QDialog):
    def _init_(self):
        self.setWindowTitle("Visionary")
        self.setWindowIcon(QIcon("logo.png"))

    @QtCore.Slot()
    def onClicked(self):
        self.TEXT.setText('Press Stop to Close to Webcam :(')
        cap = cv2.VideoCapture(0)

        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:

                # -------------written casually we can comment i, just to show how fast its running
                print('here')
                self.displayImage(frame, 1)
                cv2.waitKey()

        cap.release()
        cv2.destroyAllWindows()
        
    
app = QtWidgets.QApplication(sys.argv)
window = loader.load("Start_Stop.ui", None)
window.show()
app.exec()