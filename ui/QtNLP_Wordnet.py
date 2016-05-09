#!/usr/bin/python
# -*- coding: utf-8 -*-

# main core file
from string import lower
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from QtNLP_Wordnet_UI import Ui_MainWindow
from QtNLP_Wordnet_Editor_UI import Ui_MainWindow as df
import sqlite3,sys


class Wordnet(QMainWindow, Ui_MainWindow):

    def __init__( self, parent = None ):
        # init the parent
        super( Wordnet, self ).__init__( parent )
        # setup the UI
        self.setupUi( self )

        self.__connect = sqlite3.connect("./data/wordnet.db3")
        self.__cursor = self.__connect.cursor()
        self.__row = 0
        self.__max_row = 0
        self.__column = 1

        self.pushButton.clicked.connect( self.insertRow)
        self.comboBox.editTextChanged.connect( self.actualizar )

        self.pushButton_2.clicked.connect( self.insertSynonyms)
        self.pushButton_3.clicked.connect( self.insertAntonyms)
        self.pushButton_4.clicked.connect( self.mostar)

    # SLOTS !!!
    def actualizar(self):
        cant_row = self.tableWidget.rowCount()
        self.listWidget.clear()
        if(cant_row!=-0):
            while(cant_row!=0):
               self.tableWidget.removeRow(cant_row)
               cant_row -=1
            self.tableWidget.removeRow(0)
            self.__row = 0
            self.__max_row = 0
            self.__column = 1

    def insertRow(self):
    #@pyqtSignature('')
    #def on_pushButton_clicked(self):

        str = "SELECT ss_type,synset_offset,sense_number,tag_cnt FROM [index_sense] WHERE [lemma]='"+self.comboBox.currentText()+"' ORDER BY [ss_type],[sense_number]"
        self.__cursor.execute(unicode(str))
        result = self.__cursor.fetchall()

        #for co in result:
         #    self.tableWidget.removeRow(self.__max_row)
          #   self.__max_row -= 1
        #print result
        #self.tableWidget.setItem(self.__p_type,self.__p_type,QTableWidgetItem(self.comboBox.currentText()))
        for con in result:
             self.tableWidget.insertRow(self.__max_row)
             self.__max_row += 1
        #aux = 1

        #while(aux<6):
         #str1 = "SELECT COUNT(ss_type) FROM [index_sense] WHERE [lemma]='"+self.comboBox.currentText()+"' AND [ss_type]='"+str(aux)+"'"
         #self.__cursor.execute(unicode(str1))
         #cant = self.__cursor.fetchall()
         #self.__cant_type.append(int(cant))
         #aux += 1


        for a, b, c, d in result:
            if(a==1):
                self.tableWidget.setItem(self.__row,0,QTableWidgetItem("noun"))
                str = "SELECT [sense], [sense_es], [sense_long], [sense_long_es], [gloss], [gloss_es] FROM [data_noun] WHERE [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                data = self.__cursor.fetchall()

                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][0]))
                self.__column += 1
                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][1]))
                self.__column += 1
                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][2]))
                self.__column += 1
                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][3]))
                self.__column += 1
                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][4]))
                self.__column += 1
                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][5]))
            if(a==2):
                self.tableWidget.setItem(self.__row,0,QTableWidgetItem("verb"))
                str = "SELECT [sense], [sense_es], [sense_long], [sense_long_es], [gloss], [gloss_es] FROM [data_verb] WHERE [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                data = self.__cursor.fetchall()

                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][0]))
                self.__column += 1
                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][1]))
                self.__column += 1
                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][2]))
                self.__column += 1
                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][3]))
                self.__column += 1
                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][4]))
                self.__column += 1
                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][5]))
            if(a==3 or a==5):
                self.tableWidget.setItem(self.__row,0,QTableWidgetItem("adj"))
                str = "SELECT [sense], [sense_es], [sense_long], [sense_long_es], [gloss], [gloss_es] FROM [data_adj] WHERE [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                data = self.__cursor.fetchall()

                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][0]))
                self.__column += 1
                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][1]))
                self.__column += 1
                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][2]))
                self.__column += 1
                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][3]))
                self.__column += 1
                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][4]))
                self.__column += 1
                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][5]))
            if(a==4):
                self.tableWidget.setItem(self.__row,0,QTableWidgetItem("verb"))
                str = "SELECT [sense], [sense_es], [sense_long], [sense_long_es], [gloss], [gloss_es] FROM [data_adv] WHERE [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                data = self.__cursor.fetchall()

                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][0]))
                self.__column += 1
                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][1]))
                self.__column += 1
                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][2]))
                self.__column += 1
                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][3]))
                self.__column += 1
                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][4]))
                self.__column += 1
                self.tableWidget.setItem(self.__row,self.__column,QTableWidgetItem(data[0][5]))

            self.__column = 1
            self.__row += 1
        self.insertSynonyms()

    def insertSynonyms(self):
            self.listWidget.clear()
            str = "SELECT DISTINCT([data_noun_word_lex_id].[word]) FROM ([index_sense] INNER JOIN [data_noun_word_lex_id] USING([synset_offset])) WHERE [index_sense].[lemma]='"+self.comboBox.currentText()+"'"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()

            if  result:
             for w in result:
               if(self.comboBox.currentText().toLower()!=lower(w[0])):
                self.listWidget.addItem(w[0])
            str = "SELECT DISTINCT([data_verb_word_lex_id].[word]) FROM ([index_sense] INNER JOIN [data_verb_word_lex_id] USING([synset_offset])) WHERE [index_sense].[lemma]='"+self.comboBox.currentText()+"'"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()

            if result:
             for w in result:
                 if(self.comboBox.currentText().toLower()!=lower(w[0])):
                    self.listWidget.addItem(w[0])
            str = "SELECT DISTINCT([data_adj_word_lex_id].[word]) FROM ([index_sense] INNER JOIN [data_adj_word_lex_id] USING([synset_offset])) WHERE [index_sense].[lemma]='"+self.comboBox.currentText()+"'"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()

            if result:
                for w in result:
                  if(self.comboBox.currentText().toLower()!=lower(w[0])):
                    self.listWidget.addItem(str(w[0]))
            str = "SELECT DISTINCT([data_adv_word_lex_id].[word]) FROM ([index_sense] INNER JOIN [data_adv_word_lex_id] USING([synset_offset])) WHERE [index_sense].[lemma]='"+self.comboBox.currentText()+"'"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:
                for w in result:
                    if(self.comboBox.currentText().toLower() != lower(w[0])):
                        self.listWidget.addItem(w[0])


    def insertAntonyms(self):
            self.listWidget.clear()

            str = "SELECT DISTINCT([data_noun_ptr].[synset_offset_p]) FROM [index_sense]  INNER JOIN [data_noun_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.comboBox.currentText()+"'AND [data_noun_ptr].[pointer_symbol]='!'"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:
                for w in result:
                  str = "SELECT DISTINCT(word) FROM [data_noun_word_lex_id] WHERE [synset_offset]='"+w[0]+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  for a in data:
                        self.listWidget.addItem(a[0])

            str = "SELECT DISTINCT([data_verb_ptr].[synset_offset_p]) FROM [index_sense]  INNER JOIN [data_verb_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.comboBox.currentText()+"'AND [data_verb_ptr].[pointer_symbol]='!'"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:
                for w in result:
                  str = "SELECT DISTINCT(word) FROM [data_verb_word_lex_id] WHERE [synset_offset]='"+w[0]+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  for a in data:
                        self.listWidget.addItem(a[0])

            str = "SELECT DISTINCT([data_adj_ptr].[synset_offset_p]) FROM [index_sense]  INNER JOIN [data_adj_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.comboBox.currentText()+"'AND [data_adj_ptr].[pointer_symbol]='!'"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:
                for w in result:
                  str = "SELECT DISTINCT(word) FROM [data_adj_word_lex_id] WHERE [synset_offset]='"+w[0]+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  for a in data:
                        self.listWidget.addItem(a[0])

            str = "SELECT DISTINCT([data_adv_ptr].[synset_offset_p]) FROM [index_sense]  INNER JOIN [data_adv_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='" + self.comboBox.currentText() + "'AND [data_adv_ptr].[pointer_symbol]='!'"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:
                for w in result:
                  str = "SELECT DISTINCT(word) FROM [data_adv_word_lex_id] WHERE [synset_offset]='"+w[0]+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  for a in data:
                        self.listWidget.addItem(a[0])






            #print self.comboBox.currentText()
            #str = "SELECT DISTINCT(word) FROM [data_noun_word_lex_id] WHERE [synset_offset]=(SELECT DISTINCT([data_noun_ptr].[synset_offset_p]) FROM [index_sense]  INNER JOIN [data_noun_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.comboBox.currentText()+"' AND [data_noun_ptr].[pointer_symbol]='!')"
            #self.__cursor.execute(unicode(str))
            #result = self.__cursor.fetchall()
            #if result:
            #    for w in result:
            #      self.listWidget.addItem(w[0])

            #str = "SELECT DISTINCT(word) FROM [data_verb_word_lex_id] WHERE [synset_offset]=(SELECT DISTINCT([data_verb_ptr].[synset_offset_p]) FROM [index_sense]  INNER JOIN [data_verb_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.comboBox.currentText()+"' AND [data_verb_ptr].[pointer_symbol]='!')"
            #self.__cursor.execute(unicode(str))
            #result = self.__cursor.fetchall()
            #if result:
            #    for w in result:
            #      self.listWidget.addItem(w[0])

            #str = "SELECT DISTINCT(word) FROM [data_adj_word_lex_id] WHERE [synset_offset]=(SELECT DISTINCT([data_adj_ptr].[synset_offset_p]) FROM [index_sense]  INNER JOIN [data_adj_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.comboBox.currentText()+"' AND [data_adj_ptr].[pointer_symbol]='!')"
            #self.__cursor.execute(unicode(str))
            #result = self.__cursor.fetchall()
            #if result:
            #    for w in result:
            #      self.listWidget.addItem(w[0])

            #str = "SELECT DISTINCT(word) FROM [data_adv_word_lex_id] WHERE [synset_offset]=(SELECT DISTINCT([data_adv_ptr].[synset_offset_p]) FROM [index_sense]  INNER JOIN [data_adv_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.comboBox.currentText()+"' AND [data_adv_ptr].[pointer_symbol]='!')"
            #self.__cursor.execute(unicode(str))
            #result = self.__cursor.fetchall()
            #if result:
            #    for w in result:
            #      self.listWidget.addItem(w[0])
    def mostar(self):
        #Wordnet()
        edit = QApplication( sys.argv )
        edit.exit()
        e = WordnetEdit()
        e.show()
        sys.exit( edit.exec_() )

