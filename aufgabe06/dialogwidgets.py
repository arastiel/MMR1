import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc


class Help(qw.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hilfe zum Spiel")
        self.resize(1000, 550)
        self.setWindowModality(qc.Qt.ApplicationModal)

        hilfetext = qw.QTextBrowser()
        hilfetext.setSource(qc.QUrl("spielanleitung.html"))

        vbox = qw.QVBoxLayout()
        vbox.addWidget(hilfetext)
        self.setLayout(vbox)