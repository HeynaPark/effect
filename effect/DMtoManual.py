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
        data= json.dumps(json_data,indent=4)
        
        self.after.setText(data)
        
        self.text = data
        
    def save(self):
        FileSave,_ = QFileDialog.getSaveFileName(self, 'Save file','D:/test/calib','.pts')
        file = open(FileSave,'w')
        text = self.text
        file.write(text)
        file.close()
        
        
        
        
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
        
        
        