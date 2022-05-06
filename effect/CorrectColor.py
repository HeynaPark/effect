import sys
from xml.etree.ElementTree import tostring
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QPushButton, QSizePolicy
from PyQt5.QtWidgets import QFileDialog, QStatusBar
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtGui
import cv2
import os
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

ui = uic.loadUiType("color_correction.ui")[0]

class MyWindow(QMainWindow, ui):

    def __init__(self):
        self.chosen_points = []
        super().__init__()
        self.setupUi(self)
        
        self.pb_open.clicked.connect(self.open)
        self.pb_scope.clicked.connect(self.scope)
        
        self.image = None
        
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.histLayout.addWidget(self.canvas)
        
     
        
    
    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                            "Open Video File",'','All File(*);;"Images (*.png *.jpeg *.jpg *.bmp *.gif)')
        self.filename = fileName
        
        if fileName:
            image = QImage(self.filename)
            if image.isNull():
                QMessageBox.information(self,"Image viewer","Cannot load &s." % fileName)
                return
                
            pixmap = QPixmap.fromImage(image)
            pixmap = pixmap.scaled(QSize(960,540),aspectRatioMode=Qt.KeepAspectRatio)
            self.label.setPixmap(pixmap)
           
            
            
    def ShowWaveform(self):
        img = cv2.imread(self.filename,0)
        img_h = img.shape[0]
        img_w = img.shape[1]
        # div = 2
        # scope_w = int(img_w/div)
        
        scope_w = img_w
        div = round(img_w/scope_w)
        
        #scope_len = int(img_w/div)
        #scope_len = int(img_w/8)
        #scope_w = int(img_w/4)
       
        bw_color_scope = np.zeros((256,scope_w+1), dtype=int)
        
        for width in range(scope_w):
            vals, cnts = np.unique(img[:,width*div:(width+1)*div],return_counts=True)   #세로줄의 value 탐색
            for valCnt in range(len(vals)):
                if cnts[valCnt]<255:
                    bw_color_scope[-(vals[valCnt]-255)][width] = cnts[valCnt]
                else:
                    bw_color_scope[-(vals[valCnt]-255)][width]= 255
        
        plt.subplot(2,2,1)            
        plt.imshow(bw_color_scope, 'gray')
        plt.title('Waveform'),plt.xticks([]),plt.yticks([])
        plt.show() 
        
        wavePlot = self.fig.add_subplot(211)
        wavePlot.plot(bw_color_scope)
        self.canvas.draw()
        
    def ShowWaveformRGB(self):
        cimg = cv2.imread(self.filename)
        b,g,r = cv2.split(cimg)    
        
        img_w = cimg.shape[1]
      
        #scope_len = int(img_w/div)
        scope_len = img_w
        div = int(img_w/scope_len)
        
        b_color_scope = np.zeros((256, scope_len+1), dtype=int)
        g_color_scope = np.zeros((256, scope_len+1), dtype=int)
        r_color_scope = np.zeros((256, scope_len+1), dtype=int)
        background = np.zeros((256,scope_len+1),dtype=int)
        
        for width in range(scope_len):
            vals, cnts = np.unique(b[:,width*div:(width+1)*div],return_counts=True) 
            for valCnt in range(len(vals)):
                if cnts[valCnt]<255:
                    b_color_scope[-(vals[valCnt]-255)][width] = cnts[valCnt]
                else:
                    b_color_scope[-(vals[valCnt]-255)][width]= 255
                    
        for width in range(scope_len):
            vals, cnts = np.unique(g[:,width*div:(width+1)*div],return_counts=True) 
            for valCnt in range(len(vals)):
                if cnts[valCnt]<255:
                    g_color_scope[-(vals[valCnt]-255)][width] = cnts[valCnt]
                else:
                    g_color_scope[-(vals[valCnt]-255)][width]= 255
       
        for width in range(scope_len):
            vals, cnts = np.unique(r[:,width*div:(width+1)*div],return_counts=True) 
            for valCnt in range(len(vals)):
                if cnts[valCnt]<255:
                    r_color_scope[-(vals[valCnt]-255)][width] = cnts[valCnt]
                else:
                    r_color_scope[-(vals[valCnt]-255)][width]= 255
        
        b_show_color_scope = cv2.merge((b_color_scope,background,background))
        b_plt_color_scope = cv2.merge((background,background,b_color_scope))
        plt.subplot(222)
        plt.imshow(b_plt_color_scope)
        plt.title('Blue Color Scope'),plt.xticks([]), plt.yticks([])
        plt.show()
       
        g_show_color_scope = cv2.merge((background,g_color_scope,background))
       # g_plt_color_scope = cv2.merge((background,g_color_scope,background))
        plt.subplot(223)
        plt.imshow(g_show_color_scope)
        plt.title('Green Color Scope'),plt.xticks([]), plt.yticks([])
        plt.show()
        
        r_show_color_scope = cv2.merge((background,background,r_color_scope))
        r_plt_color_scope = cv2.merge((r_color_scope, background,background))
        plt.subplot(224)
        plt.imshow(r_plt_color_scope)
        plt.title('Red Color Scope'),plt.xticks([]), plt.yticks([])
        plt.draw()
        
        
        
    def ShowHistogram(self):
        img = cv2.imread(self.filename,0)
        hist = cv2.calcHist([img],[0],None,[256],[0,256])
        
        # plt.figure(2)
        # plt.title('Histogram')
        # plt.plot(hist)
        # plt.show()
        
        histPlot = self.fig.add_subplot(212)
        histPlot.plot(hist)
        self.canvas.draw()
        
    def ShowVectorScope(self):
        margin = 10
        dotRadius = 2
        vectorLen =8
            
    def scope(self):
        self.ShowWaveform()
        self.ShowHistogram()
        self.ShowWaveformRGB()
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()