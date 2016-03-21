#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3

class ParseExcNoun():

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
         cant = 1
         inflected = linea[0:linea.find(" ")]
         self.__cursor.execute("INSERT OR REPLACE INTO [noun_exc] ([word_inflected], [cant_base_forms]) VALUES (?,?) ", (inflected,0))
         linea = linea[linea.find(" ")+1:linea.__len__()]
         while(linea.find(" ")!=-1):
          cant += 1
          #print linea[0:linea.find(" ")]
          self.__cursor.execute("INSERT OR REPLACE INTO [noun_exc_base_forms] ([word_inflected], [base_form]) VALUES (?,?) ", (inflected, linea[0:linea.find(" ")]))
          linea = linea[linea.find(" ")+1:linea.__len__()]
        #print linea
         self.__cursor.execute("INSERT OR REPLACE INTO [noun_exc_base_forms] ([word_inflected], [base_form]) VALUES (?,?) ", (inflected, linea))
         self.__cursor.execute("UPDATE [noun_exc] SET [cant_base_forms]=? WHERE [word_inflected]=?", (cant, inflected))
      self.__connect.commit()
      self.__connect.close()
def main():
    p = ParseExcNoun("db/wordnet.db3","dict/noun.exc")
    return 0


if __name__ == '__main__':
    main()

