'''
@package main.py

main.py was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
and is distributed under LGPL version 3

Geneve August 2017
'''

import os
import sys
from pathlib import Path

path = None
try:
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
except NameError:
    path = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))
path += "/msmsspeclib"
if not path in sys.path:
    sys.path.insert(1, path)
del path

from iomsdata import *

from PyQt5 import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.backends.backend_tkagg
import matplotlib.pyplot as plt

import gui_mspfilemanager as mw
from compoundspectradialog import *
from msmscomparissondialog import *

#from aboutdialog import *
from qmodels import *

from math import exp

class MainWindow(QtWidgets.QMainWindow, mw.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.compoundlst = []
        self.lstdatamodel = QtGui.QStandardItemModel(self.listView)
        self.listView.setModel(self.lstdatamodel)
        self.listView.selectionModel().currentChanged.connect(self.updateSpectralView)

        self.addButton.clicked.connect(self.add)
        self.editButton.clicked.connect(self.edit)
        self.removeButton.clicked.connect(self.remove)

        self.zoomButton.clicked.connect(self.zoom)
        self.panButton.clicked.connect(self.pan)
        self.rescaleButton.clicked.connect(self.home)

        # Add plot
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.hide()

        # set the layout
        layout_msspectra = QtWidgets.QVBoxLayout()
        layout_msspectra.addWidget(self.canvas)
        self.groupBox_2.setLayout(layout_msspectra)

        self.tablemodel = TableModel(self)
        self.tableView.setModel(self.tablemodel)
        self.tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #self.tableView.customContextMenuRequested.connect(self.openTableMenu)

        self.actionOpen.triggered.connect(self.open)
        self.actionSave_As.triggered.connect(self.saveas)
        self.actionCompare_two_spectra.triggered.connect(self.twospectracmp)

    def home(self):
        self.toolbar.home()

    def zoom(self):
        self.toolbar.zoom()

    def pan(self):
        self.toolbar.pan()

    def open(self):
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, self.tr('Open file'), str(Path.home()), self.tr("files (*.mgf *.msp)"))
        my_file = Path(fname)
        if my_file.is_file():
            del self.compoundlst[:]
            self.lstdatamodel.clear()
            filename, file_extension = os.path.splitext(fname)
            if file_extension.lower() == ".msp":
                self.compoundlst = readMSP(fname)
            elif file_extension.lower() == ".mgf":
                self.compoundlst = readMGF(fname)
            else:
                return

            if len(self.compoundlst) > 0:
                for i in range(len(self.compoundlst)):
                    self.lstdatamodel.appendRow(QtGui.QStandardItem(self.compoundlst[i].name))

    def saveas(self):
        fname, _ = QtWidgets.QFileDialog.getSaveFileName(self, self.tr('Save file as'), str(Path.home()), self.tr("files (*.mgf *.msp)"))
        if len(fname) > 0:
            filename, file_extension = os.path.splitext(fname)
            writefnc = None
            if file_extension.lower() == ".msp":
                writefnc = writeMSP
            elif file_extension.lower() == ".mgf":
                writefnc = writeMGF
            else:
                return

            for i in range(len(self.compoundlst)):
                m = self.compoundlst[i]
                writefnc(fname, m)

    def twospectracmp(self):
        msmscmp = MSMSComparissonDialog(self.compoundlst)
        if msmscmp.exec_() == 1:
            return
        else:
            return

    def openTableMenu(self, position):
        """ context menu event """
        menu = QtWidgets.QMenu(self)
        exportAction = menu.addAction("Export table as CSV")
        action = menu.exec_(self.tableView.viewport().mapToGlobal(position))
        if action == exportAction:
            fname, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "CSV (*.csv)");
            self.tablemodel.SaveTable(fname)
        else:
            return
        return

    def keyPressEvent(self, e):
        if (e.modifiers() & QtCore.Qt.ControlModifier):
            if e.key() == QtCore.Qt.Key_C: #copy
                if len(self.tableView.selectionModel().selectedIndexes()) > 0:
                    previous = self.tableView.selectionModel().selectedIndexes()[0]
                    columns = []
                    rows = []
                    for index in self.tableView.selectionModel().selectedIndexes():
                        if previous.column() != index.column():
                            columns.append(rows)
                            rows = []
                        rows.append(str(index.data().toPyObject()))
                        previous = index
                    columns.append(rows)

                    # add rows and columns to clipboard
                    clipboard = ""
                    nrows = len(columns[0])
                    ncols = len(columns)
                    for r in xrange(nrows):
                        for c in xrange(ncols):
                            clipboard += columns[c][r]
                            if c != (ncols-1):
                                clipboard += '\t'
                        clipboard += '\n'

                    # copy to the system clipboard
                    sys_clip = QtWidgets.QApplication.clipboard()
                    sys_clip.setText(clipboard)

    def home(self):
        self.toolbar.home()

    def zoom(self):
        self.toolbar.zoom()

    def pan(self):
        self.toolbar.pan()

    def add(self):
        idialog = CompoundSpectraDialog()
        if idialog.exec_() == 1:
            [name, smiles, precmz, prectype, ionmode, tr, inst, insttype, collenergy, biosource, links, txtspectra] = idialog.getdata()
            #convert spectra to float and order by m/z
            spectra = MSMSspectra()
            for line in txtspectra:
                a = nsplit(line.strip())
                if len(a) == 2:
                    spectra.mass.append(float(a[0].replace(",", ".")))
                    spectra.intensity.append(float(a[1].replace(",", ".")))
            spectra.sortMZ()
            self.compoundlst.append(Compound(name, smiles, precmz, ionmode, tr, prectype, inst, insttype, collenergy, biosource, links, spectra))
            self.lstdatamodel.appendRow(QtGui.QStandardItem(name))

    def edit(self):
        indx = self.listView.currentIndex().row()
        idialog = CompoundSpectraDialog()
        idialog.setdata(self.compoundlst[indx].name, self.compoundlst[indx].smiles, self.compoundlst[indx].precmz, self.compoundlst[indx].prectype, self.compoundlst[indx].ionmode,  self.compoundlst[indx].tr, self.compoundlst[indx].inst, self.compoundlst[indx].insttype,  self.compoundlst[indx].collenergy,  self.compoundlst[indx].biosource, self.compoundlst[indx].links, self.compoundlst[indx].spectra.totxt())
        if idialog.exec_() == 1:
            [name, smiles, precmz, prectype, ionmode, tr, inst, insttype, collenergy, biosource, links, txtspectra] = idialog.getdata()
            spectra = MSMSspectra()
            for line in txtspectra:
                a = nsplit(line.strip())
                if len(a) == 2:
                    spectra.mass.append(float(a[0].replace(",", ".")))
                    spectra.intensity.append(float(a[1].replace(",", ".")))
            spectra.sortMZ()
            #update fields
            self.compoundlst[indx].name = name
            self.compoundlst[indx].smiles = smiles
            self.compoundlst[indx].precmz = precmz
            self.compoundlst[indx].prectype = prectype
            self.compoundlst[indx].inst = inst
            self.compoundlst[indx].insttype = insttype
            self.compoundlst[indx].collenergy = collenergy
            self.compoundlst[indx].spectra = spectra
            self.compoundlst[indx].tr = tr
            self.compoundlst[indx].ionmode = ionmode
            self.compoundlst[indx].biosource = biosource
            self.compoundlst[indx].links = links

    def remove(self):
        indx = self.listView.currentIndex().row()
        if indx >= 0 and indx < len(self.compoundlst):
            del self.compoundlst[indx]
            self.lstdatamodel.removeRow(indx)


    def about(self):
        #adialog = AboutDialog()
        #adialog.exec_()
        return

    def quit(self):
        QtWidgets.QApplication.quit()

    def updateSpectralView(self, current, previous):
        ''' plot some random stuff
        print('Row %d selected' % current.row())
        import random
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.plot(data, '*-')
        self.canvas.draw()
        '''
        mol = self.compoundlst[current.row()]
        ax = self.figure.add_subplot(111)
        ax.clear()
        if mol.spectra.signal_size() > 0:
            #width = 1.50  # the width of the bars
            #print("%s %d %f %f" % (mol.name, mol.spectra.signal_size(), mol.spectra.getMZIntensityMax(), mol.spectra.getIntensityMax()))
            width = 2*pow(mol.spectra.getIntensityMax(), -0.05)
            rects1 = ax.bar(mol.spectra.mass, mol.spectra.intensity, width, color='r')
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
            self.updateTableView(current.row())

    def updateTableView(self, indx):
        del self.tablemodel.arraydata[:]
        del self.tablemodel.header[:]
        header = ["Field", "Value"]
        self.tablemodel.setHeader(header)
        m = self.compoundlst[indx]
        self.tablemodel.addRow(["NAME", m.name])
        self.tablemodel.addRow(["PRECURSORMZ", m.precmz])
        self.tablemodel.addRow(["PRECURSORTYPE", m.prectype])
        self.tablemodel.addRow(["INSTRUMENT", m.inst])
        self.tablemodel.addRow(["INSTRUMENTTYPE", m.insttype])
        self.tablemodel.addRow(["SMILES", m.prectype])
        self.tablemodel.addRow(["COLLISIONENERGY", m.collenergy])
        self.tablemodel.addRow(["RETENTIONTIME", m.tr])
        self.tablemodel.addRow(["IONMODE", m.ionmode])
        self.tablemodel.addRow(["BIOLOGICALSOURCE", m.biosource])
        self.tablemodel.addRow(["Links", m.links])
        self.tablemodel.addRow(["Num Peaks", m.spectra.signal_size()])
        return

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
