# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'metadata_generator.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateEdit,
    QFormLayout, QGraphicsView, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QListView, QMainWindow, QMenuBar, QPushButton,
    QRadioButton, QSizePolicy, QSpinBox, QStatusBar,
    QTabWidget, QTableView, QTextBrowser, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(709, 865)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_22 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.tabs = QTabWidget(self.centralwidget)
        self.tabs.setObjectName(u"tabs")
        self.tab_ExpInfo = QWidget()
        self.tab_ExpInfo.setObjectName(u"tab_ExpInfo")
        self.verticalLayout_2 = QVBoxLayout(self.tab_ExpInfo)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.groupBox_display = QGroupBox(self.tab_ExpInfo)
        self.groupBox_display.setObjectName(u"groupBox_display")
        self.gridLayout_3 = QGridLayout(self.groupBox_display)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_29 = QLabel(self.groupBox_display)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout_3.addWidget(self.label_29, 0, 1, 1, 1)

        self.label_26 = QLabel(self.groupBox_display)
        self.label_26.setObjectName(u"label_26")

        self.gridLayout_3.addWidget(self.label_26, 2, 0, 1, 1)

        self.label_28 = QLabel(self.groupBox_display)
        self.label_28.setObjectName(u"label_28")

        self.gridLayout_3.addWidget(self.label_28, 0, 0, 1, 1)

        self.label_27 = QLabel(self.groupBox_display)
        self.label_27.setObjectName(u"label_27")

        self.gridLayout_3.addWidget(self.label_27, 2, 1, 1, 1)

        self.label_25 = QLabel(self.groupBox_display)
        self.label_25.setObjectName(u"label_25")

        self.gridLayout_3.addWidget(self.label_25, 1, 1, 1, 1)

        self.label_10 = QLabel(self.groupBox_display)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_3.addWidget(self.label_10, 1, 0, 1, 1)


        self.horizontalLayout_3.addWidget(self.groupBox_display)

        self.groupBox_fileIO = QGroupBox(self.tab_ExpInfo)
        self.groupBox_fileIO.setObjectName(u"groupBox_fileIO")
        self.verticalLayout_17 = QVBoxLayout(self.groupBox_fileIO)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.comboBox_9 = QComboBox(self.groupBox_fileIO)
        self.comboBox_9.setObjectName(u"comboBox_9")

        self.verticalLayout_17.addWidget(self.comboBox_9)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.pushButton_3 = QPushButton(self.groupBox_fileIO)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.gridLayout_4.addWidget(self.pushButton_3, 0, 1, 1, 1)

        self.pushButton_2 = QPushButton(self.groupBox_fileIO)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout_4.addWidget(self.pushButton_2, 0, 0, 1, 1)

        self.pushButton_4 = QPushButton(self.groupBox_fileIO)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.gridLayout_4.addWidget(self.pushButton_4, 1, 0, 1, 1)

        self.pushButton = QPushButton(self.groupBox_fileIO)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout_4.addWidget(self.pushButton, 1, 1, 1, 1)


        self.verticalLayout_17.addLayout(self.gridLayout_4)


        self.horizontalLayout_3.addWidget(self.groupBox_fileIO)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.groupBox_animals = QGroupBox(self.tab_ExpInfo)
        self.groupBox_animals.setObjectName(u"groupBox_animals")
        self.verticalLayout_12 = QVBoxLayout(self.groupBox_animals)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_3 = QLabel(self.groupBox_animals)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_3)

        self.lineEdit_animalID = QLineEdit(self.groupBox_animals)
        self.lineEdit_animalID.setObjectName(u"lineEdit_animalID")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.lineEdit_animalID)

        self.label_4 = QLabel(self.groupBox_animals)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_4)

        self.comboBox_Species = QComboBox(self.groupBox_animals)
        self.comboBox_Species.setObjectName(u"comboBox_Species")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.comboBox_Species)

        self.label_6 = QLabel(self.groupBox_animals)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_6)

        self.comboBox_Genotype = QComboBox(self.groupBox_animals)
        self.comboBox_Genotype.setObjectName(u"comboBox_Genotype")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.comboBox_Genotype)

        self.label_7 = QLabel(self.groupBox_animals)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_7)

        self.comboBox_4 = QComboBox(self.groupBox_animals)
        self.comboBox_4.setObjectName(u"comboBox_4")

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.comboBox_4)

        self.label_8 = QLabel(self.groupBox_animals)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.label_8)

        self.dateEdit_DOB = QDateEdit(self.groupBox_animals)
        self.dateEdit_DOB.setObjectName(u"dateEdit_DOB")

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.dateEdit_DOB)

        self.label_9 = QLabel(self.groupBox_animals)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.label_9)

        self.dateEdit_DOI = QDateEdit(self.groupBox_animals)
        self.dateEdit_DOI.setObjectName(u"dateEdit_DOI")

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.dateEdit_DOI)


        self.verticalLayout_12.addLayout(self.formLayout_2)


        self.gridLayout_2.addWidget(self.groupBox_animals, 0, 1, 1, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox_basics = QGroupBox(self.tab_ExpInfo)
        self.groupBox_basics.setObjectName(u"groupBox_basics")
        self.groupBox_basics.setEnabled(True)
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_basics)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.groupBox_basics)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.dateEdit_DOR = QDateEdit(self.groupBox_basics)
        self.dateEdit_DOR.setObjectName(u"dateEdit_DOR")
        self.dateEdit_DOR.setCalendarPopup(True)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.dateEdit_DOR)

        self.label_2 = QLabel(self.groupBox_basics)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.lineEdit_experimenters = QLineEdit(self.groupBox_basics)
        self.lineEdit_experimenters.setObjectName(u"lineEdit_experimenters")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_experimenters)

        self.label_5 = QLabel(self.groupBox_basics)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.comboBox_ACUC = QComboBox(self.groupBox_basics)
        self.comboBox_ACUC.setObjectName(u"comboBox_ACUC")

        self.horizontalLayout.addWidget(self.comboBox_ACUC)

        self.btn_add_ACUC_PN = QPushButton(self.groupBox_basics)
        self.btn_add_ACUC_PN.setObjectName(u"btn_add_ACUC_PN")
        self.btn_add_ACUC_PN.setMaximumSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.btn_add_ACUC_PN)

        self.btn_rm_ACUC_PN = QPushButton(self.groupBox_basics)
        self.btn_rm_ACUC_PN.setObjectName(u"btn_rm_ACUC_PN")
        self.btn_rm_ACUC_PN.setMaximumSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.btn_rm_ACUC_PN)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout)


        self.verticalLayout_9.addLayout(self.formLayout)


        self.verticalLayout_4.addWidget(self.groupBox_basics)

        self.groupBox_solutions = QGroupBox(self.tab_ExpInfo)
        self.groupBox_solutions.setObjectName(u"groupBox_solutions")
        self.formLayout_8 = QFormLayout(self.groupBox_solutions)
        self.formLayout_8.setObjectName(u"formLayout_8")
        self.label_30 = QLabel(self.groupBox_solutions)
        self.label_30.setObjectName(u"label_30")

        self.formLayout_8.setWidget(0, QFormLayout.LabelRole, self.label_30)

        self.lineEdit_CuttingOS = QLineEdit(self.groupBox_solutions)
        self.lineEdit_CuttingOS.setObjectName(u"lineEdit_CuttingOS")

        self.formLayout_8.setWidget(0, QFormLayout.FieldRole, self.lineEdit_CuttingOS)

        self.label_31 = QLabel(self.groupBox_solutions)
        self.label_31.setObjectName(u"label_31")

        self.formLayout_8.setWidget(2, QFormLayout.LabelRole, self.label_31)

        self.lineEdit_HoldingOS = QLineEdit(self.groupBox_solutions)
        self.lineEdit_HoldingOS.setObjectName(u"lineEdit_HoldingOS")

        self.formLayout_8.setWidget(2, QFormLayout.FieldRole, self.lineEdit_HoldingOS)

        self.label_32 = QLabel(self.groupBox_solutions)
        self.label_32.setObjectName(u"label_32")

        self.formLayout_8.setWidget(4, QFormLayout.LabelRole, self.label_32)

        self.lineEdit_RecordOS = QLineEdit(self.groupBox_solutions)
        self.lineEdit_RecordOS.setObjectName(u"lineEdit_RecordOS")

        self.formLayout_8.setWidget(4, QFormLayout.FieldRole, self.lineEdit_RecordOS)


        self.verticalLayout_4.addWidget(self.groupBox_solutions)


        self.gridLayout_2.addLayout(self.verticalLayout_4, 0, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_2)

        self.groupBox_injections = QGroupBox(self.tab_ExpInfo)
        self.groupBox_injections.setObjectName(u"groupBox_injections")
        self.verticalLayout = QVBoxLayout(self.groupBox_injections)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_33 = QLabel(self.groupBox_injections)
        self.label_33.setObjectName(u"label_33")

        self.horizontalLayout_15.addWidget(self.label_33)

        self.checkBox_hemisphere_R = QCheckBox(self.groupBox_injections)
        self.checkBox_hemisphere_R.setObjectName(u"checkBox_hemisphere_R")

        self.horizontalLayout_15.addWidget(self.checkBox_hemisphere_R)

        self.checkBox_hemisphere_L = QCheckBox(self.groupBox_injections)
        self.checkBox_hemisphere_L.setObjectName(u"checkBox_hemisphere_L")

        self.horizontalLayout_15.addWidget(self.checkBox_hemisphere_L)

        self.lineEdit_targetArea = QLineEdit(self.groupBox_injections)
        self.lineEdit_targetArea.setObjectName(u"lineEdit_targetArea")

        self.horizontalLayout_15.addWidget(self.lineEdit_targetArea)


        self.verticalLayout.addLayout(self.horizontalLayout_15)

        self.groupBox_2 = QGroupBox(self.groupBox_injections)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.formLayout_5 = QFormLayout(self.groupBox_2)
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_5.setWidget(0, QFormLayout.LabelRole, self.label_11)

        self.label_17 = QLabel(self.groupBox_2)
        self.label_17.setObjectName(u"label_17")

        self.formLayout_5.setWidget(1, QFormLayout.LabelRole, self.label_17)

        self.comboBox_injectionMode_R = QComboBox(self.groupBox_2)
        self.comboBox_injectionMode_R.setObjectName(u"comboBox_injectionMode_R")

        self.formLayout_5.setWidget(1, QFormLayout.FieldRole, self.comboBox_injectionMode_R)

        self.label_12 = QLabel(self.groupBox_2)
        self.label_12.setObjectName(u"label_12")

        self.formLayout_5.setWidget(2, QFormLayout.LabelRole, self.label_12)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_13 = QLabel(self.groupBox_2)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_12.addWidget(self.label_13)

        self.lineEdit_Coord_DV_R = QLineEdit(self.groupBox_2)
        self.lineEdit_Coord_DV_R.setObjectName(u"lineEdit_Coord_DV_R")

        self.horizontalLayout_12.addWidget(self.lineEdit_Coord_DV_R)

        self.label_14 = QLabel(self.groupBox_2)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_12.addWidget(self.label_14)

        self.lineEdit_Coord_ML_R = QLineEdit(self.groupBox_2)
        self.lineEdit_Coord_ML_R.setObjectName(u"lineEdit_Coord_ML_R")

        self.horizontalLayout_12.addWidget(self.lineEdit_Coord_ML_R)

        self.label_15 = QLabel(self.groupBox_2)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_12.addWidget(self.label_15)

        self.lineEdit_Coord_AP_R = QLineEdit(self.groupBox_2)
        self.lineEdit_Coord_AP_R.setObjectName(u"lineEdit_Coord_AP_R")

        self.horizontalLayout_12.addWidget(self.lineEdit_Coord_AP_R)


        self.formLayout_5.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_12)

        self.label_16 = QLabel(self.groupBox_2)
        self.label_16.setObjectName(u"label_16")

        self.formLayout_5.setWidget(3, QFormLayout.LabelRole, self.label_16)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.comboBox_virus_R = QComboBox(self.groupBox_2)
        self.comboBox_virus_R.setObjectName(u"comboBox_virus_R")
        self.comboBox_virus_R.setEnabled(True)
        font = QFont()
        font.setKerning(True)
        self.comboBox_virus_R.setFont(font)
        self.comboBox_virus_R.setEditable(False)

        self.horizontalLayout_2.addWidget(self.comboBox_virus_R)

        self.btn_add_virus_R = QPushButton(self.groupBox_2)
        self.btn_add_virus_R.setObjectName(u"btn_add_virus_R")
        self.btn_add_virus_R.setMaximumSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.btn_add_virus_R)

        self.btn_rm_virus_R = QPushButton(self.groupBox_2)
        self.btn_rm_virus_R.setObjectName(u"btn_rm_virus_R")
        self.btn_rm_virus_R.setMaximumSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.btn_rm_virus_R)


        self.formLayout_5.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.lineEdit_volume_R = QLineEdit(self.groupBox_2)
        self.lineEdit_volume_R.setObjectName(u"lineEdit_volume_R")

        self.horizontalLayout_7.addWidget(self.lineEdit_volume_R)

        self.comboBox_volumeUnit_R = QComboBox(self.groupBox_2)
        self.comboBox_volumeUnit_R.setObjectName(u"comboBox_volumeUnit_R")

        self.horizontalLayout_7.addWidget(self.comboBox_volumeUnit_R)


        self.formLayout_5.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_7)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self.groupBox_injections)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout_3 = QFormLayout(self.groupBox)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label_18 = QLabel(self.groupBox)
        self.label_18.setObjectName(u"label_18")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_18)

        self.label_24 = QLabel(self.groupBox)
        self.label_24.setObjectName(u"label_24")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_24)

        self.label_19 = QLabel(self.groupBox)
        self.label_19.setObjectName(u"label_19")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.label_19)

        self.label_23 = QLabel(self.groupBox)
        self.label_23.setObjectName(u"label_23")

        self.formLayout_3.setWidget(3, QFormLayout.LabelRole, self.label_23)

        self.comboBox_injectionMode_L = QComboBox(self.groupBox)
        self.comboBox_injectionMode_L.setObjectName(u"comboBox_injectionMode_L")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.comboBox_injectionMode_L)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_20 = QLabel(self.groupBox)
        self.label_20.setObjectName(u"label_20")

        self.horizontalLayout_13.addWidget(self.label_20)

        self.lineEdit_Coord_DV_L = QLineEdit(self.groupBox)
        self.lineEdit_Coord_DV_L.setObjectName(u"lineEdit_Coord_DV_L")

        self.horizontalLayout_13.addWidget(self.lineEdit_Coord_DV_L)

        self.label_21 = QLabel(self.groupBox)
        self.label_21.setObjectName(u"label_21")

        self.horizontalLayout_13.addWidget(self.label_21)

        self.lineEdit_Coord_ML_L = QLineEdit(self.groupBox)
        self.lineEdit_Coord_ML_L.setObjectName(u"lineEdit_Coord_ML_L")

        self.horizontalLayout_13.addWidget(self.lineEdit_Coord_ML_L)

        self.label_22 = QLabel(self.groupBox)
        self.label_22.setObjectName(u"label_22")

        self.horizontalLayout_13.addWidget(self.label_22)

        self.lineEdit_Coord_AP_L = QLineEdit(self.groupBox)
        self.lineEdit_Coord_AP_L.setObjectName(u"lineEdit_Coord_AP_L")

        self.horizontalLayout_13.addWidget(self.lineEdit_Coord_AP_L)


        self.formLayout_3.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_13)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.comboBox_virus_L = QComboBox(self.groupBox)
        self.comboBox_virus_L.setObjectName(u"comboBox_virus_L")

        self.horizontalLayout_4.addWidget(self.comboBox_virus_L)

        self.btn_add_virus_L = QPushButton(self.groupBox)
        self.btn_add_virus_L.setObjectName(u"btn_add_virus_L")
        self.btn_add_virus_L.setMaximumSize(QSize(20, 20))

        self.horizontalLayout_4.addWidget(self.btn_add_virus_L)

        self.btn_rm_virus_L = QPushButton(self.groupBox)
        self.btn_rm_virus_L.setObjectName(u"btn_rm_virus_L")
        self.btn_rm_virus_L.setMaximumSize(QSize(20, 20))

        self.horizontalLayout_4.addWidget(self.btn_rm_virus_L)


        self.formLayout_3.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_4)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.lineEdit_volume_L = QLineEdit(self.groupBox)
        self.lineEdit_volume_L.setObjectName(u"lineEdit_volume_L")

        self.horizontalLayout_9.addWidget(self.lineEdit_volume_L)

        self.comboBox_volumeUnit_L = QComboBox(self.groupBox)
        self.comboBox_volumeUnit_L.setObjectName(u"comboBox_volumeUnit_L")

        self.horizontalLayout_9.addWidget(self.comboBox_volumeUnit_L)


        self.formLayout_3.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_9)


        self.verticalLayout.addWidget(self.groupBox)


        self.verticalLayout_2.addWidget(self.groupBox_injections)

        self.tabs.addTab(self.tab_ExpInfo, "")
        self.tab_RecTagger = QWidget()
        self.tab_RecTagger.setObjectName(u"tab_RecTagger")
        self.horizontalLayout_23 = QHBoxLayout(self.tab_RecTagger)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBox_recBasic = QGroupBox(self.tab_RecTagger)
        self.groupBox_recBasic.setObjectName(u"groupBox_recBasic")
        self.formLayout_6 = QFormLayout(self.groupBox_recBasic)
        self.formLayout_6.setObjectName(u"formLayout_6")
        self.lbl_OBJ = QLabel(self.groupBox_recBasic)
        self.lbl_OBJ.setObjectName(u"lbl_OBJ")

        self.formLayout_6.setWidget(0, QFormLayout.LabelRole, self.lbl_OBJ)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.radioBtn_10X = QRadioButton(self.groupBox_recBasic)
        self.radioBtn_10X.setObjectName(u"radioBtn_10X")

        self.horizontalLayout_16.addWidget(self.radioBtn_10X)

        self.radioBtn_40X = QRadioButton(self.groupBox_recBasic)
        self.radioBtn_40X.setObjectName(u"radioBtn_40X")

        self.horizontalLayout_16.addWidget(self.radioBtn_40X)

        self.radioBtn_60X = QRadioButton(self.groupBox_recBasic)
        self.radioBtn_60X.setObjectName(u"radioBtn_60X")

        self.horizontalLayout_16.addWidget(self.radioBtn_60X)


        self.formLayout_6.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_16)

        self.lbl_EXC = QLabel(self.groupBox_recBasic)
        self.lbl_EXC.setObjectName(u"lbl_EXC")

        self.formLayout_6.setWidget(1, QFormLayout.LabelRole, self.lbl_EXC)

        self.comboBox_EXC = QComboBox(self.groupBox_recBasic)
        self.comboBox_EXC.setObjectName(u"comboBox_EXC")

        self.formLayout_6.setWidget(1, QFormLayout.FieldRole, self.comboBox_EXC)

        self.lbl_LEVEL = QLabel(self.groupBox_recBasic)
        self.lbl_LEVEL.setObjectName(u"lbl_LEVEL")

        self.formLayout_6.setWidget(2, QFormLayout.LabelRole, self.lbl_LEVEL)

        self.lineEdit_LEVEL = QLineEdit(self.groupBox_recBasic)
        self.lineEdit_LEVEL.setObjectName(u"lineEdit_LEVEL")

        self.formLayout_6.setWidget(2, QFormLayout.FieldRole, self.lineEdit_LEVEL)

        self.lbl_EXPO = QLabel(self.groupBox_recBasic)
        self.lbl_EXPO.setObjectName(u"lbl_EXPO")

        self.formLayout_6.setWidget(3, QFormLayout.LabelRole, self.lbl_EXPO)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.lineEdit_EXPO = QLineEdit(self.groupBox_recBasic)
        self.lineEdit_EXPO.setObjectName(u"lineEdit_EXPO")

        self.horizontalLayout_17.addWidget(self.lineEdit_EXPO)

        self.comboBox_EXPO_UNITS = QComboBox(self.groupBox_recBasic)
        self.comboBox_EXPO_UNITS.setObjectName(u"comboBox_EXPO_UNITS")

        self.horizontalLayout_17.addWidget(self.comboBox_EXPO_UNITS)


        self.formLayout_6.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_17)

        self.lbl_EMI = QLabel(self.groupBox_recBasic)
        self.lbl_EMI.setObjectName(u"lbl_EMI")

        self.formLayout_6.setWidget(4, QFormLayout.LabelRole, self.lbl_EMI)

        self.comboBox_EMI = QComboBox(self.groupBox_recBasic)
        self.comboBox_EMI.setObjectName(u"comboBox_EMI")

        self.formLayout_6.setWidget(4, QFormLayout.FieldRole, self.comboBox_EMI)

        self.lbl_FRAMES = QLabel(self.groupBox_recBasic)
        self.lbl_FRAMES.setObjectName(u"lbl_FRAMES")

        self.formLayout_6.setWidget(5, QFormLayout.LabelRole, self.lbl_FRAMES)

        self.lineEdit_FRAMES = QLineEdit(self.groupBox_recBasic)
        self.lineEdit_FRAMES.setObjectName(u"lineEdit_FRAMES")

        self.formLayout_6.setWidget(5, QFormLayout.FieldRole, self.lineEdit_FRAMES)

        self.lbl_FPS = QLabel(self.groupBox_recBasic)
        self.lbl_FPS.setObjectName(u"lbl_FPS")

        self.formLayout_6.setWidget(6, QFormLayout.LabelRole, self.lbl_FPS)

        self.lineEdit_FPS = QLineEdit(self.groupBox_recBasic)
        self.lineEdit_FPS.setObjectName(u"lineEdit_FPS")

        self.formLayout_6.setWidget(6, QFormLayout.FieldRole, self.lineEdit_FPS)

        self.lbl_CAM_TRIG_MODE = QLabel(self.groupBox_recBasic)
        self.lbl_CAM_TRIG_MODE.setObjectName(u"lbl_CAM_TRIG_MODE")

        self.formLayout_6.setWidget(7, QFormLayout.LabelRole, self.lbl_CAM_TRIG_MODE)

        self.comboBox_CAM_TRIG_MODES = QComboBox(self.groupBox_recBasic)
        self.comboBox_CAM_TRIG_MODES.setObjectName(u"comboBox_CAM_TRIG_MODES")

        self.formLayout_6.setWidget(7, QFormLayout.FieldRole, self.comboBox_CAM_TRIG_MODES)

        self.lbl_SLICE = QLabel(self.groupBox_recBasic)
        self.lbl_SLICE.setObjectName(u"lbl_SLICE")

        self.formLayout_6.setWidget(8, QFormLayout.LabelRole, self.lbl_SLICE)

        self.spinBox_SLICE = QSpinBox(self.groupBox_recBasic)
        self.spinBox_SLICE.setObjectName(u"spinBox_SLICE")

        self.formLayout_6.setWidget(8, QFormLayout.FieldRole, self.spinBox_SLICE)

        self.lbl_AT = QLabel(self.groupBox_recBasic)
        self.lbl_AT.setObjectName(u"lbl_AT")

        self.formLayout_6.setWidget(9, QFormLayout.LabelRole, self.lbl_AT)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.comboBox_LOC_TYPES = QComboBox(self.groupBox_recBasic)
        self.comboBox_LOC_TYPES.setObjectName(u"comboBox_LOC_TYPES")

        self.horizontalLayout_20.addWidget(self.comboBox_LOC_TYPES)

        self.spinBox_AT = QSpinBox(self.groupBox_recBasic)
        self.spinBox_AT.setObjectName(u"spinBox_AT")

        self.horizontalLayout_20.addWidget(self.spinBox_AT)


        self.formLayout_6.setLayout(9, QFormLayout.FieldRole, self.horizontalLayout_20)


        self.verticalLayout_5.addWidget(self.groupBox_recBasic)

        self.groupBox_recCustomized = QGroupBox(self.tab_RecTagger)
        self.groupBox_recCustomized.setObjectName(u"groupBox_recCustomized")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_recCustomized)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.checkBox_addCustomized = QCheckBox(self.groupBox_recCustomized)
        self.checkBox_addCustomized.setObjectName(u"checkBox_addCustomized")

        self.verticalLayout_7.addWidget(self.checkBox_addCustomized)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.comboBox_tagTemplates = QComboBox(self.groupBox_recCustomized)
        self.comboBox_tagTemplates.setObjectName(u"comboBox_tagTemplates")

        self.horizontalLayout_21.addWidget(self.comboBox_tagTemplates)

        self.btn_saveTemplate = QPushButton(self.groupBox_recCustomized)
        self.btn_saveTemplate.setObjectName(u"btn_saveTemplate")

        self.horizontalLayout_21.addWidget(self.btn_saveTemplate)

        self.btn_deleteCurrentTemplate = QPushButton(self.groupBox_recCustomized)
        self.btn_deleteCurrentTemplate.setObjectName(u"btn_deleteCurrentTemplate")

        self.horizontalLayout_21.addWidget(self.btn_deleteCurrentTemplate)


        self.verticalLayout_7.addLayout(self.horizontalLayout_21)

        self.tableView_customized = QTableView(self.groupBox_recCustomized)
        self.tableView_customized.setObjectName(u"tableView_customized")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView_customized.sizePolicy().hasHeightForWidth())
        self.tableView_customized.setSizePolicy(sizePolicy)
        self.tableView_customized.setAutoFillBackground(False)

        self.verticalLayout_7.addWidget(self.tableView_customized)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.btn_removeSelectedRows = QPushButton(self.groupBox_recCustomized)
        self.btn_removeSelectedRows.setObjectName(u"btn_removeSelectedRows")

        self.horizontalLayout_8.addWidget(self.btn_removeSelectedRows)

        self.btn_addNewRows = QPushButton(self.groupBox_recCustomized)
        self.btn_addNewRows.setObjectName(u"btn_addNewRows")

        self.horizontalLayout_8.addWidget(self.btn_addNewRows)

        self.btn_moveUp = QPushButton(self.groupBox_recCustomized)
        self.btn_moveUp.setObjectName(u"btn_moveUp")

        self.horizontalLayout_8.addWidget(self.btn_moveUp)

        self.btn_moveDown = QPushButton(self.groupBox_recCustomized)
        self.btn_moveDown.setObjectName(u"btn_moveDown")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_moveDown.sizePolicy().hasHeightForWidth())
        self.btn_moveDown.setSizePolicy(sizePolicy1)

        self.horizontalLayout_8.addWidget(self.btn_moveDown)


        self.verticalLayout_7.addLayout(self.horizontalLayout_8)


        self.verticalLayout_5.addWidget(self.groupBox_recCustomized)


        self.horizontalLayout_23.addLayout(self.verticalLayout_5)

        self.groupBox_tagOutput = QGroupBox(self.tab_RecTagger)
        self.groupBox_tagOutput.setObjectName(u"groupBox_tagOutput")
        self.verticalLayout_11 = QVBoxLayout(self.groupBox_tagOutput)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.lbl_recDir = QLabel(self.groupBox_tagOutput)
        self.lbl_recDir.setObjectName(u"lbl_recDir")

        self.verticalLayout_11.addWidget(self.lbl_recDir)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.lineEdit_recDir = QLineEdit(self.groupBox_tagOutput)
        self.lineEdit_recDir.setObjectName(u"lineEdit_recDir")

        self.horizontalLayout_11.addWidget(self.lineEdit_recDir)

        self.btn_browse = QPushButton(self.groupBox_tagOutput)
        self.btn_browse.setObjectName(u"btn_browse")

        self.horizontalLayout_11.addWidget(self.btn_browse)


        self.verticalLayout_11.addLayout(self.horizontalLayout_11)

        self.lbl_serialName_2 = QLabel(self.groupBox_tagOutput)
        self.lbl_serialName_2.setObjectName(u"lbl_serialName_2")

        self.verticalLayout_11.addWidget(self.lbl_serialName_2)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.lineEdit_filenameSN = QLineEdit(self.groupBox_tagOutput)
        self.lineEdit_filenameSN.setObjectName(u"lineEdit_filenameSN")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lineEdit_filenameSN.sizePolicy().hasHeightForWidth())
        self.lineEdit_filenameSN.setSizePolicy(sizePolicy2)
        self.lineEdit_filenameSN.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_18.addWidget(self.lineEdit_filenameSN)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.btn_decreaseSN = QPushButton(self.groupBox_tagOutput)
        self.btn_decreaseSN.setObjectName(u"btn_decreaseSN")

        self.gridLayout.addWidget(self.btn_decreaseSN, 1, 0, 1, 1)

        self.btn_increaseSN = QPushButton(self.groupBox_tagOutput)
        self.btn_increaseSN.setObjectName(u"btn_increaseSN")

        self.gridLayout.addWidget(self.btn_increaseSN, 0, 0, 1, 1)

        self.btn_resetSN = QPushButton(self.groupBox_tagOutput)
        self.btn_resetSN.setObjectName(u"btn_resetSN")

        self.gridLayout.addWidget(self.btn_resetSN, 0, 1, 1, 1)

        self.btn_copyFilenameSN = QPushButton(self.groupBox_tagOutput)
        self.btn_copyFilenameSN.setObjectName(u"btn_copyFilenameSN")

        self.gridLayout.addWidget(self.btn_copyFilenameSN, 1, 1, 1, 1)


        self.horizontalLayout_18.addLayout(self.gridLayout)


        self.verticalLayout_11.addLayout(self.horizontalLayout_18)

        self.groupBox_status = QGroupBox(self.groupBox_tagOutput)
        self.groupBox_status.setObjectName(u"groupBox_status")
        self.verticalLayout_16 = QVBoxLayout(self.groupBox_status)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.textBrowser_status = QTextBrowser(self.groupBox_status)
        self.textBrowser_status.setObjectName(u"textBrowser_status")

        self.verticalLayout_16.addWidget(self.textBrowser_status)


        self.verticalLayout_11.addWidget(self.groupBox_status)

        self.groupBox_tagPreview = QGroupBox(self.groupBox_tagOutput)
        self.groupBox_tagPreview.setObjectName(u"groupBox_tagPreview")
        self.verticalLayout_14 = QVBoxLayout(self.groupBox_tagPreview)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.btn_writeToRec = QPushButton(self.groupBox_tagPreview)
        self.btn_writeToRec.setObjectName(u"btn_writeToRec")

        self.horizontalLayout_19.addWidget(self.btn_writeToRec)

        self.btn_loadFromRec = QPushButton(self.groupBox_tagPreview)
        self.btn_loadFromRec.setObjectName(u"btn_loadFromRec")

        self.horizontalLayout_19.addWidget(self.btn_loadFromRec)

        self.btn_recoverRec = QPushButton(self.groupBox_tagPreview)
        self.btn_recoverRec.setObjectName(u"btn_recoverRec")

        self.horizontalLayout_19.addWidget(self.btn_recoverRec)


        self.verticalLayout_14.addLayout(self.horizontalLayout_19)

        self.textEdit_tags = QTextEdit(self.groupBox_tagPreview)
        self.textEdit_tags.setObjectName(u"textEdit_tags")

        self.verticalLayout_14.addWidget(self.textEdit_tags)


        self.verticalLayout_11.addWidget(self.groupBox_tagPreview)


        self.horizontalLayout_23.addWidget(self.groupBox_tagOutput)

        self.tabs.addTab(self.tab_RecTagger, "")
        self.tab_RecSumGen = QWidget()
        self.tab_RecSumGen.setObjectName(u"tab_RecSumGen")
        self.verticalLayout_21 = QVBoxLayout(self.tab_RecSumGen)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.pushButton_5 = QPushButton(self.tab_RecSumGen)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.verticalLayout_21.addWidget(self.pushButton_5)

        self.listView_2 = QListView(self.tab_RecSumGen)
        self.listView_2.setObjectName(u"listView_2")

        self.verticalLayout_21.addWidget(self.listView_2)

        self.pushButton_6 = QPushButton(self.tab_RecSumGen)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.verticalLayout_21.addWidget(self.pushButton_6)

        self.tableView = QTableView(self.tab_RecSumGen)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_21.addWidget(self.tableView)

        self.pushButton_7 = QPushButton(self.tab_RecSumGen)
        self.pushButton_7.setObjectName(u"pushButton_7")

        self.verticalLayout_21.addWidget(self.pushButton_7)

        self.tabs.addTab(self.tab_RecSumGen, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_22 = QVBoxLayout(self.tab)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.groupBox_10 = QGroupBox(self.tab)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.formLayout_7 = QFormLayout(self.groupBox_10)
        self.formLayout_7.setObjectName(u"formLayout_7")
        self.label_45 = QLabel(self.groupBox_10)
        self.label_45.setObjectName(u"label_45")

        self.formLayout_7.setWidget(0, QFormLayout.LabelRole, self.label_45)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.lineEdit_20 = QLineEdit(self.groupBox_10)
        self.lineEdit_20.setObjectName(u"lineEdit_20")

        self.horizontalLayout_5.addWidget(self.lineEdit_20)

        self.pushButton_8 = QPushButton(self.groupBox_10)
        self.pushButton_8.setObjectName(u"pushButton_8")

        self.horizontalLayout_5.addWidget(self.pushButton_8)


        self.formLayout_7.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_5)

        self.label_46 = QLabel(self.groupBox_10)
        self.label_46.setObjectName(u"label_46")

        self.formLayout_7.setWidget(1, QFormLayout.LabelRole, self.label_46)

        self.label_44 = QLabel(self.groupBox_10)
        self.label_44.setObjectName(u"label_44")

        self.formLayout_7.setWidget(2, QFormLayout.LabelRole, self.label_44)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.comboBox_16 = QComboBox(self.groupBox_10)
        self.comboBox_16.setObjectName(u"comboBox_16")

        self.horizontalLayout_25.addWidget(self.comboBox_16)

        self.pushButton_10 = QPushButton(self.groupBox_10)
        self.pushButton_10.setObjectName(u"pushButton_10")

        self.horizontalLayout_25.addWidget(self.pushButton_10)


        self.formLayout_7.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_25)

        self.comboBox_15 = QComboBox(self.groupBox_10)
        self.comboBox_15.setObjectName(u"comboBox_15")

        self.formLayout_7.setWidget(1, QFormLayout.FieldRole, self.comboBox_15)


        self.verticalLayout_22.addWidget(self.groupBox_10)

        self.groupBox_11 = QGroupBox(self.tab)
        self.groupBox_11.setObjectName(u"groupBox_11")

        self.verticalLayout_22.addWidget(self.groupBox_11)

        self.graphicsView = QGraphicsView(self.tab)
        self.graphicsView.setObjectName(u"graphicsView")

        self.verticalLayout_22.addWidget(self.graphicsView)

        self.tabs.addTab(self.tab, "")

        self.horizontalLayout_22.addWidget(self.tabs)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 709, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox_display.setTitle(QCoreApplication.translate("MainWindow", u"Display", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Incubation (weeks)", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"Numbers of Animals", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Ages (weeks)", None))
        self.groupBox_fileIO.setTitle(QCoreApplication.translate("MainWindow", u"File IO", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.groupBox_animals.setTitle(QCoreApplication.translate("MainWindow", u"Animals", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Animal ID", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Species", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Genotype", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Sex", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Date of Birth", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Date of Injection", None))
        self.groupBox_basics.setTitle(QCoreApplication.translate("MainWindow", u"Basics", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Date of Recording", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Experimenters", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"ACUC protocol", None))
        self.btn_add_ACUC_PN.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.btn_rm_ACUC_PN.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.groupBox_solutions.setTitle(QCoreApplication.translate("MainWindow", u"Solutions", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"Cutting(mOsm/Kg)", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"Holding(mOsm/Kg)", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Recording(mOsm/Kg)", None))
        self.groupBox_injections.setTitle(QCoreApplication.translate("MainWindow", u"Injections", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Target Area", None))
        self.checkBox_hemisphere_R.setText(QCoreApplication.translate("MainWindow", u"Right", None))
        self.checkBox_hemisphere_L.setText(QCoreApplication.translate("MainWindow", u"Left", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Right Hemisphere", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Volume", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Mode", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Coordinates", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"DV", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"ML", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"AP", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Virus", None))
        self.btn_add_virus_R.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.btn_rm_virus_R.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Left Hemisphere", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Volume", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Mode", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Coordinates", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Virus", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"DV", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"ML", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"AP", None))
        self.btn_add_virus_L.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.btn_rm_virus_L.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_ExpInfo), QCoreApplication.translate("MainWindow", u"Exp Info", None))
        self.groupBox_recBasic.setTitle(QCoreApplication.translate("MainWindow", u"Experiment Date: YYYY_MM_DD", None))
        self.lbl_OBJ.setText(QCoreApplication.translate("MainWindow", u"OBJ", None))
        self.radioBtn_10X.setText(QCoreApplication.translate("MainWindow", u"10X", None))
        self.radioBtn_40X.setText(QCoreApplication.translate("MainWindow", u"40X", None))
        self.radioBtn_60X.setText(QCoreApplication.translate("MainWindow", u"60X", None))
        self.lbl_EXC.setText(QCoreApplication.translate("MainWindow", u"EXC", None))
        self.lbl_LEVEL.setText(QCoreApplication.translate("MainWindow", u"LEVEL", None))
        self.lbl_EXPO.setText(QCoreApplication.translate("MainWindow", u"EXPO", None))
        self.lbl_EMI.setText(QCoreApplication.translate("MainWindow", u"EMI", None))
        self.lbl_FRAMES.setText(QCoreApplication.translate("MainWindow", u"FRAMES (p)", None))
        self.lbl_FPS.setText(QCoreApplication.translate("MainWindow", u"FPS (Hz)", None))
        self.lbl_CAM_TRIG_MODE.setText(QCoreApplication.translate("MainWindow", u"CAM_TRIG_MODE", None))
        self.lbl_SLICE.setText(QCoreApplication.translate("MainWindow", u"SLICE", None))
        self.lbl_AT.setText(QCoreApplication.translate("MainWindow", u"AT", None))
        self.groupBox_recCustomized.setTitle(QCoreApplication.translate("MainWindow", u"Customized Parameters", None))
        self.checkBox_addCustomized.setText(QCoreApplication.translate("MainWindow", u"Check to add customized parameters", None))
        self.btn_saveTemplate.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.btn_deleteCurrentTemplate.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.btn_removeSelectedRows.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.btn_addNewRows.setText(QCoreApplication.translate("MainWindow", u"Insert", None))
        self.btn_moveUp.setText(QCoreApplication.translate("MainWindow", u"Shift Up", None))
        self.btn_moveDown.setText(QCoreApplication.translate("MainWindow", u"Shift Down", None))
        self.groupBox_tagOutput.setTitle(QCoreApplication.translate("MainWindow", u"Output", None))
        self.lbl_recDir.setText(QCoreApplication.translate("MainWindow", u"Directory of the recording files", None))
        self.btn_browse.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.lbl_serialName_2.setText(QCoreApplication.translate("MainWindow", u"Filename SN", None))
        self.lineEdit_filenameSN.setText("")
        self.lineEdit_filenameSN.setPlaceholderText("")
        self.btn_decreaseSN.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.btn_increaseSN.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.btn_resetSN.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.btn_copyFilenameSN.setText(QCoreApplication.translate("MainWindow", u"Copy", None))
        self.groupBox_status.setTitle(QCoreApplication.translate("MainWindow", u"Status", None))
        self.groupBox_tagPreview.setTitle(QCoreApplication.translate("MainWindow", u"Tag Preview and Operations", None))
        self.btn_writeToRec.setText(QCoreApplication.translate("MainWindow", u"Write", None))
        self.btn_loadFromRec.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.btn_recoverRec.setText(QCoreApplication.translate("MainWindow", u"Recover", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_RecTagger), QCoreApplication.translate("MainWindow", u"Rec Tagger", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Scan REC files", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Generate", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_RecSumGen), QCoreApplication.translate("MainWindow", u"Rec Summary Generator", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("MainWindow", u"Preprocessing Parameters", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"Directory", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"Filename", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"Gaussian Kernel Radius", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"Process", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("MainWindow", u"Release Map", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Quick Analysis", None))
    # retranslateUi

