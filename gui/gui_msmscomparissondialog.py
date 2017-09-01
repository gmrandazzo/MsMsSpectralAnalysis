# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'msmscomparissondialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MSMSComparissonDialog(object):
    def setupUi(self, MSMSComparissonDialog):
        MSMSComparissonDialog.setObjectName("MSMSComparissonDialog")
        MSMSComparissonDialog.resize(706, 714)
        self.gridLayout_2 = QtWidgets.QGridLayout(MSMSComparissonDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(47, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(MSMSComparissonDialog)
        self.groupBox.setMaximumSize(QtCore.QSize(550, 240))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.listView = QtWidgets.QListView(self.groupBox)
        self.listView.setObjectName("listView")
        self.gridLayout.addWidget(self.listView, 0, 0, 1, 2)
        self.listView_2 = QtWidgets.QListView(self.groupBox)
        self.listView_2.setObjectName("listView_2")
        self.gridLayout.addWidget(self.listView_2, 0, 2, 1, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox.setProperty("value", 1.0)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.horizontalLayout.addWidget(self.doubleSpinBox)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 4)
        spacerItem3 = QtWidgets.QSpacerItem(173, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setMaximumSize(QtCore.QSize(150, 20))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 1, 1, 2)
        spacerItem4 = QtWidgets.QSpacerItem(176, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 2, 3, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(67, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem5, 0, 2, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(MSMSComparissonDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2.addWidget(self.groupBox_2, 1, 0, 1, 3)
        spacerItem6 = QtWidgets.QSpacerItem(460, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem6, 2, 0, 1, 2)
        self.closeButton = QtWidgets.QPushButton(MSMSComparissonDialog)
        self.closeButton.setObjectName("closeButton")
        self.gridLayout_2.addWidget(self.closeButton, 2, 2, 1, 1)

        self.retranslateUi(MSMSComparissonDialog)
        QtCore.QMetaObject.connectSlotsByName(MSMSComparissonDialog)

    def retranslateUi(self, MSMSComparissonDialog):
        _translate = QtCore.QCoreApplication.translate
        MSMSComparissonDialog.setWindowTitle(_translate("MSMSComparissonDialog", "MS MS Spectra Comparisson"))
        self.groupBox.setTitle(_translate("MSMSComparissonDialog", "Compound selection"))
        self.label_2.setText(_translate("MSMSComparissonDialog", "Remove signal less than "))
        self.label_3.setText(_translate("MSMSComparissonDialog", "%"))
        self.label.setText(_translate("MSMSComparissonDialog", "Similarity score: 1.00"))
        self.groupBox_2.setTitle(_translate("MSMSComparissonDialog", "Spectral view"))
        self.closeButton.setText(_translate("MSMSComparissonDialog", "Close"))