class WordnetEdit( QMainWindow, df):

    def __init__( self, parent = None ):
        # init the parent
        super( WordnetEdit, self ).__init__( parent )
        # setup the UI
        self.setupUi( self )

        self.__connect = sqlite3.connect("./data/wordnet.db3")
        self.__cursor = self.__connect.cursor()

        self.__bbook = []
        self.__filasel = []
        self.__filword = []
        self.__allsynon = []
        self.__allsynondown = []

        self.__max_row1 = 0
        self.__row1 = 0
        self.__column1 = 1
        self.__row = 0

        self.__max_row2 = 0
        self.__row2 = 0
        self.__column2 = 1

        self.__rowselection = -1

        self.pushButton_2.clicked.connect( self.insertRow1)
        self.comboBox_2.editTextChanged.connect( self.actualizar1 )
        self.comboBox_3.editTextChanged.connect( self.actualizar2 )
        self.pushButton_3.clicked.connect( self.insertRow2)
        self.pushButton.clicked.connect( self.buscarBook)
        self.listWidget_3.activated.connect(self.Cargar)
        self.lineEdit_3.textEdited.connect(self.actualizarbook)
        self.tableWidget_2.cellClicked.connect(self.seleccionar)
        self.tableWidget.cellClicked.connect(self.viewSynonyms)
        self.pushButton_4.clicked.connect(self.upsense)
        self.pushButton_9.clicked.connect(self.insertSynonyms)
        self.pushButton_8.clicked.connect(self.buscarSynonyms)
        self.pushButton_20.clicked.connect(self.uprelacion)
        self.listWidget.itemDoubleClicked.connect(self.modrelacion)
        self.pushButton_7.clicked.connect( self.cambrela)
        self.pushButton_22.clicked.connect( self.elim)



    def actualizar1(self):
        cant_row = self.tableWidget.rowCount()
        self.listWidget.clear()
        self.__allsynon = []
        if(cant_row!=-0):
            while(cant_row!=0):
               self.tableWidget.removeRow(cant_row)
               cant_row -=1
            self.tableWidget.removeRow(0)
            self.__row1 = 0
            self.__max_row1 = 0
            self.__column1 = 1
    def actualizar2(self):
        cant_row = self.tableWidget_2.rowCount()
        if(cant_row!=-0):
            while(cant_row!=0):
               self.tableWidget_2.removeRow(cant_row)
               cant_row -=1
            self.tableWidget_2.removeRow(0)
            self.__row2 = 0
            self.__max_row2 = 0
            self.__column2 = 1

    def insertRow1(self):

         str = "SELECT ss_type,synset_offset,sense_number,tag_cnt FROM [index_sense] WHERE [lemma]='"+self.comboBox_2.currentText()+"' ORDER BY [ss_type],[sense_number]"
         self.__cursor.execute(unicode(str))
         result = self.__cursor.fetchall()

         for con in result:
             self.tableWidget.insertRow(self.__max_row1)
             self.__max_row1 += 1

         for a, b, c, d in result:
            if(a==1):
                self.tableWidget.setItem(self.__row1,0,QTableWidgetItem("noun"))
                str = "SELECT [sense], [sense_es], [sense_long], [sense_long_es], [gloss], [gloss_es] FROM [data_noun] WHERE [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                data = self.__cursor.fetchall()

                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][0]))
                self.__column1 += 1
                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][1]))
                self.__column1 += 1
                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][2]))
                self.__column1 += 1
                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][3]))
                self.__column1 += 1
                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][4]))
                self.__column1 += 1
                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][5]))
            if(a==2):
                self.tableWidget.setItem(self.__row1,0,QTableWidgetItem("verb"))
                str = "SELECT [sense], [sense_es], [sense_long], [sense_long_es], [gloss], [gloss_es] FROM [data_verb] WHERE [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                data = self.__cursor.fetchall()

                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][0]))
                self.__column1 += 1
                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][1]))
                self.__column1 += 1
                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][2]))
                self.__column1 += 1
                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][3]))
                self.__column1 += 1
                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][4]))
                self.__column1 += 1
                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][5]))
            if(a==3 or a==5):
                self.tableWidget.setItem(self.__row1,0,QTableWidgetItem("adj"))
                str = "SELECT [sense], [sense_es], [sense_long], [sense_long_es], [gloss], [gloss_es] FROM [data_adj] WHERE [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                data = self.__cursor.fetchall()

                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][0]))
                self.__column1 += 1
                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][1]))
                self.__column1 += 1
                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][2]))
                self.__column1 += 1
                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][3]))
                self.__column1 += 1
                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][4]))
                self.__column1 += 1
                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][5]))
            if(a==4):
                self.tableWidget.setItem(self.__row1,0,QTableWidgetItem("verb"))
                str = "SELECT [sense], [sense_es], [sense_long], [sense_long_es], [gloss], [gloss_es] FROM [data_adv] WHERE [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                data = self.__cursor.fetchall()

                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][0]))
                self.__column1 += 1
                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][1]))
                self.__column1 += 1
                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][2]))
                self.__column1 += 1
                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][3]))
                self.__column1 += 1
                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][4]))
                self.__column1 += 1
                self.tableWidget.setItem(self.__row1,self.__column1,QTableWidgetItem(data[0][5]))

            self.__column1 = 1
            self.__row1 += 1
            self.insertSynonyms()

    def insertRow2(self):
         str = "SELECT ss_type,synset_offset,sense_number,tag_cnt FROM [index_sense] WHERE [lemma]='"+self.comboBox_3.currentText()+"' ORDER BY [ss_type],[sense_number]"
         self.__cursor.execute(unicode(str))
         result = self.__cursor.fetchall()

         for con in result:
             self.tableWidget_2.insertRow(self.__max_row2)
             self.__max_row2 += 1

         for a, b, c, d in result:
            if(a==1):
                self.tableWidget_2.setItem(self.__row2,0,QTableWidgetItem("noun"))
                str = "SELECT [sense], [sense_es], [sense_long], [sense_long_es], [gloss], [gloss_es] FROM [data_noun] WHERE [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                data = self.__cursor.fetchall()

                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][0]))
                self.__column2 += 1
                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][1]))
                self.__column2 += 1
                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][2]))
                self.__column2 += 1
                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][3]))
                self.__column2 += 1
                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][4]))
                self.__column2 += 1
                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][5]))
            if(a==2):
                self.tableWidget_2.setItem(self.__row2,0,QTableWidgetItem("verb"))
                str = "SELECT [sense], [sense_es], [sense_long], [sense_long_es], [gloss], [gloss_es] FROM [data_verb] WHERE [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                data = self.__cursor.fetchall()

                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][0]))
                self.__column2 += 1
                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][1]))
                self.__column2 += 1
                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][2]))
                self.__column2 += 1
                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][3]))
                self.__column2 += 1
                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][4]))
                self.__column2 += 1
                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][5]))
            if(a==3 or a==5):
                self.tableWidget_2.setItem(self.__row2,0,QTableWidgetItem("adj"))
                str = "SELECT [sense], [sense_es], [sense_long], [sense_long_es], [gloss], [gloss_es] FROM [data_adj] WHERE [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                data = self.__cursor.fetchall()

                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][0]))
                self.__column2 += 1
                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][1]))
                self.__column2 += 1
                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][2]))
                self.__column2 += 1
                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][3]))
                self.__column2 += 1
                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][4]))
                self.__column2 += 1
                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][5]))
            if(a==4):
                self.tableWidget_2.setItem(self.__row2,0,QTableWidgetItem("verb"))
                str = "SELECT [sense], [sense_es], [sense_long], [sense_long_es], [gloss], [gloss_es] FROM [data_adv] WHERE [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                data = self.__cursor.fetchall()

                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][0]))
                self.__column2 += 1
                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][1]))
                self.__column2 += 1
                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][2]))
                self.__column2 += 1
                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][3]))
                self.__column2 += 1
                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][4]))
                self.__column2 += 1
                self.tableWidget_2.setItem(self.__row2,self.__column2,QTableWidgetItem(data[0][5]))


            self.__column2 = 1
            self.__row2 += 1

    def buscarBook(self):
       self.listWidget_3.clear()
       self.textEdit.clear()
       if(len(self.lineEdit_3.text()) != 0):
        con = 1
        while(open("./data/book/"+str(con)+".txt")):
         #print con
         bookr = open("./data/book/"+str(con)+".txt").read()

         #print book[book.find(self.lineEdit_3.text()):book.find(self.lineEdit_3.text())+len(self.lineEdit_3.text())]
         nom_book = bookr[bookr.find("["):bookr.find("]")+1]
         bookr = bookr[bookr.find("]")+1:bookr.__len__()]
         book = bookr.lower()

         palabra = self.lineEdit_3.text().toLower()
         while(book.find(" "+palabra+" ")!= -1 ):
          #if():
           posword = book.find(" "+palabra+" ")

           ini = book[0:book.find(" "+palabra+" ")].rfind("\n\n")
           if(ini == -1):
               ini=0

           fin = book[book.find(" "+palabra+" "):book.__len__()].find("\n\n") #+1

           self.__bbook.append(bookr[ini:posword+fin])
           #print book[ini:book.find(" "+palabra+" ")+fin]

           self.listWidget_3.addItem(nom_book +" "+ str(book[ini:book.find(" "+palabra+" ")+fin].__len__()))
           book = book[book.find(" "+palabra+" ")+fin:book.__len__()]
           bookr = bookr[posword+fin:bookr.__len__()]
         con += 1

    def Cargar(self):
          self.textEdit.setText(self.__bbook[self.listWidget_3.currentRow()].replace("\n\n",""))
          pos = self.textEdit.find(" "+self.lineEdit_3.text()+" ")
          self.pintar(pos,pos+len(self.lineEdit_3.text()))

    def actualizarbook(self):
          self.listWidget_3.clear()
          self.textEdit.clear()
          self.__bbook = []
    def seleccionar(self):
        self.__filasel = []
        self.__row = self.tableWidget_2.currentRow()

        self.__filasel.append(self.tableWidget_2.takeItem(self.__row,0))
        self.__filasel.append(self.tableWidget_2.takeItem(self.__row,1))
        self.__filasel.append(self.tableWidget_2.takeItem(self.__row,2))
        self.__filasel.append(self.tableWidget_2.takeItem(self.__row,3))
        self.__filasel.append(self.tableWidget_2.takeItem(self.__row,4))
        self.__filasel.append(self.tableWidget_2.takeItem(self.__row,5))
        self.__filasel.append(self.tableWidget_2.takeItem(self.__row,6))

        self.actualizar2()
        self.insertRow2()
        self.insertSynonyms2()

    def upsense(self):
       if(self.__filasel.__len__() != 0):
        self.tableWidget.insertRow(self.__max_row1)

        self.tableWidget.setItem(self.__max_row1,0,QTableWidgetItem(self.__filasel[0]))
        self.tableWidget.setItem(self.__max_row1,1,QTableWidgetItem(self.__filasel[1]))
        self.tableWidget.setItem(self.__max_row1,2,QTableWidgetItem(self.__filasel[2]))
        self.tableWidget.setItem(self.__max_row1,3,QTableWidgetItem(self.__filasel[3]))
        self.tableWidget.setItem(self.__max_row1,4,QTableWidgetItem(self.__filasel[4]))
        self.tableWidget.setItem(self.__max_row1,5,QTableWidgetItem(self.__filasel[5]))
        self.tableWidget.setItem(self.__max_row1,5,QTableWidgetItem(self.__filasel[6]))
        self.__max_row1 += 1

        self.__filasel = []
        print self.__allsynondown[self.__row]
        select = self.__allsynondown[self.__row]
        self.__allsynon.append(select)
        print self.__allsynon[7]

    def insertSynonyms(self):

            self.listWidget.clear()



            str = "SELECT [synset_offset] FROM [index_sense] WHERE [lemma]='"+self.comboBox_2.currentText()+"'"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()

            if  result:
             for w in result:
                 str = "SELECT [word] FROM [data_noun_word_lex_id] WHERE [synset_offset]='"+w[0]+"'"
                 self.__cursor.execute(unicode(str))
                 data = self.__cursor.fetchall()
                 if  data:
                  for r in data:
                      self.__filword.append(r)
                  self.__allsynon.append(self.__filword)
                  self.__filword = []

                 str = "SELECT [word] FROM [data_verb_word_lex_id] WHERE [synset_offset]='"+w[0]+"'"
                 self.__cursor.execute(unicode(str))
                 data = self.__cursor.fetchall()
                 if  data:
                  for r in data:
                      self.__filword.append(r)
                  self.__allsynon.append(self.__filword)
                  self.__filword = []

                 str = "SELECT [word] FROM [data_adj_word_lex_id] WHERE [synset_offset]='"+w[0]+"'"
                 self.__cursor.execute(unicode(str))
                 data = self.__cursor.fetchall()
                 if  data:
                  for r in data:
                      self.__filword.append(r)
                  self.__allsynon.append(self.__filword)
                  self.__filword = []

                 str = "SELECT [word] FROM [data_adv_word_lex_id] WHERE [synset_offset]='"+w[0]+"'"
                 self.__cursor.execute(unicode(str))
                 data = self.__cursor.fetchall()
                 if  data:
                  for r in data:
                      self.__filword.append(r)
                  self.__allsynon.append(self.__filword)
                  self.__filword = []

    def viewSynonyms(self):

        self.listWidget.clear()
        row = self.tableWidget.currentRow()
        print self.__allsynon[self.__allsynon.__len__()-1]
        print row
        print  self.__allsynon[7]
        for w in self.__allsynon[row]:
         self.listWidget.addItem(w[0])

    def buscarSynonyms(self):
            self.listWidget_2.clear()
            str = "SELECT DISTINCT([data_noun_word_lex_id].[word]) FROM ([index_sense] INNER JOIN [data_noun_word_lex_id] USING([synset_offset])) WHERE [index_sense].[lemma]='"+self.lineEdit_2.text()+"'"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()

            if  result:
             for w in result:
               if(self.lineEdit_2.text().toLower()!=lower(w[0])):
                self.listWidget_2.addItem(w[0])
            str = "SELECT DISTINCT([data_verb_word_lex_id].[word]) FROM ([index_sense] INNER JOIN [data_verb_word_lex_id] USING([synset_offset])) WHERE [index_sense].[lemma]='"+self.lineEdit_2.text()+"'"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()

            if result:
             for w in result:
                 if(self.lineEdit_2.text().toLower()!=lower(w[0])):
                    self.listWidget_2.addItem(w[0])
            str = "SELECT DISTINCT([data_adj_word_lex_id].[word]) FROM ([index_sense] INNER JOIN [data_adj_word_lex_id] USING([synset_offset])) WHERE [index_sense].[lemma]='"+self.lineEdit_2.text()+"'"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()

            if result:
                for w in result:
                  if(self.lineEdit_2.text().toLower()!=lower(w[0])):
                    self.listWidget.addItem(str(w[0]))
            str = "SELECT DISTINCT([data_adv_word_lex_id].[word]) FROM ([index_sense] INNER JOIN [data_adv_word_lex_id] USING([synset_offset])) WHERE [index_sense].[lemma]='"+self.lineEdit_2.text()+"'"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:
                for w in result:
                    if(self.lineEdit_2.text().toLower() != lower(w[0])):
                        self.listWidget.addItem(w[0])

    def uprelacion(self):

        select = self.listWidget_2.currentRow()

        relaword = self.listWidget_2.takeItem(select)
        self.listWidget_2.insertItem(select,relaword)

        self.listWidget.addItem(str(relaword.text()))

    def modrelacion(self):
        self.pushButton_7.setText("Modificar")
        self.__rowselection = self.listWidget.currentRow()
        #self.listWidget.

    def cambrela(self):

        if(self.__rowselection != -1):
            self.listWidget.takeItem(self.__rowselection)
            self.listWidget.insertItem(self.__rowselection,self.lineEdit.text())
            self.__rowselection = -1
            self.pushButton_7.setText("Insertar")
        else:
            self.listWidget.addItem(self.lineEdit.text())

    def elim(self):
        self.listWidget.takeItem(self.__rowselection)
        self.__rowselection = -1
        self.pushButton_7.setText("Insertar")

    def pintar( self, pi,pf):
        format = QTextCharFormat()
        format.setBackground(QBrush(Qt.darkRed))
        cursor = self.textEdit.textCursor()
        cursor.setPosition(pi)
        cursor.setPosition(pf, QTextCursor.KeepAnchor)
        cursor.mergeCharFormat(format)
        cursor.clearSelection()

    def insertSynonyms2(self):

            str = "SELECT [synset_offset] FROM [index_sense] WHERE [lemma]='"+self.comboBox_3.currentText()+"'"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()

            if  result:
             for w in result:
                 str = "SELECT [word] FROM [data_noun_word_lex_id] WHERE [synset_offset]='"+w[0]+"'"
                 self.__cursor.execute(unicode(str))
                 data = self.__cursor.fetchall()
                 if  data:
                  for r in data:
                      self.__filword.append(r)
                  self.__allsynondown.append(self.__filword)
                  self.__filword = []

                 str = "SELECT [word] FROM [data_verb_word_lex_id] WHERE [synset_offset]='"+w[0]+"'"
                 self.__cursor.execute(unicode(str))
                 data = self.__cursor.fetchall()
                 if  data:
                  for r in data:
                      self.__filword.append(r)
                  self.__allsynondown.append(self.__filword)
                  self.__filword = []

                 str = "SELECT [word] FROM [data_adj_word_lex_id] WHERE [synset_offset]='"+w[0]+"'"
                 self.__cursor.execute(unicode(str))
                 data = self.__cursor.fetchall()
                 if  data:
                  for r in data:
                      self.__filword.append(r)
                  self.__allsynondown.append(self.__filword)
                  self.__filword = []

                 str = "SELECT [word] FROM [data_adv_word_lex_id] WHERE [synset_offset]='"+w[0]+"'"
                 self.__cursor.execute(unicode(str))
                 data = self.__cursor.fetchall()
                 if  data:
                  for r in data:
                      self.__filword.append(r)
                  self.__allsynondown.append(self.__filword)
                  self.__filword = []






