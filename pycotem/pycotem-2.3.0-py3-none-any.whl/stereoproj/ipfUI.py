# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ipfUI.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_IPF(object):
    def setupUi(self, IPF):
        IPF.setObjectName("IPF")
        IPF.resize(707, 738)
        self.gridLayout_2 = QtWidgets.QGridLayout(IPF)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.mplvl = QtWidgets.QGridLayout()
        self.mplvl.setObjectName("mplvl")
        self.gridLayout_2.addLayout(self.mplvl, 1, 0, 1, 4)
        self.remove_pole_button = QtWidgets.QPushButton(IPF)
        self.remove_pole_button.setObjectName("remove_pole_button")
        self.gridLayout_2.addWidget(self.remove_pole_button, 7, 3, 1, 1)
        self.add_pole_button = QtWidgets.QPushButton(IPF)
        self.add_pole_button.setObjectName("add_pole_button")
        self.gridLayout_2.addWidget(self.add_pole_button, 7, 2, 1, 1)
        self.pole_comboBox = QtWidgets.QComboBox(IPF)
        self.pole_comboBox.setEditable(True)
        self.pole_comboBox.setObjectName("pole_comboBox")
        self.gridLayout_2.addWidget(self.pole_comboBox, 7, 0, 1, 2)
        self.add_plane_button = QtWidgets.QPushButton(IPF)
        self.add_plane_button.setObjectName("add_plane_button")
        self.gridLayout_2.addWidget(self.add_plane_button, 8, 2, 1, 1)
        self.remove_plane_button = QtWidgets.QPushButton(IPF)
        self.remove_plane_button.setObjectName("remove_plane_button")
        self.gridLayout_2.addWidget(self.remove_plane_button, 8, 3, 1, 1)
        self.plane_comboBox = QtWidgets.QComboBox(IPF)
        self.plane_comboBox.setEditable(True)
        self.plane_comboBox.setObjectName("plane_comboBox")
        self.gridLayout_2.addWidget(self.plane_comboBox, 8, 0, 1, 2)
        self.refresh_Button = QtWidgets.QPushButton(IPF)
        self.refresh_Button.setObjectName("refresh_Button")
        self.gridLayout_2.addWidget(self.refresh_Button, 6, 2, 1, 1)
        self.draw_button = QtWidgets.QPushButton(IPF)
        self.draw_button.setObjectName("draw_button")
        self.gridLayout_2.addWidget(self.draw_button, 6, 0, 1, 2)
        self.Show_label_checkBox = QtWidgets.QCheckBox(IPF)
        self.Show_label_checkBox.setObjectName("Show_label_checkBox")
        self.gridLayout_2.addWidget(self.Show_label_checkBox, 6, 3, 1, 1)
        self.blue_Button = QtWidgets.QRadioButton(IPF)
        self.blue_Button.setObjectName("blue_Button")
        self.gridLayout_2.addWidget(self.blue_Button, 9, 0, 1, 1)
        self.red_Button = QtWidgets.QRadioButton(IPF)
        self.red_Button.setObjectName("red_Button")
        self.gridLayout_2.addWidget(self.red_Button, 9, 1, 1, 1)
        self.green_Button = QtWidgets.QRadioButton(IPF)
        self.green_Button.setObjectName("green_Button")
        self.gridLayout_2.addWidget(self.green_Button, 9, 2, 1, 1)

        self.retranslateUi(IPF)
        QtCore.QMetaObject.connectSlotsByName(IPF)
        IPF.setTabOrder(self.draw_button, self.refresh_Button)
        IPF.setTabOrder(self.refresh_Button, self.Show_label_checkBox)
        IPF.setTabOrder(self.Show_label_checkBox, self.pole_comboBox)
        IPF.setTabOrder(self.pole_comboBox, self.add_pole_button)
        IPF.setTabOrder(self.add_pole_button, self.remove_pole_button)
        IPF.setTabOrder(self.remove_pole_button, self.plane_comboBox)
        IPF.setTabOrder(self.plane_comboBox, self.add_plane_button)
        IPF.setTabOrder(self.add_plane_button, self.remove_plane_button)
        IPF.setTabOrder(self.remove_plane_button, self.blue_Button)
        IPF.setTabOrder(self.blue_Button, self.red_Button)
        IPF.setTabOrder(self.red_Button, self.green_Button)

    def retranslateUi(self, IPF):
        _translate = QtCore.QCoreApplication.translate
        IPF.setWindowTitle(_translate("IPF", "IPF"))
        self.remove_pole_button.setText(_translate("IPF", "Remove Pole"))
        self.add_pole_button.setText(_translate("IPF", "Add Pole"))
        self.add_plane_button.setText(_translate("IPF", "Add Plane"))
        self.remove_plane_button.setText(_translate("IPF", "Remove Plane"))
        self.refresh_Button.setText(_translate("IPF", "Refresh view"))
        self.draw_button.setText(_translate("IPF", "Draw Standard Triangle"))
        self.Show_label_checkBox.setText(_translate("IPF", "Show labels"))
        self.blue_Button.setText(_translate("IPF", "Blue"))
        self.red_Button.setText(_translate("IPF", "Red"))
        self.green_Button.setText(_translate("IPF", "Green"))

