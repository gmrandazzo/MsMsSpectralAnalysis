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

    def setdata(self, name, smiles, precmz, prectype, ionmode, tr, inst, insttype, collenergy, biosource, links, spectra):
        self.lineEdit.setText(name)
        self.lineEdit_2.setText(precmz)
        self.lineEdit_3.setText(prectype)
        self.lineEdit_4.setText(insttype)
        self.lineEdit_5.setText(inst)
        self.lineEdit_9.setText(ionmode)
        self.lineEdit_7.setText(collenergy)
        self.lineEdit_8.setText(tr)
        self.lineEdit_6.setText(smiles)
        self.lineEdit_11.setText(biosource)
        self.lineEdit_10.setText(links)
        self.textEdit.setText(spectra)

    def getdata(self):
        name = self.lineEdit.text()
        precmz = self.lineEdit_2.text()
        prectype = self.lineEdit_3.text()
        insttype = self.lineEdit_4.text()
        inst =  self.lineEdit_5.text()
        ionmode = self.lineEdit_9.text()
        collenergy = self.lineEdit_7.text()
        tr = self.lineEdit_8.text()
        smiles = self.lineEdit_6.text()
        biosource = self.lineEdit_11.text()
        links = self.lineEdit_10.text()
        txtspectra = self.textEdit.toPlainText()
        return [name, smiles, precmz, prectype, ionmode, tr, inst, insttype, collenergy, biosource, links, txtspectra]
