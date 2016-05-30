#!/usr/bin/python
# -*- coding: utf-8 -*-

# main core file
from string import lower
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from QtNLP_Wordnet_UI import Ui_MainWindow
import sqlite3
from QtNLP_Wordnet_Editor import WordnetEditor

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
        self.__column = 3
        self.__difAtrib = ["[data_noun_ptr].[pointer_symbol]='!'","[data_noun_ptr].[pointer_symbol] = '=' OR [data_noun_ptr].[pointer_symbol] = \'\\'","[data_noun_ptr].[pointer_symbol] = '+' OR [data_noun_ptr].[pointer_symbol] = '^'","[data_noun_ptr].[pointer_symbol] = '='","[data_noun_ptr].[pointer_symbol] = '&'","[data_noun_ptr].[pointer_symbol] like '%c' OR [data_noun_ptr].[pointer_symbol] like '%r' OR [data_noun_ptr].[pointer_symbol] = '%u'","[data_noun_ptr].[pointer_symbol] like '%c' OR [data_noun_ptr].[pointer_symbol] like '%r' OR [data_noun_ptr].[pointer_symbol] = '%u'","[data_noun_ptr].[pointer_symbol] = '>'","[data_noun_ptr].[pointer_symbol] = '*'","[data_noun_ptr].[pointer_symbol] like '@%'","[data_noun_ptr].[pointer_symbol] like '~%'","[data_noun_ptr].[pointer_symbol] like '#%'","[data_noun_ptr].[pointer_symbol] = '%m' OR [data_noun_ptr].[pointer_symbol] = '%s' OR [data_noun_ptr].[pointer_symbol] = '%p'"]
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.pushButton_15.clicked.connect( self.__editWord )
        self.pushButton.clicked.connect( self.insertRow)
        self.comboBox.editTextChanged.connect( self.actualizar )

        self.pushButton_2.clicked.connect( self.insertSynonyms)
        self.pushButton_3.clicked.connect( self.insertAntonyms)
        self.pushButton_6.clicked.connect( self.insertAttributes)
        self.pushButton_11.clicked.connect( self.insertKindof)
        self.pushButton_12.clicked.connect( self.insertKinds)
        self.pushButton_13.clicked.connect( self.insertPartof)
        self.pushButton_14.clicked.connect( self.insertParts)
        self.pushButton_8.clicked.connect( self.insertDomain)
        self.pushButton_4.clicked.connect( self.insertDerivatives)
        self.pushButton_5.clicked.connect( self.insertRelatesto)
        self.pushButton_7.clicked.connect( self.insertSimilar)
        self.pushButton_9.clicked.connect( self.insertCauses)
        self.pushButton_10.clicked.connect( self.insertEntails)

        self.listWidget.doubleClicked.connect(self.pasar)


    # SLOTS !!!
    def __editWord(self):
        e = WordnetEditor(self)
        e.show()
    def pasar(self):
        select = self.listWidget.currentRow()
        relaword = self.listWidget.takeItem(select)
        self.listWidget.insertItem(select,relaword)

        self.comboBox.setEditText(str(relaword.text()))
        self.insertRow()

    def chekeando(self):
        if(self.checkAtributo(self.__difAtrib[0])!=True):
          self.pushButton_3.setEnabled(False)
        else:
          self.pushButton_3.setEnabled(True)
        if(self.checkAtributo(self.__difAtrib[1])!=True):
          self.pushButton_4.setEnabled(False)
        else:
          self.pushButton_4.setEnabled(True)
        if(self.checkAtributo(self.__difAtrib[2])!=True):
          self.pushButton_5.setEnabled(False)
        else:
          self.pushButton_5.setEnabled(True)
        if(self.checkAtributo(self.__difAtrib[3])!=True):
          self.pushButton_6.setEnabled(False)
        else:
          self.pushButton_6.setEnabled(True)
        if(self.checkAtributo(self.__difAtrib[4])!=True):
          self.pushButton_7.setEnabled(False)
        else:
          self.pushButton_7.setEnabled(True)
        if(self.checkAtributo(self.__difAtrib[5])!=True):
          self.pushButton_8.setEnabled(False)
        else:
          self.pushButton_8.setEnabled(True)
        if(self.checkAtributo(self.__difAtrib[6])!=True):
          self.pushButton_9.setEnabled(False)
        else:
          self.pushButton_9.setEnabled(True)
        if(self.checkAtributo(self.__difAtrib[7])!=True):
          self.pushButton_10.setEnabled(False)
        else:
          self.pushButton_10.setEnabled(True)
        if(self.checkAtributo(self.__difAtrib[8])!=True):
          self.pushButton_11.setEnabled(False)
        else:
          self.pushButton_11.setEnabled(True)
        if(self.checkAtributo(self.__difAtrib[9])!=True):
          self.pushButton_12.setEnabled(False)
        else:
          self.pushButton_12.setEnabled(True)
        if(self.checkAtributo(self.__difAtrib[10])!=True):
          self.pushButton_13.setEnabled(False)
        else:
          self.pushButton_13.setEnabled(True)
        if(self.checkAtributo(self.__difAtrib[11])!=True):
          self.pushButton_14.setEnabled(False)
        else:
          self.pushButton_14.setEnabled(True)


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
            self.__column = 3

    def insertAtributo(self,cadena):
            self.listWidget.clear()

            str = "SELECT DISTINCT([data_noun_ptr].[synset_offset_p]) FROM [index_sense]  INNER JOIN [data_noun_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.comboBox.currentText()+"'AND ("+cadena+")"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:
                for w in result:
                  str = "SELECT DISTINCT(word) FROM [data_noun_word_lex_id] WHERE [synset_offset]='"+w[0]+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        self.listWidget.addItem(a[0])

            str = "SELECT DISTINCT([data_verb_ptr].[synset_offset_p]) FROM [index_sense]  INNER JOIN [data_verb_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.comboBox.currentText()+"'AND ("+cadena.replace("noun","verb")+")"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:
                for w in result:
                  str = "SELECT DISTINCT(word) FROM [data_verb_word_lex_id] WHERE [synset_offset]='"+w[0]+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        self.listWidget.addItem(a[0])

            str = "SELECT DISTINCT([data_adj_ptr].[synset_offset_p]) FROM [index_sense]  INNER JOIN [data_adj_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.comboBox.currentText()+"'AND ("+cadena.replace("noun","adj")+")"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:
                for w in result:
                  str = "SELECT DISTINCT(word) FROM [data_adj_word_lex_id] WHERE [synset_offset]='"+w[0]+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        self.listWidget.addItem(a[0])

            str = "SELECT DISTINCT([data_adv_ptr].[synset_offset_p]) FROM [index_sense]  INNER JOIN [data_adv_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='" + self.comboBox.currentText() + "'AND ("+cadena.replace("noun","adv")+")"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:
                for w in result:
                  str = "SELECT DISTINCT(word) FROM [data_adv_word_lex_id] WHERE [synset_offset]='"+w[0]+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        self.listWidget.addItem(a[0])

    def checkAtributo(self,cadena):

            str = "SELECT DISTINCT([data_noun_ptr].[synset_offset_p]) FROM [index_sense]  INNER JOIN [data_noun_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.comboBox.currentText()+"'AND ("+cadena+")"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:
                return True

            str = "SELECT DISTINCT([data_verb_ptr].[synset_offset_p]) FROM [index_sense]  INNER JOIN [data_verb_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.comboBox.currentText()+"'AND ("+cadena.replace("noun","verb")+")"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:
                return True

            str = "SELECT DISTINCT([data_adj_ptr].[synset_offset_p]) FROM [index_sense]  INNER JOIN [data_adj_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.comboBox.currentText()+"'AND ("+cadena.replace("noun","adj")+")"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:
                return True

            str = "SELECT DISTINCT([data_adv_ptr].[synset_offset_p]) FROM [index_sense]  INNER JOIN [data_adv_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='" + self.comboBox.currentText() + "'AND ("+cadena.replace("noun","adv")+")"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:
                return True

    def insertRow(self):
    #@pyqtSignature('')
    #def on_pushButton_clicked(self):

        str = "SELECT ss_type,synset_offset,sense_number,tag_cnt FROM [index_sense] WHERE [lemma]='"+self.comboBox.currentText()+"' ORDER BY [ss_type],[tag_cnt] DESC, [sense_number]"
        self.__cursor.execute(unicode(str))
        result = self.__cursor.fetchall()

        """para poner los botones disables"""
        #self.chekeando()

        for con in result:
             self.tableWidget.insertRow(self.__max_row)
             self.__max_row += 1

        for a, b, c, d in result:
            self.tableWidget.setItem(self.__row,0,QTableWidgetItem(self.comboBox.currentText()))

            if(a==1):
                self.tableWidget.setItem(self.__row,2,QTableWidgetItem("noun"))
                str = "SELECT DISTINCT([word_traslated]) FROM [data_noun_word_lex_id] WHERE [word]='"+self.comboBox.currentText()+"'AND [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                traslated = self.__cursor.fetchall()
                if(traslated):
                    self.tableWidget.setItem(self.__row,1,QTableWidgetItem(traslated[0][0]))
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
                self.tableWidget.setItem(self.__row,2,QTableWidgetItem("verb"))
                str = "SELECT DISTINCT([word_traslated]) FROM [data_verb_word_lex_id] WHERE [word]='"+self.comboBox.currentText()+"'AND [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                traslated = self.__cursor.fetchall()
                if(traslated):
                    self.tableWidget.setItem(self.__row,1,QTableWidgetItem(traslated[0][0]))
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
                self.tableWidget.setItem(self.__row,2,QTableWidgetItem("verb"))
                str = "SELECT DISTINCT([word_traslated]) FROM [data_adj_word_lex_id] WHERE [word]='"+self.comboBox.currentText()+"'AND [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                traslated = self.__cursor.fetchall()
                if(traslated):
                    self.tableWidget.setItem(self.__row,1,QTableWidgetItem(traslated[0][0]))
                self.tableWidget.setItem(self.__row,2,QTableWidgetItem("adj"))
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
                self.tableWidget.setItem(self.__row,2,QTableWidgetItem("verb"))
                str = "SELECT DISTINCT([word_traslated]) FROM [data_adv_word_lex_id] WHERE [word]='"+self.comboBox.currentText()+"'AND [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                traslated = self.__cursor.fetchall()
                if(traslated):
                    self.tableWidget.setItem(self.__row,1,QTableWidgetItem(traslated[0][0]))
                self.tableWidget.setItem(self.__row,2,QTableWidgetItem("adv"))
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

            self.__column = 3
            self.__row += 1
        self.insertExec()
        self.insertSynonyms()

    def insertExec(self):
    #@pyqtSignature('')
    #def on_pushButton_clicked(self):
        #argl = []
        str = "SELECT base_form FROM [exceptions] WHERE [word_inflected]='"+self.comboBox.currentText()+"'"
        self.__cursor.execute(unicode(str))
        resultword = self.__cursor.fetchall()

        if(resultword):

             str = "SELECT base_form FROM [noun_exc] WHERE [word_inflected]='"+self.comboBox.currentText()+"'"
             self.__cursor.execute(unicode(str))
             base = self.__cursor.fetchall()

             if(base):
                 str = "SELECT ss_type,synset_offset,sense_number,tag_cnt FROM [index_sense] WHERE [lemma]='"+base[0][0]+"' and ss_type = 1 ORDER BY [ss_type],[tag_cnt] DESC, [sense_number]"
                 self.__cursor.execute(unicode(str))
                 result = self.__cursor.fetchall()
                 if(result):
                  for con in result:
                    self.tableWidget.insertRow(self.__max_row)
                    self.__max_row += 1

                  for a, b, c, d in result:
                    self.tableWidget.setItem(self.__row,2,QTableWidgetItem("noun"))
                    self.tableWidget.setItem(self.__row,0,QTableWidgetItem(base[0][0]))
                    str = "SELECT DISTINCT([word_traslated]) FROM [data_noun_word_lex_id] WHERE [word]='"+base[0][0]+"'AND [synset_offset]='"+b+"'"
                    self.__cursor.execute(unicode(str))
                    traslated = self.__cursor.fetchall()
                    if(traslated):
                        self.tableWidget.setItem(self.__row,1,QTableWidgetItem(traslated[0][0]))
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
                    self.__column = 3
                    self.__row += 1

             str = "SELECT base_form FROM [verb_exc] WHERE [word_inflected]='"+self.comboBox.currentText()+"'"
             self.__cursor.execute(unicode(str))
             base = self.__cursor.fetchall()

             if(base):
                 str = "SELECT ss_type,synset_offset,sense_number,tag_cnt FROM [index_sense] WHERE [lemma]='"+base[0][0]+"' and ss_type = 2 ORDER BY [ss_type],[tag_cnt] DESC, [sense_number]"
                 self.__cursor.execute(unicode(str))
                 result = self.__cursor.fetchall()
                 if(result):
                  for con in result:
                    self.tableWidget.insertRow(self.__max_row)
                    self.__max_row += 1

                  for a, b, c, d in result:
                    self.tableWidget.setItem(self.__row,2,QTableWidgetItem("verb"))
                    self.tableWidget.setItem(self.__row,0,QTableWidgetItem(base[0][0]))
                    str = "SELECT DISTINCT([word_traslated]) FROM [data_verb_word_lex_id] WHERE [word]='"+base[0][0]+"'AND [synset_offset]='"+b+"'"
                    self.__cursor.execute(unicode(str))
                    traslated = self.__cursor.fetchall()
                    if(traslated):
                        self.tableWidget.setItem(self.__row,1,QTableWidgetItem(traslated[0][0]))
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
                    self.__column = 3
                    self.__row += 1

             str = "SELECT base_form FROM [adj_exc] WHERE [word_inflected]='"+self.comboBox.currentText()+"'"
             self.__cursor.execute(unicode(str))
             base = self.__cursor.fetchall()

             if(base):
                 #word = base[0]
                 str = "SELECT ss_type,synset_offset,sense_number,tag_cnt FROM [index_sense] WHERE [lemma]='"+base[0][0]+"' and (ss_type = 3 or ss_type = 5) ORDER BY [ss_type],[tag_cnt] DESC, [sense_number]"
                 self.__cursor.execute(unicode(str))
                 result = self.__cursor.fetchall()
                 if(result):
                  for con in result:
                    self.tableWidget.insertRow(self.__max_row)
                    self.__max_row += 1

                  for a, b, c, d in result:
                    self.tableWidget.setItem(self.__row,2,QTableWidgetItem("adj"))
                    self.tableWidget.setItem(self.__row,0,QTableWidgetItem(base[0][0]))
                    str = "SELECT DISTINCT([word_traslated]) FROM [data_adj_word_lex_id] WHERE [word]='"+base[0][0]+"'AND [synset_offset]='"+b+"'"
                    self.__cursor.execute(unicode(str))
                    traslated = self.__cursor.fetchall()
                    if(traslated):
                        self.tableWidget.setItem(self.__row,1,QTableWidgetItem(traslated[0][0]))
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
                    self.__column = 3
                    self.__row += 1

             str = "SELECT base_form FROM [adv_exc] WHERE [word_inflected]='"+self.comboBox.currentText()+"'"
             self.__cursor.execute(unicode(str))
             base = self.__cursor.fetchall()

             if(base):
                 str = "SELECT ss_type,synset_offset,sense_number,tag_cnt FROM [index_sense] WHERE [lemma]='"+base[0][0]+"' and ss_type = 4 ORDER BY [ss_type],[tag_cnt] DESC, [sense_number]"
                 self.__cursor.execute(unicode(str))
                 result = self.__cursor.fetchall()
                 if(result):
                  for con in result:
                    self.tableWidget.insertRow(self.__max_row)
                    self.__max_row += 1

                  for a, b, c, d in result:
                    self.tableWidget.setItem(self.__row,2,QTableWidgetItem("adv"))
                    self.tableWidget.setItem(self.__row,0,QTableWidgetItem(base[0][0]))
                    str = "SELECT DISTINCT([word_traslated]) FROM [data_adv_word_lex_id] WHERE [word]='"+base[0][0]+"'AND [synset_offset]='"+b+"'"
                    self.__cursor.execute(unicode(str))
                    traslated = self.__cursor.fetchall()
                    if(traslated):
                        self.tableWidget.setItem(self.__row,1,QTableWidgetItem(traslated[0][0]))
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
                    self.__column = 3
                    self.__row += 1

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
                    self.listWidget.addItem(w[0])

            str = "SELECT DISTINCT([data_adv_word_lex_id].[word]) FROM ([index_sense] INNER JOIN [data_adv_word_lex_id] USING([synset_offset])) WHERE [index_sense].[lemma]='"+self.comboBox.currentText()+"'"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:
                for w in result:
                    if(self.comboBox.currentText().toLower() != lower(w[0])):
                        self.listWidget.addItem(w[0])

            str = "SELECT base_form FROM [exceptions] WHERE [word_inflected]='"+self.comboBox.currentText()+"'"
            self.__cursor.execute(unicode(str))
            resultword = self.__cursor.fetchall()

            if(resultword):
                str = "SELECT base_form FROM [noun_exc] WHERE [word_inflected]='"+self.comboBox.currentText()+"'"
                self.__cursor.execute(unicode(str))
                base = self.__cursor.fetchall()

                if(base):
                 str = "SELECT DISTINCT([data_noun_word_lex_id].[word]) FROM ([index_sense] INNER JOIN [data_noun_word_lex_id] USING([synset_offset])) WHERE [index_sense].[lemma]='"+base[0][0]+"'"
                 self.__cursor.execute(unicode(str))
                 result = self.__cursor.fetchall()
                 if(result):
                     for w in result:
                         if(self.comboBox.currentText().toLower() != lower(w[0])):
                             self.listWidget.addItem(w[0])

                str = "SELECT base_form FROM [verb_exc] WHERE [word_inflected]='"+self.comboBox.currentText()+"'"
                self.__cursor.execute(unicode(str))
                base = self.__cursor.fetchall()

                if(base):
                 str = "SELECT DISTINCT([data_verb_word_lex_id].[word]) FROM ([index_sense] INNER JOIN [data_verb_word_lex_id] USING([synset_offset])) WHERE [index_sense].[lemma]='"+base[0][0]+"'"
                 self.__cursor.execute(unicode(str))
                 result = self.__cursor.fetchall()
                 if(result):
                     for w in result:
                         if(self.comboBox.currentText().toLower() != lower(w[0])):
                             self.listWidget.addItem(w[0])

                str = "SELECT base_form FROM [adj_exc] WHERE [word_inflected]='"+self.comboBox.currentText()+"'"
                self.__cursor.execute(unicode(str))
                base = self.__cursor.fetchall()

                if(base):
                 str = "SELECT DISTINCT([data_adj_word_lex_id].[word]) FROM ([index_sense] INNER JOIN [data_adj_word_lex_id] USING([synset_offset])) WHERE [index_sense].[lemma]='"+base[0][0]+"'"
                 self.__cursor.execute(unicode(str))
                 result = self.__cursor.fetchall()
                 if(result):
                     for w in result:
                         if(self.comboBox.currentText().toLower() != lower(w[0])):
                             self.listWidget.addItem(w[0])

                str = "SELECT base_form FROM [adv_exc] WHERE [word_inflected]='"+self.comboBox.currentText()+"'"
                self.__cursor.execute(unicode(str))
                base = self.__cursor.fetchall()

                if(base):
                 str = "SELECT DISTINCT([data_adv_word_lex_id].[word]) FROM ([index_sense] INNER JOIN [data_adv_word_lex_id] USING([synset_offset])) WHERE [index_sense].[lemma]='"+base[0][0]+"'"
                 self.__cursor.execute(unicode(str))
                 result = self.__cursor.fetchall()
                 if(result):
                     for w in result:
                         if(self.comboBox.currentText().toLower() != lower(w[0])):
                             self.listWidget.addItem(w[0])

    def insertAntonyms(self):
        self.insertAtributo(self.__difAtrib[0])

    def insertAttributes(self):
        self.insertAtributo(self.__difAtrib[3])

    def insertKindof(self):
        self.insertAtributo(self.__difAtrib[9])

    def insertKinds(self):
        self.insertAtributo(self.__difAtrib[10])

    def insertPartof(self):
        self.insertAtributo(self.__difAtrib[11])

    def insertParts(self):
        self.insertAtributo(self.__difAtrib[12])

    def insertDomain(self):
        self.insertAtributo(self.__difAtrib[6])

    def insertDerivatives(self):
        self.insertAtributo(self.__difAtrib[1])

    def insertRelatesto(self):
        self.insertAtributo(self.__difAtrib[2])

    def insertSimilar(self):
        self.insertAtributo(self.__difAtrib[4])

    def insertCauses(self):
        self.insertAtributo(self.__difAtrib[7])

    def insertEntails(self):
        self.insertAtributo(self.__difAtrib[8])
