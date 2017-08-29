'''
@package compoundspectradialog.py

compoundspectradialog.py was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
and is distributed under LGPL version 3

Geneve August 2017
'''

from PyQt5 import *
from PyQt5 import *

from gui_compoundspectra import Ui_CompoundSpectraDialog

class CompoundSpectraDialog(QtWidgets.QDialog, Ui_CompoundSpectraDialog):
    def __init__(self,parent=None):
        QtWidgets.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.closeButton.clicked.connect(self.close_)
        self.okButton.clicked.connect(self.ok_)
        self.okButton.setAutoDefault(True)
        self.okButton.setDefault(True)

    def close_(self):
        self.reject()

    def ok_(self):
        self.accept()

    def setdata(self, name, smiles, precursormz, precursortype, inst, inst_type, ionmode, colenergy, tr, spectra, links):
        self.lineEdit.setText(name)
        self.lineEdit_2.setText(precursormz)
        self.lineEdit_3.setText(precursortype)
        self.lineEdit_4.setText(inst_type)
        self.lineEdit_5.setText(inst)
        self.lineEdit_9.setText(ionmode)
        self.lineEdit_7.setText(colenergy)
        self.lineEdit_8.setText(tr)
        self.lineEdit_6.setText(smiles)
        self.lineEdit_10.setText(links)
        self.textEdit.setText(spectra)

    def getdata(self):
        name = self.lineEdit.text()
        precursormz = self.lineEdit_2.text()
        precursortype = self.lineEdit_3.text()
        inst_type = self.lineEdit_4.text()
        inst =  self.lineEdit_5.text()
        ionmode = self.lineEdit_9.text()
        colenergy = self.lineEdit_7.text()
        tr = self.lineEdit_8.text()
        smiles = self.lineEdit_6.text()
        links = self.lineEdit_10.text()
        spectra = self.textEdit.toPlainText()
        return [name, precursormz, precursortype, inst_type, inst, ionmode, colenergy, tr, smiles ,links, spectra]
