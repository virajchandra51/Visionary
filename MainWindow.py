# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Start_Stop.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QLabel, QPushButton, QSizePolicy, QTextBrowser,
    QWidget)

class Ui_Visionary(object):
    def setupUi(self, Visionary):
        if not Visionary.objectName():
            Visionary.setObjectName(u"Visionary")
        Visionary.resize(1081, 799)
        Visionary.setStyleSheet(u"QPushButton{\n"
"	background-color:#78B9EB ;\n"
"}\n"
"\n"
"QPushButton:enabled {\n"
"	background-color:#78B9EB ;\n"
"	color: white;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: #0d2f72;\n"
"	color: #fffffe;\n"
"}\n"
"\n"
"QPushButton:hover:!pressed {\n"
"	background-color: #E1F4FF;\n"
"	color: #0c2f70;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"	background-color: #aaaaaa;\n"
"	color: #ffffff;\n"
"}\n"
"\n"
"")
        self.layoutWidget = QWidget(Visionary)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 0, 2, 2))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(Visionary)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(10, 0, 1061, 791))
        self.frame_3.setMinimumSize(QSize(19, 14))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.Start = QPushButton(self.frame_3)
        self.Start.setObjectName(u"Start")
        self.Start.setGeometry(QRect(800, 10, 121, 31))
        font = QFont()
        font.setFamilies([u"Helvetica"])
        font.setPointSize(10)
        font.setBold(False)
        self.Start.setFont(font)
        self.Start.setAutoFillBackground(False)
        self.Start.setStyleSheet(u"QPushButton{\n"
"	background-color:#78B9EB ;\n"
"}\n"
"\n"
"QPushButton:enabled {\n"
"	background-color:#78B9EB ;\n"
"	color: white;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: #0d2f72;\n"
"	color: #fffffe;\n"
"}\n"
"\n"
"QPushButton:hover:!pressed {\n"
"	background-color: #E1F4FF;\n"
"	color: #0c2f70;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"	background-color: #aaaaaa;\n"
"	color: #ffffff;\n"
"}")
        self.Start.setFlat(False)
        self.Stop = QPushButton(self.frame_3)
        self.Stop.setObjectName(u"Stop")
        self.Stop.setGeometry(QRect(930, 10, 121, 31))
        self.Stop.setFont(font)
        self.Stop.setStyleSheet(u"QPushButton{\n"
"	background-color:#78B9EB ;\n"
"}\n"
"\n"
"QPushButton:enabled {\n"
"	background-color:#78B9EB ;\n"
"	color: white;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: #0d2f72;\n"
"	color: #fffffe;\n"
"}\n"
"\n"
"QPushButton:hover:!pressed {\n"
"	background-color: #E1F4FF;\n"
"	color: #0c2f70;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"	background-color: #aaaaaa;\n"
"	color: #ffffff;\n"
"}")
        self.TEXT = QTextBrowser(self.frame_3)
        self.TEXT.setObjectName(u"TEXT")
        self.TEXT.setGeometry(QRect(10, 10, 721, 31))
        font1 = QFont()
        font1.setFamilies([u"Helvetica"])
        self.TEXT.setFont(font1)
        self.image_label = QLabel(self.frame_3)
        self.image_label.setObjectName(u"image_label")
        self.image_label.setGeometry(QRect(10, 50, 1041, 710))
        self.image_label.setFrameShape(QFrame.Box)
        self.image_label.setFrameShadow(QFrame.Raised)
        self.image_label.setLineWidth(5)

        self.retranslateUi(Visionary)

        QMetaObject.connectSlotsByName(Visionary)
    # setupUi

    def retranslateUi(self, Visionary):
        Visionary.setWindowTitle(QCoreApplication.translate("Visionary", u"Visionary", None))
        self.Start.setText(QCoreApplication.translate("Visionary", u"Start Webcam", None))
        self.Stop.setText(QCoreApplication.translate("Visionary", u"Stop Webcam", None))
        self.TEXT.setHtml(QCoreApplication.translate("Visionary", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Helvetica'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2';\"><br /></p></body></html>", None))
        self.image_label.setText("")
    # retranslateUi

