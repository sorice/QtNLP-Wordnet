#!/usr/bin/python
# -*- coding: utf-8 -*-

# main core file
from string import lower
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from QtNLP_Wordnet_Editor_UI import Ui_MainWindow
import sqlite3
from __builtin__ import unicode


class WordnetEditor( QMainWindow, Ui_MainWindow):

    def __init__( self, parent = None ):
        # init the parent
        super( WordnetEditor, self ).__init__( parent )
        # setup the UI
        self.setupUi( self )

        self.__connect = sqlite3.connect("./data/wordnet.db3")
        self.__cursor = self.__connect.cursor()
        self.lineEdit_4.setEnabled(False)

        str = "SELECT num FROM [max_synset_offset]"
        self.__cursor.execute(unicode(str))
        self.__nummaxdb = self.__cursor.fetchall()
        self.__nummaxdb = int(self.__nummaxdb[0][0])
        self.__bbook = []
        self.__filasel = []
        self.__filword = []
        self.__allsynon = []
        self.__allsynondown = []
        self.__allsynset_offset = []
        self.__allsynset_offsetdown = []
        self.__tablesynset = []
        self.__tablesynsetdown = []
        self.__arrayid = []
        self.__arrayfind = []

        self.__max_row1 = 0
        self.__row1 = 0
        self.__column1 = 2
        self.__row = 0
        self.__search = False
        self.__columnselected = 0
        self.__filter = 0

        self.__max_row2 = 0
        self.__row2 = 0
        self.__column2 = 2

        self.__arrepos = -1
        self.__arrepos2 = -1

        self.__rowselection = -1
        """cambiar \ por el $ en al bd"""
        self.__difAtrib = ["[data_noun_ptr].[pointer_symbol]='!'","[data_noun_ptr].[pointer_symbol] = '$'","[data_noun_ptr].[pointer_symbol] = '+' OR [data_noun_ptr].[pointer_symbol] = '^'","[data_noun_ptr].[pointer_symbol] = '='","[data_noun_ptr].[pointer_symbol] = '&'","[data_noun_ptr].[pointer_symbol] like '%c' OR [data_noun_ptr].[pointer_symbol] like '%r' OR [data_noun_ptr].[pointer_symbol] = '%u'","[data_noun_ptr].[pointer_symbol] = '>'","[data_noun_ptr].[pointer_symbol] = '*'","[data_noun_ptr].[pointer_symbol] like '@%'","[data_noun_ptr].[pointer_symbol] like '~%'","[data_noun_ptr].[pointer_symbol] like '#%'","[data_noun_ptr].[pointer_symbol] = '%m' OR [data_noun_ptr].[pointer_symbol] = '%s' OR [data_noun_ptr].[pointer_symbol] = '%p'"]

        self.__antonyms = []
        self.__derivatives = []
        self.__relatesto = []
        self.__attributes = []
        self.__similar = []
        self.__domain = []
        self.__causes = []
        self.__entails = []
        self.__kindof = []
        self.__kinds = []
        self.__partof = []
        self.__parts = []

        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_2.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.pushButton_40.clicked.connect(self.insertmodifinDB)
        self.tableWidget.cellChanged.connect(self.modiftable)
        self.lineEdit_4.textChanged.connect(self.busqueda)
        self.pushButton_6.clicked.connect(self.elimatrib)
        self.listWidget_4.activated.connect(self.modifexc)
        self.pushButton_42.clicked.connect( self.insertexc)
        self.pushButton_2.clicked.connect( self.insertRow1)
        self.comboBox_2.editTextChanged.connect( self.actualizar1 )
        self.comboBox_3.editTextChanged.connect( self.actualizar2 )
        self.pushButton_3.clicked.connect( self.insertRow2)
        self.pushButton.clicked.connect( self.buscarBook)
        self.listWidget_3.activated.connect(self.Cargar)
        self.lineEdit_3.textEdited.connect(self.actualizarbook)
        self.pushButton_5.clicked.connect(self.newfill)

        self.tableWidget_2.cellClicked.connect(self.seleccionar)

        self.tableWidget.cellClicked.connect(self.viewSynonyms)
        self.pushButton_4.clicked.connect(self.upsense)
        self.pushButton_9.setEnabled(False)
        self.pushButton_8.clicked.connect(self.chekeando)
        self.pushButton_25.clicked.connect(self.buscarSynonyms)
        self.pushButton_20.clicked.connect(self.uprelacion)
        self.listWidget.itemDoubleClicked.connect(self.modrelacion)
       # self.pushButton_7.clicked.connect( self.cambrela)
        self.pushButton_22.clicked.connect( self.elim)

        self.pushButton_10.clicked.connect( self.insertAntonyms)
        self.pushButton_11.clicked.connect( self.insertDerivatives)
        self.pushButton_12.clicked.connect( self.insertRelatesto)
        self.pushButton_13.clicked.connect( self.insertAttributes)
        self.pushButton_14.clicked.connect( self.insertSimilar)
        self.pushButton_15.clicked.connect( self.insertDomain)
        self.pushButton_16.clicked.connect( self.insertCauses)
        self.pushButton_17.clicked.connect( self.insertEntails)
        self.pushButton_18.clicked.connect( self.insertKindof)
        self.pushButton_19.clicked.connect( self.insertKinds)
        self.pushButton_23.clicked.connect( self.insertPartof)
        self.pushButton_24.clicked.connect( self.insertParts)

        self.pushButton_27.clicked.connect( self.insertAntonyms2)
        self.pushButton_29.clicked.connect( self.insertDerivatives2)
        self.pushButton_31.clicked.connect( self.insertRelatesto2)
        self.pushButton_33.clicked.connect( self.insertAttributes2)
        self.pushButton_35.clicked.connect( self.insertSimilar2)
        self.pushButton_37.clicked.connect( self.insertDomain2)
        self.pushButton_26.clicked.connect( self.insertCauses2)
        self.pushButton_28.clicked.connect( self.insertEntails2)
        self.pushButton_30.clicked.connect( self.insertKindof2)
        self.pushButton_32.clicked.connect( self.insertKinds2)
        self.pushButton_34.clicked.connect( self.insertPartof2)
        self.pushButton_36.clicked.connect( self.insertParts2)
    def cantPointers(self):
          p_cnt = len(self.__antonyms) + len(self.__derivatives) + len(self.__relatesto) + len(self.__attributes) + len(self.__similar) + len(self.__domain) + len(self.__causes) + len(self.__entails) + len(self.__kindof) + len(self.__kinds) + len(self.__partof) + len(self.__parts)

          if(len(str(p_cnt))==1):
              p_cnt ="00" + str(p_cnt)
          if(len(str(p_cnt))==2):
              p_cnt ="0" + str(p_cnt)
          return p_cnt
    def ChangeHex(self,n):
      x = (n % 16)
      c = ""
      if (x < 10):
        c = x
      if (x == 10):
        c = "a"
      if (x == 11):
        c = "b"
      if (x == 12):
        c = "c"
      if (x == 13):
        c = "d"
      if (x == 14):
        c = "e"
      if (x == 15):
        c = "f"

      if (n - x != 0):
        return self.ChangeHex(n / 16) + str(c)
      else:
        return str(c)

    def insertmodifinDB(self):

        countexc = self.listWidget_4.count()

        self.__cursor.execute(unicode("DELETE FROM [exceptions] WHERE [word_inflected]= '"+self.comboBox_2.currentText()+"'"))
        self.__cursor.execute(unicode("DELETE FROM [noun_exc] WHERE [word_inflected]= '"+self.comboBox_2.currentText()+"'"))
        self.__cursor.execute(unicode("DELETE FROM [verb_exc] WHERE [word_inflected]= '"+self.comboBox_2.currentText()+"'"))
        self.__cursor.execute(unicode("DELETE FROM [adj_exc] WHERE [word_inflected]= '"+self.comboBox_2.currentText()+"'"))
        self.__cursor.execute(unicode("DELETE FROM [adv_exc] WHERE [word_inflected]= '"+self.comboBox_2.currentText()+"'"))

        if(countexc!=0):
           while(countexc > 0):
              wordexc = self.listWidget_4.item(countexc-1).text()
              self.__cursor.execute(unicode("INSERT OR REPLACE INTO [exceptions] ([word_inflected], [base_form]) VALUES ('"+self.comboBox_2.currentText()+"','"+wordexc[0:wordexc.indexOf(" -")]+"')"))
              self.__cursor.execute(unicode("INSERT OR REPLACE INTO ["+wordexc[wordexc.indexOf("> ")+2:len(wordexc)]+"_exc] ([word_inflected], [base_form]) VALUES ('"+self.comboBox_2.currentText()+"','"+wordexc[0:wordexc.indexOf(" -")]+"')"))
              countexc -= 1

        query = "SELECT num FROM [max_synset_offset]"
        self.__cursor.execute(unicode(query))
        max = self.__cursor.fetchall()
        max = int(max[0][0])

        verificword = "SELECT * FROM [index_sense] WHERE [lemma]='"+self.comboBox_2.currentText()+"'"
        self.__cursor.execute(unicode(verificword))
        verific = self.__cursor.fetchall()

        if(verific):
          print "sii"
          createconsult = "DELETE FROM [index_sense] WHERE [lemma]='"+self.comboBox_2.currentText()+"'"
          for id in self.__allsynset_offset:
             createconsult += "AND [synset_offset] !='"+id+"'"
          self.__cursor.execute(unicode(createconsult))

          cont = 0
          for row in self.__tablesynset:

            #consult = "DELETE FROM [data_"+str(row[0])+"_word_lex_id] WHERE [synset_offset]='"+str(self.__allsynset_offset[cont])+"' AND [word]='"+self.comboBox_2.currentText()+"'"
            #print consult

            w_cnt = self.ChangeHex(len(self.__allsynon[cont]))
            if(len(w_cnt)==1):
              w_cnt ="0"+w_cnt

            p_cnt = self.cantPointers()

            if(row[0]=="noun"):
              ss_type = "n"
            elif(row[0]=="verb"):
              ss_type = "v"
            elif(row[0]=="adj"):
              ss_type = "a"
            else:
              ss_type = "r"

            for word in self.__allsynon[cont]:
              if(str(word[0])==self.comboBox_2.currentText()):
                 consult = "UPDATE [data_"+str(row[0])+"_word_lex_id] SET [word_traslated]='"+str(row[1])+"'"
                 print consult
            if(int(self.__allsynset_offset[cont]) < max):
              consult = "UPDATE [data_"+str(row[0])+"] SET [ss_type]='"+ss_type+"', [w_cnt]='"+w_cnt+"', [p_cnt]='"+p_cnt+"', [sense]='"+row[2]+"', [sense_es]='"+row[3]+"', [sense_long]='"+row[4]+"', [sense_long_es]='"+row[5]+"', [gloss]='"+row[6]+"', [gloss_es]='"+row[7]+"' WHERE [synset_offset]='"+self.__allsynset_offset[cont]+"'"
            else:
              consult = "INSERT OR REPLACE INTO [data_"+str(row[0])+"] VALUES ('"+str(self.__allsynset_offset[cont])+"','00','"+ss_type+"','"+w_cnt+"','"+p_cnt+"','"+row[2]+"','"+row[3]+"','"+row[4]+"','"+row[5]+"','"+row[6]+"','"+row[7]+"')"
            print consult
            cont += 1
        else:
            print "noooo"



          #if(row[0]=="noun" and pos.find("1 ")==-1):
          #   pos += "1 "
          #if(row[0]=="verb" and pos.find("2 ")==-1):
          #   pos += "2 "
          #if(row[0]=="adj" and pos.find("3 ")==-1):
          #   pos += "3 "
          #if(row[0]=="adv" and pos.find("4 ")==-1):
          #   pos += "4 "




       # print self.__allsynset_offset
       # print  self.__tablesynset
       #self.__connect.commit()

    def modiftable(self):

        if(self.__search==True and len(self.lineEdit_4.text())==0):
               print "1"
               self.__search = False
               item = self.tableWidget.takeItem(self.tableWidget.currentRow(),self.tableWidget.currentColumn())
               self.__tablesynset[self.tableWidget.currentRow()][self.tableWidget.currentColumn()] = str(item.text())
               self.tableWidget.setItem(self.tableWidget.currentRow(),self.tableWidget.currentColumn(),item)
               self.__search = True
               print self.__search

        #print self.__tablesynset
        elif(self.__search==True and len(self.lineEdit_4.text())!=0):
               print "2"
               self.__search = False
               item = self.tableWidget.takeItem(self.tableWidget.currentRow(),self.tableWidget.currentColumn())
               self.__tablesynset[self.__arrayid[self.tableWidget.currentRow()]][self.tableWidget.currentColumn()] = str(item.text())
               self.tableWidget.setItem(self.tableWidget.currentRow(),self.tableWidget.currentColumn(),item)
               self.__search = True


    def busqueda(self):
        self.__search = False
        self.listWidget.clear()
        self.__arrayid = []
        columnb = 0
        contword = 0
        cant_row = self.tableWidget.rowCount()
        if(cant_row!=-1):
            while(cant_row!=0):
               self.tableWidget.removeRow(cant_row)
               cant_row -=1
            self.tableWidget.removeRow(0)

        self.__max_row1 = 0
        palabra = self.lineEdit_4.text()
        if(palabra!=""):
            self.__filter = 1
        else:
            self.__filter = 0

        if(len(palabra)==0):
         for word in self.__arrayfind:
                self.tableWidget.insertRow(self.__max_row1)
                self.tableWidget.setItem(self.__max_row1,columnb,QTableWidgetItem(self.__tablesynset[self.__max_row1][0]))
                columnb += 1
                self.tableWidget.setItem(self.__max_row1,columnb,QTableWidgetItem(self.__tablesynset[self.__max_row1][1]))
                columnb += 1
                self.tableWidget.setItem(self.__max_row1,columnb,QTableWidgetItem(self.__tablesynset[self.__max_row1][2]))
                columnb += 1
                self.tableWidget.setItem(self.__max_row1,columnb,QTableWidgetItem(self.__tablesynset[self.__max_row1][3]))
                columnb += 1
                self.tableWidget.setItem(self.__max_row1,columnb,QTableWidgetItem(self.__tablesynset[self.__max_row1][4]))
                columnb += 1
                self.tableWidget.setItem(self.__max_row1,columnb,QTableWidgetItem(self.__tablesynset[self.__max_row1][5]))
                columnb += 1
                self.tableWidget.setItem(self.__max_row1,columnb,QTableWidgetItem(self.__tablesynset[self.__max_row1][6]))
                columnb += 1
                self.tableWidget.setItem(self.__max_row1,columnb,QTableWidgetItem(self.__tablesynset[self.__max_row1][7]))
                self.__max_row1 += 1
                columnb = 0

        else:
         for word in self.__arrayfind:

            if(word.find(palabra)!=-1):
                self.__arrayid.append(contword)
                self.tableWidget.insertRow(self.__max_row1)
                self.tableWidget.setItem(self.__max_row1,columnb,QTableWidgetItem(self.__tablesynset[contword][0]))
                columnb += 1
                self.tableWidget.setItem(self.__max_row1,columnb,QTableWidgetItem(self.__tablesynset[contword][1]))
                columnb += 1
                self.tableWidget.setItem(self.__max_row1,columnb,QTableWidgetItem(self.__tablesynset[contword][2]))
                columnb += 1
                self.tableWidget.setItem(self.__max_row1,columnb,QTableWidgetItem(self.__tablesynset[contword][3]))
                columnb += 1
                self.tableWidget.setItem(self.__max_row1,columnb,QTableWidgetItem(self.__tablesynset[contword][4]))
                columnb += 1
                self.tableWidget.setItem(self.__max_row1,columnb,QTableWidgetItem(self.__tablesynset[contword][5]))
                columnb += 1
                self.tableWidget.setItem(self.__max_row1,columnb,QTableWidgetItem(self.__tablesynset[contword][6]))
                columnb += 1
                self.tableWidget.setItem(self.__max_row1,columnb,QTableWidgetItem(self.__tablesynset[contword][7]))
                self.__max_row1 += 1
            columnb = 0
            contword += 1
        self.__search = True

    def elimatrib(self):
          self.__search = False
          self.lineEdit_4.setText("")
          self.lineEdit_4.setEnabled(False)
          self.tableWidget.removeRow(self.__rowarray)
          self.__allsynon.pop(self.__rowarray)
          self.__tablesynset.pop(self.__rowarray)
          self.__allsynset_offset.pop(self.__rowarray)
          self.__max_row1 -= 1
          self.__search = True
          #aarr = ["as","ds","sf"]
          #print aarr.pop(2)
          #print aarr

    def modifexc(self):
        textexc = self.listWidget_4.takeItem(self.listWidget_4.currentRow()).text()
        self.lineEdit_5.setText(textexc[0:textexc.indexOf(" -")])
        ss_type = textexc[textexc.indexOf("> ")+2:len(textexc)]
        if(ss_type == "noun"):
            self.comboBox.setCurrentIndex(0)
        elif(ss_type == "verb"):
            self.comboBox.setCurrentIndex(1)
        elif(ss_type == "adj"):
            self.comboBox.setCurrentIndex(2)
        else:
            self.comboBox.setCurrentIndex(3)


    def insertexc(self):

        countexc = self.listWidget_4.count()
        bool = 0
        if(self.listWidget_4.count()<4 and self.lineEdit_5.text() != ""):
         exc = self.lineEdit_5.text()+" --> "+self.comboBox.currentText()

         while(countexc > 0):
            ss_type = self.listWidget_4.item(countexc-1).text()

            if (ss_type[ss_type.indexOf("> ")+2:len(ss_type)]==self.comboBox.currentText()):
              bool = 1
              break
            countexc -= 1
         if(bool ==0):
             self.listWidget_4.addItem(exc)

    def newfill(self):

        self.__search = False
        self.lineEdit_4.setText("")
        self.lineEdit_4.setEnabled(False)
        array1 = []
        array2 = [" "," "," "," "," "," "," "," "]
        self.__allsynon.append(array1)
        self.tableWidget.insertRow(self.__max_row1)
        self.__max_row1 += 1
        self.__allsynset_offset.append(str(self.__nummaxdb))
        self.__nummaxdb += 1
        self.__tablesynset.append(array2)
        self.__search = True

    def chekeando(self):
        if(self.checkAtributo(self.__difAtrib[0])!=True):
          self.pushButton_27.setEnabled(False)
        else:
          self.pushButton_27.setEnabled(True)
        if(self.checkAtributo(self.__difAtrib[1])!=True):
          self.pushButton_29.setEnabled(False)
        else:
          self.pushButton_29.setEnabled(True)
        if(self.checkAtributo(self.__difAtrib[3])!=True):
          self.pushButton_33.setEnabled(False)
        else:
          self.pushButton_33.setEnabled(True)
        if(self.checkAtributo(self.__difAtrib[2])!=True):
          self.pushButton_31.setEnabled(False)
        else:
          self.pushButton_31.setEnabled(True)
        if(self.checkAtributo(self.__difAtrib[4])!=True):
          self.pushButton_35.setEnabled(False)
        else:
          self.pushButton_35.setEnabled(True)
        if(self.checkAtributo(self.__difAtrib[5])!=True):
          self.pushButton_37.setEnabled(False)
        else:
          self.pushButton_37.setEnabled(True)
        if(self.checkAtributo(self.__difAtrib[6])!=True):
          self.pushButton_26.setEnabled(False)
        else:
          self.pushButton_26.setEnabled(True)
        if(self.checkAtributo(self.__difAtrib[7])!=True):
          self.pushButton_28.setEnabled(False)
        else:
          self.pushButton_28.setEnabled(True)
        if(self.checkAtributo(self.__difAtrib[8])!=True):
          self.pushButton_30.setEnabled(False)
        else:
          self.pushButton_30.setEnabled(True)
        if(self.checkAtributo(self.__difAtrib[9])!=True):
          self.pushButton_32.setEnabled(False)
        else:
          self.pushButton_32.setEnabled(True)
        if(self.checkAtributo(self.__difAtrib[10])!=True):
          self.pushButton_34.setEnabled(False)
        else:
          self.pushButton_34.setEnabled(True)
        if(self.checkAtributo(self.__difAtrib[11])!=True):
          self.pushButton_36.setEnabled(False)
        else:
          self.pushButton_36.setEnabled(True)

    def insertAtributo(self,cadena):
            self.listWidget.clear()
            aux = []
            array = []

            str = "SELECT DISTINCT([data_noun_ptr].[synset_offset_p]), [synset_offset] FROM [index_sense]  INNER JOIN [data_noun_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.comboBox_2.currentText()+"'AND ("+cadena+")"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:

                for w, s in result:
                  aux.append("noun")
                  aux.append(s)
                  aux.append(w)
                  str = "SELECT DISTINCT(word) FROM [data_noun_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_verb_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_adj_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_adv_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  aux.append("0")
                  array.append(aux)
                  aux = []

            str = "SELECT DISTINCT([data_verb_ptr].[synset_offset_p]), [synset_offset] FROM [index_sense]  INNER JOIN [data_verb_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.comboBox_2.currentText()+"'AND ("+cadena.replace("noun","verb")+")"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:

                for w, s in result:
                  aux.append("verb")
                  aux.append(s)
                  aux.append(w)
                  str = "SELECT DISTINCT(word) FROM [data_noun_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_verb_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_adj_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_adv_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  aux.append("0")
                  array.append(aux)
                  aux = []

            str = "SELECT DISTINCT([data_adj_ptr].[synset_offset_p]), [synset_offset] FROM [index_sense]  INNER JOIN [data_adj_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.comboBox_2.currentText()+"'AND ("+cadena.replace("noun","adj")+")"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:

                for w, s in result:
                  aux.append("adj")
                  aux.append(s)
                  aux.append(w)
                  str = "SELECT DISTINCT(word) FROM [data_noun_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_verb_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_adj_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_adv_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  aux.append("0")
                  array.append(aux)
                  aux = []

            str = "SELECT DISTINCT([data_adv_ptr].[synset_offset_p]), [synset_offset] FROM [index_sense]  INNER JOIN [data_adv_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='" + self.comboBox_2.currentText() + "'AND ("+cadena.replace("noun","adv")+")"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:
                for w, s in result:
                  aux.append("adv")
                  aux.append(s)
                  aux.append(w)
                  str = "SELECT DISTINCT(word) FROM [data_noun_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_verb_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_adj_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_adv_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  aux.append("0")
                  array.append(aux)

            return array

    def insertAtributo1(self,cadena):
            self.listWidget_2.clear()
            aux = []
            array = []

            str = "SELECT DISTINCT([data_noun_ptr].[synset_offset_p]), [synset_offset] FROM [index_sense]  INNER JOIN [data_noun_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.lineEdit_2.text()+"'AND ("+cadena+")"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:

                for w, s in result:
                  aux.append("noun")
                  aux.append(s)
                  aux.append(w)
                  str = "SELECT DISTINCT(word) FROM [data_noun_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_verb_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_adj_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_adv_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  aux.append("1")
                  array.append(aux)
                  aux = []

            str = "SELECT DISTINCT([data_verb_ptr].[synset_offset_p]), [synset_offset] FROM [index_sense]  INNER JOIN [data_verb_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.lineEdit_2.text()+"'AND ("+cadena.replace("noun","verb")+")"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:

                for w, s in result:
                  aux.append("verb")
                  aux.append(s)
                  aux.append(w)
                  str = "SELECT DISTINCT(word) FROM [data_noun_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_verb_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_adj_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_adv_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  aux.append("1")
                  array.append(aux)
                  aux = []

            str = "SELECT DISTINCT([data_adj_ptr].[synset_offset_p]), [synset_offset] FROM [index_sense]  INNER JOIN [data_adj_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.lineEdit_2.text()+"'AND ("+cadena.replace("noun","adj")+")"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:

                for w, s in result:
                  aux.append("adj")
                  aux.append(s)
                  aux.append(w)
                  str = "SELECT DISTINCT(word) FROM [data_noun_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_verb_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_adj_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_adv_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  aux.append("1")
                  array.append(aux)
                  aux = []

            str = "SELECT DISTINCT([data_adv_ptr].[synset_offset_p]), [synset_offset] FROM [index_sense]  INNER JOIN [data_adv_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.lineEdit_2.text()+"'AND ("+cadena.replace("noun","adv")+")"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:
                for w, s in result:
                  aux.append("adv")
                  aux.append(s)
                  aux.append(w)
                  str = "SELECT DISTINCT(word) FROM [data_noun_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_verb_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_adj_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  str = "SELECT DISTINCT(word) FROM [data_adv_word_lex_id] WHERE [synset_offset]='"+w+"'"
                  self.__cursor.execute(unicode(str))
                  data = self.__cursor.fetchall()
                  if data:
                   for a in data:
                        aux.append(a[0])
                  aux.append("1")
                  array.append(aux)

            return array


    def insertAntonyms1(self):
        self.__antonyms = self.insertAtributo(self.__difAtrib[0])

    def insertAntonyms(self):
        self.__arrepos = 0
        self.listWidget.clear()
        for w in self.__antonyms:
            str = ""
            aux = 0
            if(w[1]==self.__allsynset_offset[self.__rowarray]):
             for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
             self.listWidget.addItem(str[0:len(str)-2])



    def insertAntonyms2(self):
        self.__arrepos2 = 0
        array = []
        array = self.insertAtributo1(self.__difAtrib[0])

        for w in array:
            str = ""
            aux = 0
            for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
            self.listWidget_2.addItem(str[0:len(str)-2])

    def insertKindof2(self):
        self.__arrepos2 = 8
        array = []
        array = self.insertAtributo1(self.__difAtrib[8])

        for w in array:
            str = ""
            aux = 0
            for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
            self.listWidget_2.addItem(str[0:len(str)-2])

    def insertKinds2(self):
        self.__arrepos2 = 9
        array = []
        array = self.insertAtributo1(self.__difAtrib[9])

        for w in array:
            str = ""
            aux = 0
            for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
            self.listWidget_2.addItem(str[0:len(str)-2])

    def insertPartof2(self):
        self.__arrepos2 = 10
        array = []
        array = self.insertAtributo1(self.__difAtrib[10])

        for w in array:
            str = ""
            aux = 0
            for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
            self.listWidget_2.addItem(str[0:len(str)-2])

    def insertParts2(self):
        self.__arrepos2 = 11
        array = []
        array = self.insertAtributo1(self.__difAtrib[11])

        for w in array:
            str = ""
            aux = 0
            for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
            self.listWidget_2.addItem(str[0:len(str)-2])

    def insertDomain2(self):
        self.__arrepos2 = 5
        array = []
        array = self.insertAtributo1(self.__difAtrib[5])

        for w in array:
            str = ""
            aux = 0
            for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
            self.listWidget_2.addItem(str[0:len(str)-2])

    def insertDerivatives2(self):
        self.__arrepos2 = 1
        array = []
        array = self.insertAtributo1(self.__difAtrib[1])

        for w in array:
            str = ""
            aux = 0
            for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
            self.listWidget_2.addItem(str[0:len(str)-2])

    def insertRelatesto2(self):
        self.__arrepos2 = 2
        array = []
        array = self.insertAtributo1(self.__difAtrib[2])

        for w in array:
            str = ""
            aux = 0
            for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
            self.listWidget_2.addItem(str[0:len(str)-2])

    def insertAttributes2(self):
        self.__arrepos2 = 3
        array = []
        array = self.insertAtributo1(self.__difAtrib[3])

        for w in array:
            str = ""
            aux = 0
            for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
            self.listWidget_2.addItem(str[0:len(str)-2])

    def insertSimilar2(self):
        self.__arrepos2 = 4
        array = []
        array = self.insertAtributo1(self.__difAtrib[4])

        for w in array:
            str = ""
            aux = 0
            for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
            self.listWidget_2.addItem(str[0:len(str)-2])

    def insertCauses2(self):
        self.__arrepos2 = 6
        array = []
        array = self.insertAtributo1(self.__difAtrib[6])

        for w in array:
            str = ""
            aux = 0
            for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
            self.listWidget_2.addItem(str[0:len(str)-2])

    def insertEntails2(self):
        self.__arrepos2 = 7
        array = []
        array = self.insertAtributo1(self.__difAtrib[7])

        for w in array:
            str = ""
            aux = 0
            for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
            self.listWidget_2.addItem(str[0:len(str)-2])

    def checkAtributo(self,cadena):

            str = "SELECT DISTINCT([data_noun_ptr].[synset_offset_p]) FROM [index_sense]  INNER JOIN [data_noun_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.lineEdit_2.text()+"'AND ("+cadena+")"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:
                return True

            str = "SELECT DISTINCT([data_verb_ptr].[synset_offset_p]) FROM [index_sense]  INNER JOIN [data_verb_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.lineEdit_2.text()+"'AND ("+cadena.replace("noun","verb")+")"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:
                return True

            str = "SELECT DISTINCT([data_adj_ptr].[synset_offset_p]) FROM [index_sense]  INNER JOIN [data_adj_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='"+self.lineEdit_2.text()+"'AND ("+cadena.replace("noun","adj")+")"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:
                return True

            str = "SELECT DISTINCT([data_adv_ptr].[synset_offset_p]) FROM [index_sense]  INNER JOIN [data_adv_ptr] USING([synset_offset]) WHERE [index_sense].[lemma]='" +self.lineEdit_2.text()+ "'AND ("+cadena.replace("noun","adv")+")"
            self.__cursor.execute(unicode(str))
            result = self.__cursor.fetchall()
            if result:
                return True

    def insertAntonyms1(self):
        self.__antonyms = self.insertAtributo(self.__difAtrib[0])

    def insertAntonyms(self):
        self.__arrepos = 0
        self.listWidget.clear()
        print self.__antonyms
        for w in self.__antonyms:
            str = ""
            aux = 0
            if(w[1]==self.__allsynset_offset[self.__rowarray]):
             for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
             self.listWidget.addItem(str[0:len(str)-2])

    def insertKindof1(self):
        self.__kindof = self.insertAtributo(self.__difAtrib[8])


    def insertKindof(self):
        self.__arrepos = 8


        self.listWidget.clear()
        for w in self.__kindof:
            str = ""
            aux = 0
            if(w[1]==self.__allsynset_offset[self.__rowarray]):
             for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
             self.listWidget.addItem(str[0:len(str)-2])


    def insertKinds1(self):
        self.__kinds = self.insertAtributo(self.__difAtrib[9])


    def insertKinds(self):
        self.__arrepos = 9
        self.listWidget.clear()
        for w in self.__kinds:
            str = ""
            aux = 0
            if(w[1]==self.__allsynset_offset[self.__rowarray]):
             for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
             self.listWidget.addItem(str[0:len(str)-2])

    def insertPartof1(self):
        self.__partof = self.insertAtributo(self.__difAtrib[10])


    def insertPartof(self):
        self.__arrepos = 10
        self.listWidget.clear()
        for w in self.__partof:
            str = ""
            aux = 0
            if(w[1]==self.__allsynset_offset[self.__rowarray]):
             for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
             self.listWidget.addItem(str[0:len(str)-2])

    def insertParts1(self):
        self.__parts = self.insertAtributo(self.__difAtrib[11])


    def insertParts(self):
        self.__arrepos = 11
        self.listWidget.clear()
        for w in self.__parts:
            str = ""
            aux = 0
            if(w[1]==self.__allsynset_offset[self.__rowarray]):
             for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
             self.listWidget.addItem(str[0:len(str)-2])

    def insertDomain1(self):
        self.__domain = self.insertAtributo(self.__difAtrib[5])


    def insertDomain(self):
        self.__arrepos = 5
        self.listWidget.clear()
        for w in self.__domain:
            str = ""
            aux = 0
            if(w[1]==self.__allsynset_offset[self.__rowarray]):
             for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
             self.listWidget.addItem(str[0:len(str)-2])

    def insertDerivatives1(self):
        self.__derivatives = self.insertAtributo(self.__difAtrib[1])


    def insertDerivatives(self):
        self.__arrepos = 1
        self.listWidget.clear()
        for w in self.__derivatives:
            str = ""
            aux = 0
            if(w[1]==self.__allsynset_offset[self.__rowarray]):
             for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
             self.listWidget.addItem(str[0:len(str)-2])

    def insertAttributes1(self):
        self.__relatesto = self.insertAtributo(self.__difAtrib[3])

    def insertAttributes(self):
        self.__arrepos = 3
        self.listWidget.clear()
        for w in self.__attributes:
            str = ""
            aux = 0
            if(w[1]==self.__allsynset_offset[self.__rowarray]):
             for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
             self.listWidget.addItem(str[0:len(str)-2])

    def insertRelatesto1(self):
        self.__relatesto = self.insertAtributo(self.__difAtrib[2])

    def insertRelatesto(self):
        self.__arrepos = 2
        self.listWidget.clear()
        for w in self.__relatesto:
            str = ""
            aux = 0
            if(w[1]==self.__allsynset_offset[self.__rowarray]):
             for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
             self.listWidget.addItem(str[0:len(str)-2])

    def insertSimilar1(self):
        self.__similar = self.insertAtributo(self.__difAtrib[4])


    def insertSimilar(self):
        self.__arrepos = 4
        self.listWidget.clear()
        for w in self.__similar:
            str = ""
            aux = 0
            if(w[1]==self.__allsynset_offset[self.__rowarray]):
             for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
             self.listWidget.addItem(str[0:len(str)-2])

    def insertCauses1(self):
        self.__causes = self.insertAtributo(self.__difAtrib[6])


    def insertCauses(self):
        self.__arrepos = 6
        self.listWidget.clear()
        for w in self.__causes:
            str = ""
            aux = 0
            if(w[1]==self.__allsynset_offset[self.__rowarray]):
             for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
             self.listWidget.addItem(str[0:len(str)-2])

    def insertEntails1(self):
        self.__entails = self.insertAtributo(self.__difAtrib[7])


    def insertEntails(self):
        self.__arrepos = 7
        self.listWidget.clear()
        for w in self.__entails:
            str = ""
            aux = 0
            if(w[1]==self.__allsynset_offset[self.__rowarray]):
             for a in w:
              if(aux > 2):
               str += a+", "
              else:
               aux += 1
             self.listWidget.addItem(str[0:len(str)-2])

    def actualizar1(self):
        self.__search = False
        cant_row = self.tableWidget.rowCount()
        self.listWidget.clear()
        self.__allsynon = []
        self.listWidget_4.clear()
        if(cant_row!=-1):
            while(cant_row!=0):
               self.tableWidget.removeRow(cant_row)
               cant_row -=1
            self.tableWidget.removeRow(0)
            self.__row1 = 0
            self.__max_row1 = 0
            self.__column1 = 2

    def actualizar2(self):
        cant_row = self.tableWidget_2.rowCount()
        if(cant_row!=-0):
            while(cant_row!=0):
               self.tableWidget_2.removeRow(cant_row)
               cant_row -=1
            self.tableWidget_2.removeRow(0)
            self.__row2 = 0
            self.__max_row2 = 0
            self.__column2 = 2

    def insertRow1(self):

         self.__allsynset_offset = []
         aux = []

         self.insertAntonyms1()
         self.insertDerivatives1()
         self.insertRelatesto1()
         self.insertAttributes1()
         self.insertSimilar1()
         self.insertDomain1()
         self.insertCauses1()
         self.insertEntails1()
         self.insertKindof1()
         self.insertKinds1()
         self.insertPartof1()
         self.insertParts1()

         self.findexc()

         str = "SELECT ss_type,synset_offset,sense_number,tag_cnt FROM [index_sense] WHERE [lemma]='"+self.comboBox_2.currentText()+"' ORDER BY [ss_type],[tag_cnt] DESC, [sense_number]"
         self.__cursor.execute(unicode(str))
         result = self.__cursor.fetchall()

         for con in result:
             self.tableWidget.insertRow(self.__max_row1)
             self.__max_row1 += 1

         for a, b, c, d in result:
            self.__allsynset_offset.append(b)
            if(a==1):
                aux.append("noun")
                self.tableWidget.setItem(self.__row1,0,QTableWidgetItem("noun"))
                str = "SELECT DISTINCT([word_traslated]) FROM [data_noun_word_lex_id] WHERE [word]='"+self.comboBox_2.currentText()+"' AND [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                traslated = self.__cursor.fetchall()
                if(traslated):
                    aux.append(traslated[0][0])
                    self.tableWidget.setItem(self.__row1,1,QTableWidgetItem(traslated[0][0]))
                else:
                    aux.append(" ")
                    self.tableWidget.setItem(self.__row1,1,QTableWidgetItem(" "))

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
                aux.append(data[0][0])
                aux.append(data[0][1])
                aux.append(data[0][2])
                aux.append(data[0][3])
                aux.append(data[0][4])
                aux.append(data[0][5])
                self.__tablesynset.append(aux)
                aux = []

            if(a==2):
                aux.append("verb")
                self.tableWidget.setItem(self.__row1,0,QTableWidgetItem("verb"))
                str = "SELECT DISTINCT([word_traslated]) FROM [data_verb_word_lex_id] WHERE [word]='"+self.comboBox_2.currentText()+"'AND [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                traslated = self.__cursor.fetchall()
                if(traslated):
                    aux.append(traslated[0][0])
                    self.tableWidget.setItem(self.__row1,1,QTableWidgetItem(traslated[0][0]))
                else:
                    aux.append(" ")
                    self.tableWidget.setItem(self.__row1,1,QTableWidgetItem(" "))
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
                aux.append(data[0][0])
                aux.append(data[0][1])
                aux.append(data[0][2])
                aux.append(data[0][3])
                aux.append(data[0][4])
                aux.append(data[0][5])
                self.__tablesynset.append(aux)
                aux = []
            if(a==3 or a==5):
                aux.append("adj")
                self.tableWidget.setItem(self.__row1,0,QTableWidgetItem("adj"))
                str = "SELECT DISTINCT([word_traslated]) FROM [data_adj_word_lex_id] WHERE [word]='"+self.comboBox_2.currentText()+"'AND [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                traslated = self.__cursor.fetchall()
                if(traslated):
                    aux.append(traslated[0][0])
                    self.tableWidget.setItem(self.__row1,1,QTableWidgetItem(traslated[0][0]))
                else:
                    aux.append(" ")
                    self.tableWidget.setItem(self.__row1,1,QTableWidgetItem(" "))
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
                aux.append(data[0][0])
                aux.append(data[0][1])
                aux.append(data[0][2])
                aux.append(data[0][3])
                aux.append(data[0][4])
                aux.append(data[0][5])
                self.__tablesynset.append(aux)
                aux = []
            if(a==4):
                aux.append("adv")
                self.tableWidget.setItem(self.__row1,0,QTableWidgetItem("adv"))
                str = "SELECT DISTINCT([word_traslated]) FROM [data_adv_word_lex_id] WHERE [word]='"+self.comboBox_2.currentText()+"'AND [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                traslated = self.__cursor.fetchall()
                if(traslated):
                    aux.append(traslated[0][0])
                    self.tableWidget.setItem(self.__row1,1,QTableWidgetItem(traslated[0][0]))
                else:
                    aux.append(" ")
                    self.tableWidget.setItem(self.__row1,1,QTableWidgetItem(" "))
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
                aux.append(data[0][0])
                aux.append(data[0][1])
                aux.append(data[0][2])
                aux.append(data[0][3])
                aux.append(data[0][4])
                aux.append(data[0][5])
                self.__tablesynset.append(aux)
                aux = []

            self.__column1 = 2
            self.__row1 += 1

         self.insertSynonyms()
         self.tableWidget.horizontalHeader().setStretchLastSection(True)
         self.__search = True

    def findexc(self):
        str = "SELECT base_form FROM [exceptions] WHERE [word_inflected]='"+self.comboBox_2.currentText()+"'"
        self.__cursor.execute(unicode(str))
        resultword = self.__cursor.fetchall()

        if(resultword):
            str = "SELECT base_form FROM [noun_exc] WHERE [word_inflected]='"+self.comboBox_2.currentText()+"'"
            self.__cursor.execute(unicode(str))
            base = self.__cursor.fetchall()
            if(base):
                self.listWidget_4.addItem(base[0][0]+" --> noun")

            str = "SELECT base_form FROM [verb_exc] WHERE [word_inflected]='"+self.comboBox_2.currentText()+"'"
            self.__cursor.execute(unicode(str))
            base = self.__cursor.fetchall()
            if(base):
                self.listWidget_4.addItem(base[0][0]+" --> verb")

            str = "SELECT base_form FROM [adj_exc] WHERE [word_inflected]='"+self.comboBox_2.currentText()+"'"
            self.__cursor.execute(unicode(str))
            base = self.__cursor.fetchall()
            if(base):
                self.listWidget_4.addItem(base[0][0]+" --> adj")

            str = "SELECT base_form FROM [adv_exc] WHERE [word_inflected]='"+self.comboBox_2.currentText()+"'"
            self.__cursor.execute(unicode(str))
            base = self.__cursor.fetchall()
            if(base):
                self.listWidget_4.addItem(base[0][0]+" --> adv")


    def insertRow2(self):
         self.__allsynset_offsetdown = []
         aux = []


         str = "SELECT ss_type,synset_offset,sense_number,tag_cnt FROM [index_sense] WHERE [lemma]='"+self.comboBox_3.currentText()+"' ORDER BY [ss_type],[tag_cnt] DESC, [sense_number]"
         self.__cursor.execute(unicode(str))
         result = self.__cursor.fetchall()

         for con in result:
             self.tableWidget_2.insertRow(self.__max_row2)
             self.__max_row2 += 1

         for a, b, c, d in result:
            self.__allsynset_offsetdown.append(b)
            if(a==1):
                aux.append("noun")
                self.tableWidget_2.setItem(self.__row2,0,QTableWidgetItem("noun"))
                str = "SELECT DISTINCT([word_traslated]) FROM [data_noun_word_lex_id] WHERE [word]='"+self.comboBox_3.currentText()+"' AND [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                traslated = self.__cursor.fetchall()
                if(traslated):
                    aux.append(traslated[0][0])
                    self.tableWidget_2.setItem(self.__row2,1,QTableWidgetItem(traslated[0][0]))
                else:
                    aux.append(" ")
                    self.tableWidget_2.setItem(self.__row2,1,QTableWidgetItem(" "))
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
                aux.append(data[0][0])
                aux.append(data[0][1])
                aux.append(data[0][2])
                aux.append(data[0][3])
                aux.append(data[0][4])
                aux.append(data[0][5])
                self.__tablesynsetdown.append(aux)
                aux = []
            if(a==2):
                aux.append("verb")
                self.tableWidget_2.setItem(self.__row2,0,QTableWidgetItem("verb"))
                str = "SELECT DISTINCT([word_traslated]) FROM [data_verb_word_lex_id] WHERE [word]='"+self.comboBox_3.currentText()+"' AND [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                traslated = self.__cursor.fetchall()
                if(traslated):
                    aux.append(traslated[0][0])
                    self.tableWidget_2.setItem(self.__row2,1,QTableWidgetItem(traslated[0][0]))
                else:
                    aux.append(" ")
                    self.tableWidget_2.setItem(self.__row2,1,QTableWidgetItem(" "))
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
                aux.append(data[0][0])
                aux.append(data[0][1])
                aux.append(data[0][2])
                aux.append(data[0][3])
                aux.append(data[0][4])
                aux.append(data[0][5])
                self.__tablesynsetdown.append(aux)
                aux = []
            if(a==3 or a==5):
                aux.append("adj")
                self.tableWidget_2.setItem(self.__row2,0,QTableWidgetItem("adj"))
                str = "SELECT DISTINCT([word_traslated]) FROM [data_adj_word_lex_id] WHERE [word]='"+self.comboBox_3.currentText()+"' AND [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                traslated = self.__cursor.fetchall()
                if(traslated):
                    aux.append(traslated[0][0])
                    self.tableWidget_2.setItem(self.__row2,1,QTableWidgetItem(traslated[0][0]))
                else:
                    aux.append(" ")
                    self.tableWidget_2.setItem(self.__row2,1,QTableWidgetItem(" "))
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
                aux.append(data[0][0])
                aux.append(data[0][1])
                aux.append(data[0][2])
                aux.append(data[0][3])
                aux.append(data[0][4])
                aux.append(data[0][5])
                self.__tablesynsetdown.append(aux)
                aux = []
            if(a==4):
                aux.append("adv")
                self.tableWidget_2.setItem(self.__row2,0,QTableWidgetItem("adv"))
                str = "SELECT DISTINCT([word_traslated]) FROM [data_adv_word_lex_id] WHERE [word]='"+self.comboBox_3.currentText()+"' AND [synset_offset]='"+b+"'"
                self.__cursor.execute(unicode(str))
                traslated = self.__cursor.fetchall()
                if(traslated):
                    aux.append(traslated[0][0])
                    self.tableWidget_2.setItem(self.__row2,1,QTableWidgetItem(traslated[0][0]))
                else:
                    aux.append(" ")
                    self.tableWidget_2.setItem(self.__row2,1,QTableWidgetItem(" "))
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
                aux.append(data[0][0])
                aux.append(data[0][1])
                aux.append(data[0][2])
                aux.append(data[0][3])
                aux.append(data[0][4])
                aux.append(data[0][5])
                self.__tablesynsetdown.append(aux)
                aux = []


            self.__column2 = 2
            self.__row2 += 1
         self.insertSynonyms2()

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
          postant = 0
          self.textEdit.setText(self.__bbook[self.listWidget_3.currentRow()].replace("\n\n",""))
          textbook = self.__bbook[self.listWidget_3.currentRow()].replace("\n\n","")
          post = lower(textbook).find(" "+self.lineEdit_3.text().toLower()+" ")
          while(post!=-1):
           self.pintar(postant + post + 1,postant + post + len(self.lineEdit_3.text()) + 1)
           textbook = textbook[post+len(self.lineEdit_3.text()):len(textbook)]
           postant += post+len(self.lineEdit_3.text())
           post = lower(textbook).find(" "+self.lineEdit_3.text().toLower()+" ")



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
        self.__filasel.append(self.tableWidget_2.takeItem(self.__row,7))

        self.tableWidget_2.setItem(self.__row,0,QTableWidgetItem(self.__filasel[0]))
        self.tableWidget_2.setItem(self.__row,1,QTableWidgetItem(self.__filasel[1]))
        self.tableWidget_2.setItem(self.__row,2,QTableWidgetItem(self.__filasel[2]))
        self.tableWidget_2.setItem(self.__row,3,QTableWidgetItem(self.__filasel[3]))
        self.tableWidget_2.setItem(self.__row,4,QTableWidgetItem(self.__filasel[4]))
        self.tableWidget_2.setItem(self.__row,5,QTableWidgetItem(self.__filasel[5]))
        self.tableWidget_2.setItem(self.__row,6,QTableWidgetItem(self.__filasel[6]))
        self.tableWidget_2.setItem(self.__row,6,QTableWidgetItem(self.__filasel[7]))
        #self.tableWidget_2.insert

        #self.actualizar2()
        #self.insertRow2()


    def upsense(self):
       self.__search = False
       self.lineEdit_4.setText("")
       self.lineEdit_4.setEnabled(False)
       if(self.__filasel.__len__() != 0):
        self.tableWidget.insertRow(self.__max_row1)

        self.tableWidget.setItem(self.__max_row1,0,QTableWidgetItem(self.__filasel[0]))
        self.tableWidget.setItem(self.__max_row1,1,QTableWidgetItem(self.__filasel[1]))
        self.tableWidget.setItem(self.__max_row1,2,QTableWidgetItem(self.__filasel[2]))
        self.tableWidget.setItem(self.__max_row1,3,QTableWidgetItem(self.__filasel[3]))
        self.tableWidget.setItem(self.__max_row1,4,QTableWidgetItem(self.__filasel[4]))
        self.tableWidget.setItem(self.__max_row1,5,QTableWidgetItem(self.__filasel[5]))
        self.tableWidget.setItem(self.__max_row1,6,QTableWidgetItem(self.__filasel[6]))
        self.tableWidget.setItem(self.__max_row1,7,QTableWidgetItem(self.__filasel[7]))
        self.__max_row1 += 1

        self.__filasel = []
        select = self.__allsynondown[self.__row]
        self.__allsynon.append(select)
        self.__tablesynset.append(self.__tablesynsetdown[self.__row])
        self.__allsynset_offset.append(self.__allsynset_offsetdown[self.__row])
        self.__search = True

    def insertSynonyms(self):

            self.listWidget.clear()



            str = "SELECT [synset_offset] FROM [index_sense] WHERE [lemma]='"+self.comboBox_2.currentText()+"' ORDER BY [ss_type],[tag_cnt] DESC, [sense_number]"
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

        #self.lineEdit_4.setText("")
        if(self.__filter==0):
           self.lineEdit_4.setEnabled(True)
           self.__arrayid = []
           cant_row = self.tableWidget.rowCount()
           self.__arrayfind = []
           pos = 0
           self.__columnselected = self.tableWidget.currentColumn()
           while(cant_row > pos):
             selectw = self.__tablesynset[pos][self.__columnselected]
             self.__arrayfind.append(selectw)
             pos += 1

        self.listWidget.clear()
        self.__arrepos = 12
        row = self.tableWidget.currentRow()
        if(len(self.lineEdit_4.text())!=0 and self.__arrayid.__len__()>0):
            self.__rowarray = self.__arrayid[row]
        else:
            self.__rowarray = row
        for w in self.__allsynon[self.__rowarray]:
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
                    self.listWidget.addItem(w[0])
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
        array = []
        array = self.insertAtributo1(self.__difAtrib[self.__arrepos2])
        aux = array[select]
        aux[1]=self.__allsynset_offset[self.__rowarray]
        if(self.__arrepos==0):
            self.__antonyms.append(aux)
        elif(self.__arrepos==1):
            self.__derivatives.append(aux)
        elif(self.__arrepos==2):
            self.__relatesto.append(aux)
        elif(self.__arrepos==3):
            self.__attributes.append(aux)
        elif(self.__arrepos==4):
            self.__similar.append(aux)
        elif(self.__arrepos==5):
            self.__domain.append(aux)
        elif(self.__arrepos==6):
            self.__causes.append(aux)
        elif(self.__arrepos==7):
            self.__entails.append(aux)
        elif(self.__arrepos==8):
            self.__kindof.append(aux)
        elif(self.__arrepos==9):
            self.__kinds.append(aux)
        elif(self.__arrepos==10):
            self.__partof.append(aux)
        elif(self.__arrepos==11):
            self.__parts.append(aux)
        else:
            array = []
            array.append(str(relaword.text()))
            self.__allsynon[self.__rowarray].append(array)


    def modrelacion(self):
        if(self.__arrepos==12):
         self.pushButton_7.setText("Modific")
         self.__rowselection = self.listWidget.currentRow()
        #self.listWidget.

    def cambrela(self):

        if(self.__rowselection != -1):

            welim = self.listWidget.takeItem(self.__rowselection)
            self.listWidget.insertItem(self.__rowselection,self.lineEdit.text())
            self.pushButton_7.setText("Insert")
            if(self.__arrepos==0):
             self.__antonyms.remove(str(welim.text()))
             self.__antonyms.insert(self.__rowselection,self.lineEdit.text())
            elif(self.__arrepos==1):
             self.__derivatives.remove(str(welim.text()))
             self.__derivatives.insert(self.__rowselection,self.lineEdit.text())
            elif(self.__arrepos==2):
             self.__relatesto.remove(str(welim.text()))
             self.__relatesto.insert(self.__rowselection,self.lineEdit.text())
            elif(self.__arrepos==3):
             self.__attributes.remove(str(welim.text()))
             self.__attributes.insert(self.__rowselection,self.lineEdit.text())
            elif(self.__arrepos==4):
             self.__similar.remove(str(welim.text()))
             self.__similar.insert(self.__rowselection,self.lineEdit.text())
            elif(self.__arrepos==5):
             self.__domain.remove(str(welim.text()))
             self.__domain.insert(self.__rowselection,self.lineEdit.text())
            elif(self.__arrepos==6):
             self.__causes.remove(str(welim.text()))
             self.__causes.insert(self.__rowselection,self.lineEdit.text())
            elif(self.__arrepos==7):
             self.__entails.remove(str(welim.text()))
             self.__entails.insert(self.__rowselection,self.lineEdit.text())
            elif(self.__arrepos==8):
             self.__kindof.remove(str(welim.text()))
             self.__kindof.insert(self.__rowselection,self.lineEdit.text())
            elif(self.__arrepos==9):
             self.__kinds.remove(str(welim.text()))
             self.__kinds.insert(self.__rowselection,self.lineEdit.text())
            elif(self.__arrepos==10):
             self.__partof.remove(str(welim.text()))
             self.__partof.insert(self.__rowselection,self.lineEdit.text())
            elif(self.__arrepos==11):
             self.__parts.remove(str(welim.text()))
             self.__parts.insert(self.__rowselection,self.lineEdit.text())
            else:
             array = []
             arrayw = [self.lineEdit.text()]

             for wor in self.__allsynon[self.__rowarray]:
                if(wor!=self.__allsynon[self.__rowarray][self.__rowselection]):
                    array.append(wor)
                else:
                    array.append(arrayw)
             self.__allsynon[self.__rowarray] = array
            self.__rowselection = -1
        else:
            self.listWidget.addItem(self.lineEdit.text())
            if(self.__arrepos==0):
              self.__antonyms.append(str(self.lineEdit.text()))
            elif(self.__arrepos==1):
              self.__derivatives.append(str(self.lineEdit.text()))
            elif(self.__arrepos==2):
              self.__relatesto.append(str(self.lineEdit.text()))
            elif(self.__arrepos==3):
              self.__attributes.append(str(self.lineEdit.text()))
            elif(self.__arrepos==4):
              self.__similar.append(str(self.lineEdit.text()))
            elif(self.__arrepos==5):
              self.__domain.append(str(self.lineEdit.text()))
            elif(self.__arrepos==6):
              self.__causes.append(str(self.lineEdit.text()))
            elif(self.__arrepos==7):
              self.__entails.append(str(self.lineEdit.text()))
            elif(self.__arrepos==8):
              self.__kindof.append(str(self.lineEdit.text()))
            elif(self.__arrepos==9):
              self.__kinds.append(str(self.lineEdit.text()))
            elif(self.__arrepos==10):
              self.__partof.append(str(self.lineEdit.text()))
            elif(self.__arrepos==11):
              self.__parts.append(str(self.lineEdit.text()))
            else:
              array = []
              array.append(str(self.lineEdit.text()))
              self.__allsynon[self.__rowarray].append(array)

    def elim(self):
        #welim = self.listWidget.takeItem(self.__rowselection)
        self.listWidget.takeItem(self.__rowselection)

        if(self.__arrepos==0):
            if(self.__antonyms[self.__rowselection][len(self.__antonyms[self.__rowselection])-1]=="1"):
               self.__antonyms.pop(self.__rowselection)
        elif(self.__arrepos==1):
            if(self.__derivatives[self.__rowselection][len(self.__derivatives[self.__rowselection])-1]=="1"):
               self.__derivatives.pop(self.__rowselection)
        elif(self.__arrepos==2):
            if(self.__relatesto[self.__rowselection][len(self.__relatesto[self.__rowselection])-1]=="1"):
               self.__relatesto.pop(self.__rowselection)
        elif(self.__arrepos==3):
            if(self.__attributes[self.__rowselection][len(self.__attributes[self.__rowselection])-1]=="1"):
               self.__attributes.pop(self.__rowselection)
        elif(self.__arrepos==4):
            if(self.__similar[self.__rowselection][len(self.__similar[self.__rowselection])-1]=="1"):
               self.__similar.pop(self.__rowselection)
        elif(self.__arrepos==5):
            if(self.__domain[self.__rowselection][len(self.__domain[self.__rowselection])-1]=="1"):
               self.__domain.pop(self.__rowselection)
        elif(self.__arrepos==6):
            if(self.__causes[self.__rowselection][len(self.__causes[self.__rowselection])-1]=="1"):
               self.__causes.pop(self.__rowselection)
        elif(self.__arrepos==7):
            if(self.__entails[self.__rowselection][len(self.__entails[self.__rowselection])-1]=="1"):
               self.__entails.pop(self.__rowselection)
        elif(self.__arrepos==8):
            if(self.__kindof[self.__rowselection][len(self.__kindof[self.__rowselection])-1]=="1"):
               self.__kindof.pop(self.__rowselection)
        elif(self.__arrepos==9):
            if(self.__kinds[self.__rowselection][len(self.__kinds[self.__rowselection])-1]=="1"):
               self.__kinds.pop(self.__rowselection)
        elif(self.__arrepos==10):
            if(self.__partof[self.__rowselection][len(self.__partof[self.__rowselection])-1]=="1"):
               self.__partof.pop(self.__rowselection)
        elif(self.__arrepos==11):
            if(self.__parts[self.__rowselection][len(self.__parts[self.__rowselection])-1]=="1"):
               self.__parts.pop(self.__rowselection)
        else:
            array = []

            for wor in self.__allsynon[self.__rowarray]:
                if(wor!=self.__allsynon[self.__rowarray][self.__rowselection]):
                    array.append(wor)
            self.__allsynon[self.__rowarray] = array
        self.__rowselection = -1
        self.pushButton_7.setText("Insertar")

    def pintar( self, pi,pf):
        format = QTextCharFormat()
        format.setBackground(QBrush(Qt.yellow))
        cursor = self.textEdit.textCursor()
        cursor.setPosition(pi)
        cursor.setPosition(pf, QTextCursor.KeepAnchor)
        cursor.mergeCharFormat(format)
        cursor.clearSelection()

    def insertSynonyms2(self):
            self.__allsynondown = []

            str = "SELECT [synset_offset] FROM [index_sense] WHERE [lemma]='"+self.comboBox_3.currentText()+"'ORDER BY [ss_type],[tag_cnt] DESC, [sense_number]"
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








