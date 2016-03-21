#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3

class ParseIndexSense():

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

          #print linea[0:linea.find("%")]+"-"+linea[linea.find("%")+1:linea.find(":")]+"-"+linea[linea.find(":")+1:linea.find(":")+3]+"-"+linea[linea.find(":")+4:linea.find(":")+6]+"-"+linea[linea.find(":")+7:linea.find(" ")]
          sequence = linea[linea.find(" ")+1:linea.__len__()]
          #print sequence[0:8]+"-"+sequence[9:10]+"-"+sequence[11:12]
          self.__cursor.execute("INSERT OR REPLACE INTO [index_sense] ([lemma], [ss_type], [lex_filenum], [lex_id], [head_word_id], [synset_offset], [sense_number], [tag_cnt]) VALUES (?,?,?,?,?,?,?,?) ", (linea[0:linea.find("%")], linea[linea.find("%")+1:linea.find(":")], linea[linea.find(":")+1:linea.find(":")+3], linea[linea.find(":")+4:linea.find(":")+6], linea[linea.find(":")+7:linea.find(" ")], sequence[0:8], sequence[9:10], sequence[11:12]))
      self.__connect.commit()
def main():
    p = ParseIndexSense("db/wordnet.db3","dict/index.sense")
    return 0


if __name__ == '__main__':
    main()

