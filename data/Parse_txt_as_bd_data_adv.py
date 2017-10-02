#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
from string import lower

class ParseDataAdv():
    """
    Clase del Analizador de los datos de los adjetivos de Wordnet 3.0
    :param target_sqlite_db: ruta + nombre de la BD sqlite donde se escribirán los datos.
    :param type: str
    :param data_to_parse: fichero de los datos de los adjetivos de Wordnet 3.0
    :param type: str
    :rtype: 0



    """

    def __init__( self, target_sqlite_db, data_to_parse):
      self.__connect = sqlite3.connect(target_sqlite_db)
      self.__cursor = self.__connect.cursor()

      self.__aux = 0
      self.__cant_pointers = 0
      archivo = open(data_to_parse)
      lineas = archivo.readlines()
      archivo.close()

      for linea in lineas:
          #print linea[0:8]+"-"+linea[9:11]+"-"+linea[12:13]+"-"+linea[14:16]+"-"+linea[16:linea.find("|")-1]+"-"+linea[linea.find("|")+2:linea.find(";")]+"-"+linea[linea.find(";")+2:linea.__len__()]
          gloss = linea[linea.find("|")+2:linea.__len__()]
          palabra =  linea[17:linea.find("|")-1]+" "
          cant_words = int(linea[14:16], 16)

          while(self.__cant_pointers < 1000):
              if(self.__cant_pointers == 0):
                  w_aux = "00"
              elif(self.__cant_pointers == 10):
                  w_aux = "0"
              elif(self.__cant_pointers == 100):
                  w_aux = ""
              words = palabra.find(" "+w_aux+str(self.__cant_pointers)+" ")
              if(words != -1):
                break
              self.__cant_pointers += 1

          all_words = palabra[0:words]

          if(gloss.find('; "') != -1):
           self.__cursor.execute("INSERT OR REPLACE INTO [data_adv] ([synset_offset], [lex_filenum], [ss_type], [w_cnt], [p_cnt], [sense], [sense_es], [sense_long], [sense_long_es], [gloss], [gloss_es]) VALUES (?,?,?,?,?,?,'not','not','not',?,'not') ", (linea[0:8], linea[9:11], linea[12:13], linea[14:16], w_aux+str(self.__cant_pointers), gloss[0:gloss.find('; "')], gloss[gloss.find('; "')+2:gloss.__len__()]))
          else:
           self.__cursor.execute("INSERT OR REPLACE INTO [data_adv] ([synset_offset], [lex_filenum], [ss_type], [w_cnt], [p_cnt], [sense], [sense_es], [sense_long], [sense_long_es], [gloss], [gloss_es]) VALUES (?,?,?,?,?,?,'not','not','not','not','not') ", (linea[0:8], linea[9:11], linea[12:13], linea[14:16], w_aux+str(self.__cant_pointers), gloss))

          all_pointers = palabra[words+5:palabra.__len__()]
          #print all_words
          while(cant_words > 1):
           #print all_words[0:all_words.find(" ")]+"-"+all_words[all_words.find(" ")+1:all_words.find(" ")+2]
           self.__cursor.execute("INSERT OR REPLACE INTO [data_adv_word_lex_id] ([synset_offset], [word], [word_traslated], [lex_id]) VALUES (?,?,'not',?) ", (linea[0:8], lower(all_words[0:all_words.find(" ")]), all_words[all_words.find(" ")+1:all_words.find(" ")+2]))
           all_words = all_words[all_words.find(" ")+3:all_words.__len__()]
           cant_words -= 1
          #print all_words[0:all_words.find(" ")]+"-"+all_words[all_words.find(" ")+1:all_words.find(" ")+2]
          self.__cursor.execute("INSERT OR REPLACE INTO [data_adv_word_lex_id] ([synset_offset], [word], [word_traslated], [lex_id]) VALUES (?,?,'not',?) ", (linea[0:8], lower(all_words[0:all_words.find(" ")]), all_words[all_words.find(" ")+1:all_words.find(" ")+2]))

          while(self.__cant_pointers > 0):
            #print all_pointers[0:all_pointers.find(" ")]
            other = all_pointers[all_pointers.find(" ")+1:all_pointers.find(" ")+17]
            #print other[0:8]+"-"+other[9:10]+"-"+other[11:other.__len__()]
            self.__cursor.execute("INSERT OR REPLACE INTO [data_adv_ptr] ([synset_offset], [pointer_symbol], [synset_offset_p], [pos], [source/target]) VALUES (?,?,?,?,?) ", (linea[0:8], (all_pointers[0:all_pointers.find(" ")]).replace("\\","$"), other[0:8], other[9:10], other[11:other.__len__()]))
            all_pointers = all_pointers[all_pointers.find(" ")+17:all_pointers.__len__()]
            self.__cant_pointers -= 1

          words = 0
          self.__cant_pointers= 0

      self.__connect.commit()
      self.__connect.close()

def main():
    p = ParseDataAdv("wordnet.db3","dict/data.adv")
    return 0



if __name__ == '__main__':
    main()

