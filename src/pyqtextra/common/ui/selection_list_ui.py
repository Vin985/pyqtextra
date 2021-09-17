# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'selection_list.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

import resources_rc

class Ui_SelectionList(object):
    def setupUi(self, SelectionList):
        if not SelectionList.objectName():
            SelectionList.setObjectName(u"SelectionList")
        SelectionList.resize(548, 444)
        self.horizontalLayout = QHBoxLayout(SelectionList)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.list_src = QListWidget(SelectionList)
        self.list_src.setObjectName(u"list_src")
        self.list_src.setSortingEnabled(True)

        self.horizontalLayout.addWidget(self.list_src)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, -1, 20, -1)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.btn_add = QPushButton(SelectionList)
        self.btn_add.setObjectName(u"btn_add")
        icon = QIcon()
        icon.addFile(u":/icons/right", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_add.setIcon(icon)
        self.btn_add.setFlat(True)

        self.verticalLayout.addWidget(self.btn_add)

        self.btn_remove = QPushButton(SelectionList)
        self.btn_remove.setObjectName(u"btn_remove")
        icon1 = QIcon()
        icon1.addFile(u":/icons/left", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_remove.setIcon(icon1)
        self.btn_remove.setFlat(True)

        self.verticalLayout.addWidget(self.btn_remove)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.list_dest = QListWidget(SelectionList)
        self.list_dest.setObjectName(u"list_dest")
        self.list_dest.setSortingEnabled(True)

        self.horizontalLayout.addWidget(self.list_dest)


        self.retranslateUi(SelectionList)

        QMetaObject.connectSlotsByName(SelectionList)
    # setupUi

    def retranslateUi(self, SelectionList):
        SelectionList.setWindowTitle(QCoreApplication.translate("SelectionList", u"Form", None))
        self.btn_add.setText("")
        self.btn_remove.setText("")
    # retranslateUi

