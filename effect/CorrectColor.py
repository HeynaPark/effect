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
import math
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
        
        plt.subplot(1,2,1)            
        plt.imshow(bw_color_scope, 'gray')
        plt.title('Waveform'),plt.xticks([]),plt.yticks([])
        plt.show() 
        
        wavePlot = self.fig.add_subplot(211)
        wavePlot.plot(bw_color_scope)
        self.canvas.draw()
        
    def ShowRGBparade(self):
        cimg = cv2.imread(self.filename)
        b,g,r = cv2.split(cimg)    
        
        img_w = cimg.shape[1]
      
        #scope_len = int(img_w/div)
        scope_len = int(img_w/4)
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
    
        g_show_color_scope = cv2.merge((background,g_color_scope,background))

        
        r_show_color_scope = cv2.merge((background,background,r_color_scope))
        r_plt_color_scope = cv2.merge((r_color_scope, background,background))


        temp = np.hstack((r_plt_color_scope,g_show_color_scope))
        parade = np.hstack((temp,b_plt_color_scope))
        
        plt.subplot(122)
        plt.imshow(parade)
        plt.title('RGB parade'),plt.xticks([]), plt.yticks([])
        plt.show()
       
        
        
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
        scale_factor = 2
        src = cv2.imread(self.filename)
        B, G, R = src[:,:,0], src[:,:,1], src[:,:,2]

        Y = (0.299 * R) + (0.587 * G) + (0.114 * B)
        Cb = (-0.169 * R) - (0.331 * G) + (0.499 * B) + 128*scale_factor
        Cr = (0.499 * R) - (0.418 * G) - (0.0813 * B) + 128*scale_factor

        # traditional vectorscope orientation:
        Cr = 256*scale_factor - Cr
        #Cb = 256-Cb

        cols = 512
        rows = 512
        margin = 10


        dst = np.zeros((cols, rows, 3), dtype=src.dtype)

        center_x = int(cols/2)
        center_y = int(rows/2)

        radius = int(rows/2 - margin)

        outerlineColor = (0,100,100)
        outerlineThick = 1

        cv2.circle(dst,(center_x, center_y),radius, outerlineColor,outerlineThick,8)


        cv2.line(dst,(center_x-radius, center_y),(center_x+radius,center_y),outerlineColor,outerlineThick)
        cv2.line(dst,(center_x, center_y-radius),(center_x,center_y+radius),outerlineColor,outerlineThick)

        #draw I/Q lines
        rad_iq = 33. *math.pi/180.
        grid_x = int(np.float(center_x) + np.float64(radius)*math.cos(rad_iq))
        grid_y = int(np.float(center_y) - np.float64(radius)*math.sin(rad_iq))
        grid_x_end = int(np.float(center_x) + np.float64(radius)*math.cos(rad_iq+math.pi))
        grid_y_end = int(np.float(center_y) - np.float64(radius)*math.sin(rad_iq+math.pi))
        cv2.line(dst,(grid_x, grid_y),(grid_x_end, grid_y_end),outerlineColor,outerlineThick)



        #draw grid
        large_thick_ratio = 0.99
        small_thick_ratio = 0.95

        for i in range(0,360,5):
            theta = np.float64(i)/180*math.pi
            if(i%10)==10:
                r_s = np.float64(radius)*large_thick_ratio
            else:
                r_s = np.float64(radius)*small_thick_ratio
            xs =  int(np.float(center_x) + np.float64(radius)*math.cos(theta))
            ys =  int(np.float(center_y) - np.float64(radius)*math.sin(theta))
            xe =  int(np.float(center_x) + np.float64(r_s)*math.cos(theta))
            ye =  int(np.float(center_y) - np.float64(r_s)*math.sin(theta))
            cv2.line(dst,(xs,ys),(xe,ye),outerlineColor,outerlineThick)

        for x in range(src.shape[0]):
            for y in range(src.shape[1]):
                dst[int(Cr[x, y]), int(Cb[x, y])] = np.array([B[x, y], G[x, y], R[x, y]])

        cv2.imshow('vectorscope',dst)

        cv2.waitKey(0)
        
        # plt.subplot(2,2,4)            
        # plt.imshow(dst, 'vectorscope')
        # plt.title('vectorscope'),plt.xticks([]),plt.yticks([])
        # plt.show() 
           
           
           
           
            
    def scope(self):
        self.ShowWaveform()
        self.ShowHistogram()
        self.ShowRGBparade()
        self.ShowVectorScope()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()