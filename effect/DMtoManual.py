import sys
from xml.etree.ElementTree import tostring
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QPushButton, QSizePolicy
from PyQt5.QtWidgets import QFileDialog, QStatusBar
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import json
import os

ui = uic.loadUiType("JsonChange.ui")[0]


class MyWindow(QMainWindow, ui):
    
    def __init__(self):
        self.chosen_points = []
        super().__init__()
        self.setupUi(self)
        
        self.pb_import.clicked.connect(self.open)
        self.pb_change.clicked.connect(self.change)
        self.pb_export.clicked.connect(self.save)
        self.filename=[]
        self.text = []
        self.json_data =[]
        self.radio_pts_toDM.setChecked(True)
        
    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                            "Open pts File","D:/test/calib",'All File(*)')
       # self.filename = fileName
        
        with open(fileName, "r") as json_file:
            json_data = json.load(json_file)
        self.json_data = json_data
        
        text = json.dumps(json_data, indent =4)
        self.before.text = QTextBrowser(self.before)
        self.before.setText(text)
        self.text = text

    def change(self):
       # self.after.setText(self.text)
        if self.radio_pts.isChecked():
            json_data ={
                "stadium":None,
                "world_coords":{
                    "X1":0,
                    "X2":0
                },
                "points":None
            }

        # json_data['points'] = len(self.json_data['points'])
            points = [len(self.json_data['points'])]
            print(len(points))
            
        
            json_data['stadium'] = self.json_data['worlds'][0]['stadium']
            json_data['world_coords'] = self.json_data['worlds'][0]['world_coords']
            
            # for i in range(len(self.json_data['points'])): 
            #     points[i] = self.json_data['points'][i]['dsc_id']
                #json_data['points'] = self.json_data['points']
        #  json_data['points'].append(self.json_data['points'])
            json_data['points'] = self.json_data['points']
        
        
        if self.radio_pts_toDM.isChecked():
            json_data = {
                "RecordName" : None,
                "PreSetNumber" : 0,
                "worlds" : [
                    {
                            
                        "group":None,
                        "stadium":None,
                        "world_coords":None
                    }
                ]
                    ,
                "points" : None
            }
            json_data['worlds'][0]['group'] = "Group1"
            json_data['worlds'][0]['stadium'] = self.json_data['stadium']
            json_data['worlds'][0]['world_coords'] = self.json_data['world_coords']
            
            
            json_data['points'] = self.json_data['points']
        
            for i in range(len(self.json_data['points'])): 
                json_data['points'][i]['dsc_id'] = self.json_data['points'][i]['dsc_id']
                json_data['points'][i]['point_index'] = 1
                json_data['points'][i]['framenum'] = 181
                json_data['points'][i]['camfps'] = 30
                json_data['points'][i]['flip'] = 0
                json_data['points'][i]['Group'] = "Group1"
                json_data['points'][i]['Width'] = 3840
                json_data['points'][i]['Height'] = 2160
                json_data['points'][i]['infection_point'] = 0
                json_data['points'][i]['swipe_base_length'] = -1.0
                json_data['points'][i]['ManualOffesetY'] = 0
                json_data['points'][i]['FocalLength'] = 14.0
                json_data['points'][i]['pts_2d'] = self.json_data['points'][i]['pts_2d']
                json_data['points'][i]['pts_3d'] = self.json_data['points'][i]['pts_3d']               

                json_data['points'][i]['pts_2d']['Upper'] = {"IsEmpty":None,"X":0,"Y":0}
                json_data['points'][i]['pts_2d']['Upper']['IsEmpty'] = False
                json_data['points'][i]['pts_2d']['Upper']['X'] = self.json_data['points'][i]['pts_2d']['UpperPosX']
                json_data['points'][i]['pts_2d']['Upper']['Y'] = self.json_data['points'][i]['pts_2d']['UpperPosY']
                json_data['points'][i]['pts_2d']['Middle'] = {"IsEmpty":None,"X":0,"Y":0}
                json_data['points'][i]['pts_2d']['Middle']['IsEmpty'] = False
                json_data['points'][i]['pts_2d']['Middle']['X'] = self.json_data['points'][i]['pts_2d']['MiddlePosX']
                json_data['points'][i]['pts_2d']['Middle']['Y'] = self.json_data['points'][i]['pts_2d']['MiddlePosY']
                json_data['points'][i]['pts_2d']['Lower'] = {"IsEmpty":None,"X":0,"Y":0}
                json_data['points'][i]['pts_2d']['Lower']['IsEmpty'] = False
                json_data['points'][i]['pts_2d']['Lower']['X'] = self.json_data['points'][i]['pts_2d']['LowerPosX']
                json_data['points'][i]['pts_2d']['Lower']['Y'] = self.json_data['points'][i]['pts_2d']['LowerPosY']

                json_data['points'][i]['pts_3d']['Point1'] = {"IsEmpty":None,"X":0,"Y":0}
                json_data['points'][i]['pts_3d']['Point1']['IsEmpty'] = False
                json_data['points'][i]['pts_3d']['Point1']['X'] = self.json_data['points'][i]['pts_3d']['X1']
                json_data['points'][i]['pts_3d']['Point1']['Y'] = self.json_data['points'][i]['pts_3d']['Y1']
                json_data['points'][i]['pts_3d']['Point2'] = {"IsEmpty":None,"X":0,"Y":0}
                json_data['points'][i]['pts_3d']['Point2']['IsEmpty'] = False
                json_data['points'][i]['pts_3d']['Point2']['X'] = self.json_data['points'][i]['pts_3d']['X2']
                json_data['points'][i]['pts_3d']['Point2']['Y'] = self.json_data['points'][i]['pts_3d']['Y2']
                json_data['points'][i]['pts_3d']['Point3'] = {"IsEmpty":None,"X":0,"Y":0}
                json_data['points'][i]['pts_3d']['Point3']['IsEmpty'] = False
                json_data['points'][i]['pts_3d']['Point3']['X'] = self.json_data['points'][i]['pts_3d']['X3']
                json_data['points'][i]['pts_3d']['Point3']['Y'] = self.json_data['points'][i]['pts_3d']['Y3']
                json_data['points'][i]['pts_3d']['Point4'] = {"IsEmpty":None,"X":0,"Y":0}
                json_data['points'][i]['pts_3d']['Point4']['IsEmpty'] = False
                json_data['points'][i]['pts_3d']['Point4']['X'] = self.json_data['points'][i]['pts_3d']['X4']
                json_data['points'][i]['pts_3d']['Point4']['Y'] = self.json_data['points'][i]['pts_3d']['Y4']
                
                json_data['points'][i]['pts_swipe'] = {"X1" : 0, "Y1":0, "X2": 0 , "Y2": 0}
                json_data['points'][i]['pts_swipe']['X1']=-1.0
                json_data['points'][i]['pts_swipe']['Y1']=-1.0
                json_data['points'][i]['pts_swipe']['X2']=-1.0
                json_data['points'][i]['pts_swipe']['Y2']=-1.0
        
        
        if self.radio_adj.isChecked():
            json_data ={
                "mode":1,
                "adjust_list":None
            }
            json_data['adjust_list'] = self.json_data['adjust_list']
            AdjustX = self.json_data['adjust_list'][0]['adjust']['AdjustX']
            AdjustY = self.json_data['adjust_list'][0]['adjust']['AdjustY']
            RotateX = self.json_data['adjust_list'][0]['adjust']['RotateX']
            RotateY = self.json_data['adjust_list'][0]['adjust']['RotateY']
            Width = self.json_data['adjust_list'][0]['adjust']['RectMargin']['Width']
            Height = self.json_data['adjust_list'][0]['adjust']['RectMargin']['Height']
            
            if(AdjustX!=0):
                normAdjustX = Width/AdjustX
            else:
                normAdjustX = 0
            if(AdjustY!=0):
                normAdjustY = Height/AdjustY
            else:
                normAdjustY = 0
                  
            json_data['adjust_list'][0]['adjust']['normAdjustX'] = normAdjustX
            
        
        data= json.dumps(json_data,indent=4)   
        self.after.setText(data)          
        self.text = data
        
    def save(self):
        
        if self.radio_pts.isChecked():
            FileSave,_ = QFileDialog.getSaveFileName(self, 'Save file','D:/test/calib','.pts')
        if self.radio_pts_toDM.isChecked():
            FileSave,_ = QFileDialog.getSaveFileName(self, 'Save file','D:/test/calib','.pts')
        if self.radio_adj.isChecked():
            FileSave,_ = QFileDialog.getSaveFileName(self, 'Save file','D:/test/calib','.adj')
    
        file = open(FileSave,'w')
        text = self.text
        file.write(text)
        file.close()
        
        
        
        
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
        
        
os.system('pause')