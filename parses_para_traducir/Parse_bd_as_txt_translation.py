#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3

class ParseTraslation():
    """
    Clase del Analizador de los datos de los adjetivos de Wordnet 3.0
    :param target_sqlite_db: ruta + nombre de la BD sqlite donde se escribirán los datos.
    :param type: str
    :rtype: 0



    """

    def __init__( self, target_sqlite_db):
      self.__connect = sqlite3.connect(target_sqlite_db)
      self.__cursor = self.__connect.cursor()

      str = "SELECT [lemma] FROM [index_sense]"
      self.__cursor.execute(unicode(str))
      result = self.__cursor.fetchall()
      palabras = open("index_sense_ing_lemma.txt","w")

      for r in result:
         palabras.write(r[0]+"\n")
         #if(r[0]=="not"):
         # palabras.write("\n")






      self.__connect.commit()
      self.__connect.close()

def main():
    p = ParseTraslation("data/wordnet.db3")
    return 0


if __name__ == '__main__':
    main()

