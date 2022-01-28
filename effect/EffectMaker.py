import sys
from xml.etree.ElementTree import tostring
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QPushButton, QSizePolicy
from PyQt5.QtWidgets import QFileDialog, QStatusBar
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import cv2
import os
import numpy as np

ui = uic.loadUiType("effect.ui")[0]

class MyWindow(QMainWindow, ui):

    def __init__(self):
        self.chosen_points = []
        super().__init__()
        self.setupUi(self)
        
        self.filename = './icehockey.mp4'
        
        self.key =10
        self.bt_start.clicked.connect(self.play)
        self.bt_track.clicked.connect(self.track)
    
    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                            "Open Video File",'','All File(*);;"Videos (*.mov *.mp4 *.avi *.wmv *.mkv)')
        self.filename = fileName
    
    def play(self):
        cap = cv2.VideoCapture(self.filename)
        
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        self.fps = fps
        self.cap = cap

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("No Frame.")
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h,w,c = frame.shape
            self.frame = frame
            self.qimg = QImage(frame.data,w,h,w*c,QImage.Format_RGB888)
            
            pixmap = QPixmap.fromImage(self.qimg)
            self.p = pixmap.scaled(self.label.size(),Qt.KeepAspectRatio)
            self.label.setPixmap(self.p)
            
            if cv2.waitKey(self.key)==ord('q'):
                break
            if cv2.waitKey(self.key)==ord('p'):
                cv2.waitKey(-1)
            if(cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT)):
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                
                
            
        cap.release()
            
    def track(self):
        
        frame = self.play.frame
        tracker = cv2.TrackerCSRT_create()
        
        rc = cv2.selectROI('frame',frame)
        tracker.init(frame,rc)
        self.play.ret, rc = tracker.update(frame)
        
        rc = tuple([int(_) for _ in rc])
        cv2.rectangle(frame,rc,(0,0,255),8)
        
        
        





if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()