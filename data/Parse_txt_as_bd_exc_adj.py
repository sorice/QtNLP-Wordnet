#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3

class ParseExcAdj():

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

      archivo = open(data_to_parse)
      lineas = archivo.readlines()
      archivo.close()

      for linea in lineas:
         inflected = linea[0:linea.find(" ")]
         linea = linea[linea.find(" ")+1:linea.__len__()]
         self.__cursor.execute("INSERT OR REPLACE INTO [adv_exc] ([word_inflected], [base_form]) VALUES (?,?) ", (inflected,linea[0:linea.find(" ")]))
      self.__connect.commit()
      self.__connect.close()
def main():
    p = ParseExcAdj("wordnet.db3","wordnet/adv.exc")
    return 0


if __name__ == '__main__':
    main()

