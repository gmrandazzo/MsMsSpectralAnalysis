'''
@package msmscmp.py

compoundspectradialog.py was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
and is distributed under LGPL version 3

Geneve August 2017
'''

from PyQt5 import *
from PyQt5 import *
from gui_msmscomparissondialog import Ui_MSMSComparissonDialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.backends.backend_tkagg
import matplotlib.pyplot as plt


import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from msmsspeclib.iomsdata import *
from msmsspeclib.MSMSVectorSpace import *

class MSMSComparissonDialog(QtWidgets.QDialog, Ui_MSMSComparissonDialog):
    def __init__(self, compoundlst, parent=None):
        QtWidgets.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.compoundlst = compoundlst
        self.closeButton.clicked.connect(self.close_)
        self.closeButton.setAutoDefault(True)
        self.label.setText("Similarity score: 1.00")
        self.lstdatamodel1 = QtGui.QStandardItemModel(self.listView)
        self.listView.setModel(self.lstdatamodel1)
        self.listView.selectionModel().selectionChanged.connect(self.updateSpectralView)
        self.lstdatamodel2 = QtGui.QStandardItemModel(self.listView_2)
        self.listView_2.setModel(self.lstdatamodel2)
        self.listView_2.selectionModel().selectionChanged.connect(self.updateSpectralView)
        self.doubleSpinBox.valueChanged.connect(self.updateSpectralView)

        for i in range(len(self.compoundlst)):
            self.lstdatamodel1.appendRow(QtGui.QStandardItem(self.compoundlst[i].name))
            self.lstdatamodel2.appendRow(QtGui.QStandardItem(self.compoundlst[i].name))

        # Add plot
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.hide()

        # set the layout
        layout_msspectra = QtWidgets.QVBoxLayout()
        layout_msspectra.addWidget(self.canvas)
        self.groupBox_2.setLayout(layout_msspectra)


    def close_(self):
        self.reject()

    def setsimilarity(self, cosine_similarity):
        self.label.setText("Similarity score: %.2f" % (round(cosine_similarity)))

    def updateSpectralView(self):
        if len(self.listView.selectedIndexes()) > 0 and len(self.listView_2.selectedIndexes()) > 0:
            mol1 = self.compoundlst[self.listView.selectedIndexes()[0].row()]
            mol2 = self.compoundlst[self.listView_2.selectedIndexes()[0].row()]

            filter = self.doubleSpinBox.value()/100.
            spectra1 = spectraconvert(mol1.spectra, filter)
            spectra2 = spectraconvert(mol2.spectra, filter)

            msmscmp = MSMSVectorSpace(5.0)

            vfp = []
            msmscmp.FPMassVector(vfp, spectra1)
            msmscmp.FPMassVector(vfp, spectra2)
            vfp.sort()

            fp1 = msmscmp.genGlobalMSMSFingerprint(vfp, spectra1)
            fp2 = msmscmp.genGlobalMSMSFingerprint(vfp, spectra2)

            similarity = msmscmp.cosine_similarity(fp1, fp2)

            self.label.setText("Spectral similarity: %.2f" % (similarity))

            #width = 0.30       # the width of the bars
            width1 = 2*pow(spectra1.getIntensityMax(), -0.05)
            width2 = 2*pow(spectra2.getIntensityMax(), -0.05)

            width = 0.3
            if width1 > width2:
                width = width2
            else:
                width = width1

            ax = self.figure.add_subplot(111)
            ax.clear()

            rects1 = ax.bar(spectra1.mass, spectra1.intensity, width, color='r')
            for i in range(spectra2.signal_size()):
                spectra2.intensity[i] *= -1

            rects2 = ax.bar(spectra2.mass, spectra2.intensity, width, color='g')
            ax.set_ylabel('intensity')
            #ax.legend( (rects1[0], rects2[0], rects3[0]), ('y', 'z', 'k') )

            def autolabel(rects):
                for rect in rects:
                    h = rect.get_height()
                    ax.text(rect.get_x()+rect.get_width()/2., 1.05*h, '%d'%int(h),
                            ha='center', va='bottom')

            #autolabel(rects1)
            #autolabel(rects2)
            self.canvas.draw()
            return
