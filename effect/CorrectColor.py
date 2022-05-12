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
import time




ui = uic.loadUiType("color_correction.ui")[0]

class MyWindow(QMainWindow, ui):

    def __init__(self):
        self.chosen_points = []
        super().__init__()
        self.setupUi(self)
        
        self.pb_open.clicked.connect(self.open)
        self.pb_import.clicked.connect(self.OpenImages)
        self.pb_scope.clicked.connect(self.scope)
        
        self.image = None
        
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.histLayout.addWidget(self.canvas)
        
        self.pos = 0
        self.total = 0
        self.img_list = None
        self.width_resize = 480
        self.height_resize = 270
    
    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                            "Open image File",'D:/color/test','All File(*);;"Images (*.png *.jpeg *.jpg *.bmp *.gif)')
        self.filename = fileName
        
        if fileName:
            image = QImage(self.filename)
            if image.isNull():
                QMessageBox.information(self,"Image viewer","Cannot load &s." % fileName)
                return
                
            pixmap = QPixmap.fromImage(image)
            pixmap = pixmap.scaled(QSize(960,540),aspectRatioMode=Qt.KeepAspectRatio)
            self.label.setPixmap(pixmap)
           
            
   
    def ShowImage(self, image=None, fileName=None):
            if image == None:
                fileName = self.img_list[self.pos]
                image = QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer",
                                        "Cannot load %s." % fileName)
                return
            image = cv2.imread(self.img_list[self.pos])
            self.label.setPixmap(QPixmap.fromImage(image))

    def OpenImages(self):
            
        img_list,_ = QFileDialog.getOpenFileNames(self,"Open Folder",'','All File(*.png *.jpg()')
        
        self.img_list = img_list
        
        self.total = len(img_list)
        if img_list:
            image = cv2.imread(self.img_list[self.pos])
            self.ShowImage(image = self.toQImage(image))
    
    def toQImage(self, im, copy=False):
        if im is None:
            return QImage()
        if im.dtype == np.uint8:
            if len(im.shape) == 2:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
                qim.setColorTable(self.gray_color_table)
                return qim.copy() if copy else qim
            elif len(im.shape) == 3:
                if im.shape[2] == 3:
                    qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888)
                    return qim.copy() if copy else qim
                elif im.shape[2] == 4:
                    qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_ARGB32)
                    return qim.copy() if copy else qim    
          
  
           
    def keyPressEvent(self, e):
        if e.key() == 65:
            if not self.pos == 0:
                self.pos -= 1
                image = cv2.imread(self.img_list[self.pos])
                """
                이미지 처리
                """
                self.ShowImage(image=self.toQImage(image))
                print('\r' + self.img_list[self.pos], end="")
               
                                                
        elif e.key() == 68:
            self.pos += 1
            if self.total == self.pos:
                self.pos -= 1
            image = cv2.imread(self.img_list[self.pos])
            """
            이미지 처리
            """
            self.ShowImage(image=self.toQImage(image))
            print('\r' + self.img_list[self.pos], end="")
   
                       
            
    def ShowWaveform(self):
        src = cv2.imread(self.filename,0)
        img = cv2.resize(src,(self.width_resize,self.height_resize))
        img_h = img.shape[0]
        img_w = img.shape[1]
        # div = 2
        # scope_w = int(img_w/div)
        
        scope_w = img_w
        div = round(img_w/scope_w)

       
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
        src = cv2.imread(self.filename)
        cimg = cv2.resize(src,(self.width_resize,self.height_resize))
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
        src = cv2.imread(self.filename,0)
        img = cv2.resize(src,(self.width_resize,self.height_resize))
        hist = cv2.calcHist([img],[0],None,[256],[0,256])
        
        
        histPlot = self.fig.add_subplot(212)
        histPlot.plot(hist)
        self.canvas.draw()
        
        
    def ShowVectorScope(self):
        start = time.time()
        scale_factor = 2
        src_ = cv2.imread(self.filename)
        src = cv2.resize(src_,(self.width_resize,self.height_resize))
        print("src size: ",src.shape)
        
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
        outerlineColor_iq = (0,60,60)
        outerlineThick = 1

        cv2.circle(dst,(center_x, center_y),radius, outerlineColor,outerlineThick+1,8)


        cv2.line(dst,(center_x-radius, center_y),(center_x+radius,center_y),outerlineColor,outerlineThick+1)
        cv2.line(dst,(center_x, center_y-radius),(center_x,center_y+radius),outerlineColor,outerlineThick+1)

        #draw I/Q lines
        rad_iq = 33. *math.pi/180.
        grid_x = int(np.float(center_x) + np.float64(radius)*math.cos(rad_iq))
        grid_y = int(np.float(center_y) - np.float64(radius)*math.sin(rad_iq))
        grid_x_end = int(np.float(center_x) + np.float64(radius)*math.cos(rad_iq+math.pi))
        grid_y_end = int(np.float(center_y) - np.float64(radius)*math.sin(rad_iq+math.pi))
        cv2.line(dst,(grid_x, grid_y),(grid_x_end, grid_y_end),outerlineColor_iq,outerlineThick)

        grid_x = int(np.float(center_x) + np.float64(radius)*math.cos(math.pi*0.5+rad_iq))
        grid_y = int(np.float(center_y) - np.float64(radius)*math.sin(math.pi*0.5+rad_iq))
        grid_x_end = int(np.float(center_x) + np.float64(radius)*math.cos(math.pi*1.5+rad_iq))
        grid_y_end = int(np.float(center_y) - np.float64(radius)*math.sin(math.pi*1.5+rad_iq))
        cv2.line(dst,(grid_x, grid_y),(grid_x_end, grid_y_end),outerlineColor_iq,outerlineThick)
                
        col_name = ["B","Cy","G","Y","R","M"] 
        fontType = cv2.FONT_HERSHEY_SIMPLEX
        vec = [-20, -80, -120, -190, -250, -300]   
            
        for v,c in zip(vec,col_name):
            rad_iq = v *math.pi/180.
            x = int(np.float(center_x) + np.float64(radius)*0.7*math.cos(rad_iq))
            y = int(np.float(center_y) - np.float64(radius)*0.7*math.sin(rad_iq))
            cv2.putText(dst,c,(x,y),fontType,1,outerlineColor,outerlineThick,16)


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
        print("time: ", time.time()-start)

        cv2.waitKey(0)
        
  
     
            
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