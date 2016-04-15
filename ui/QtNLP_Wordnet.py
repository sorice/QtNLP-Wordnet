#!/usr/bin/python
# -*- coding: utf-8 -*-

# main core file
from string import lower

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from QtNLP_Wordnet_UI import Ui_MainWindow
import sqlite3


class Wordnet( QMainWindow, Ui_MainWindow):

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

        self.pushButton.clicked.connect( self.insertRow )
        self.comboBox.editTextChanged.connect( self.actualizar )

        self.pushButton_2.clicked.connect( self.insertSynonyms)
        self.pushButton_3.clicked.connect( self.insertAntonyms)

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
            if not result:
                print
            else:
             for w in result:
               if(self.comboBox.currentText().toLower()!=lower(w[0])):
                self.listWidget.addItem(w[0])
            str = "SELECT DISTINCT([data_verb_word_lex_id].[word]) FROM ([index_sense] INNER JOIN [data_verb_word_lex_id] USING([synset_offset])) WHERE [index_sense].[lemma]='"+self.comboBox.currentText()+"'"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if not result:
                 print
            else:
             for w in result:
                 if(self.comboBox.currentText().toLower()!=lower(w[0])):
                    self.listWidget.addItem(w[0])
            str = "SELECT DISTINCT([data_adj_word_lex_id].[word]) FROM ([index_sense] INNER JOIN [data_adj_word_lex_id] USING([synset_offset])) WHERE [index_sense].[lemma]='"+self.comboBox.currentText()+"'"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if not result:
                 print
            else:
                for w in result:
                  if(self.comboBox.currentText().toLower()!=lower(w[0])):
                    self.listWidget.addItem(str(w[0]))
            str = "SELECT DISTINCT([data_adv_word_lex_id].[word]) FROM ([index_sense] INNER JOIN [data_adv_word_lex_id] USING([synset_offset])) WHERE [index_sense].[lemma]='"+self.comboBox.currentText()+"'"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:
                for w in result:
                    if(self.comboBox.currentText().toLower()!=lower(w[0])):
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

            str = "SELECT DISTINCT([data_adv_ptr].[synset_offset_p]) FROM [index_sense]  INNER JOIN [data_adv_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.comboBox.currentText()+"'AND [data_adv_ptr].[pointer_symbol]='!'"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:
                for w in result:
                  str = "SELECT DISTINCT(word) FROM [data_adv_word_lex_id] WHERE [synset_offset]='"+w[0]+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  for a in data:
                        self.listWidget.addItem(a[0])
