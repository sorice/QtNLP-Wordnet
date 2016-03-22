#!/usr/bin/python
# -*- coding: utf-8 -*-

# main core file

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from QtNLP_Wordnet_UI import Ui_MainWindow


class Wordnet( QMainWindow, Ui_MainWindow):

    def __init__( self, parent = None ):
        # init the parent
        super( Wordnet, self ).__init__( parent )
        # setup the UI
        self.setupUi( self )
        self.comboBox.setEditable(1)
        self.i = 0
        
        #~ self.pushButton.clicked.connect( self.insertRow )

    # SLOTS !!!
    #~ def insertRow(self):
    #~ @pyqtSignature('')
    def on_pushButton_clicked(self):
        self.tableWidget.setVerticalHeaderItem(self.i,QTableWidgetItem("hola"))
        a = self.tableWidget.rowCount()
        print a
        b = QTableWidgetItem("Prueba")
        c = QTableWidgetItem("synset")
        self.tableWidget.insertRow(1)
        self.tableWidget.setVerticalHeaderItem(1,c)
        self.tableWidget.setHorizontalHeaderItem(0,QTableWidgetItem("synset_2"))
        self.tableWidget.setItem(0,0,b)
