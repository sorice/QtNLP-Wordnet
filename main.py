#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import QApplication
from ui.QtNLP_Wordnet import Wordnet
#from ui.QtNLP_Wordnet_Editor import WordnetEdit
from ui.QtNLP_Wordnet_UI import Ui_MainWindow
if __name__ == '__main__':
    """Función principal"""
    app = QApplication( sys.argv )
    w = Wordnet()
    w.show()
    sys.exit( app.exec_() )
