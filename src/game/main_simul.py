# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

"""
Cette classe fournit un interface graphique pour lancer des partie en simultané avec D=10 

"""

from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np 
from dice import *
from hog import hog
from outils import *

class Ui_Frame(object):
    def setupUi(self, Frame,joueur=1):
        D = 10
        N = 100
        self.h = hog(D,N)
        
        self.result = lp_resolution(self.h.probabiltes,D,joueur)
        
        Frame.setObjectName("Frame")
        Frame.resize(750, 247)
        self.gridLayout_2 = QtWidgets.QGridLayout(Frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.Text = QtWidgets.QLabel(Frame)
        self.Text.setObjectName("Text")
        self.verticalLayout.addWidget(self.Text)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.entry_d1 = QtWidgets.QSpinBox(Frame)
        self.entry_d1.setMinimum(1)
        self.entry_d1.setObjectName("entry_d1")
        self.horizontalLayout.addWidget(self.entry_d1)
        self.button_lancer = QtWidgets.QPushButton(Frame)
        self.button_lancer.setObjectName("button_lancer")
        self.horizontalLayout.addWidget(self.button_lancer)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.d1_aff = QtWidgets.QLabel(Frame)
        self.d1_aff.setObjectName("d1_aff")
        self.horizontalLayout_2.addWidget(self.d1_aff)
        self.d2_aff = QtWidgets.QLabel(Frame)
        self.d2_aff.setObjectName("d2_aff")
        self.horizontalLayout_2.addWidget(self.d2_aff)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.ganeur_aff = QtWidgets.QLabel(Frame)
        self.ganeur_aff.setObjectName("ganeur_aff")
        self.gridLayout.addWidget(self.ganeur_aff, 3, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.score1_aff = QtWidgets.QLabel(Frame)
        self.score1_aff.setObjectName("score1_aff")
        self.horizontalLayout_3.addWidget(self.score1_aff)
        self.score2_aff = QtWidgets.QLabel(Frame)
        self.score2_aff.setObjectName("score2_aff")
        self.horizontalLayout_3.addWidget(self.score2_aff)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.Nom = QtWidgets.QLabel(Frame)
        self.Nom.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.Nom.setObjectName("Nom")
        self.gridLayout_2.addWidget(self.Nom, 0, 0, 1, 1)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)
    
    
    def clicked(self):
        self.play()   
    
    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.Text.setText(_translate("Frame", "Nombre de Dés que vous vouler lancer:"))
        self.button_lancer.setText(_translate("Frame", "lancer !"))
       
        self.Nom.setText(_translate("Frame", "Simultane"))
        self.button_lancer.clicked.connect(self.clicked)
    
    
    def roulez_les_des(self,d):
        
        assert type(d) == int, 'nombre de dés doit étre un entier.'
        assert d > 0, 'il faut faire au moin un lacer.'

        vfunc = np.vectorize(lambda x: dice())
        a = np.zeros(d) - 1
        a = vfunc(a)
        if(1 in a):
            return 1
        else:
            return a.sum()
    
    def play(self):
        
        a = np.array(np.array([ v.varValue for v in self.result])).cumsum()
        r = np.random.random()
        
        d2 =  int(np.where(a > r)[0][0])+1
        
        d1 = self.entry_d1.value()
        
        _translate = QtCore.QCoreApplication.translate
        
        strs = _translate("Frame", "d1 = "+str(d1))
        self.d1_aff.setText(strs)
        
        strs = _translate("Frame", "d2 = "+str(d2))
        self.d2_aff.setText(strs)
        
        socre1 =  self.roulez_les_des(d1)
        self.score1_aff.setText(_translate("Frame", "Score Joueur1 = "+str(socre1)))
        
        score2 =  self.roulez_les_des(d2)
        self.score2_aff.setText(_translate("Frame", "Score Joueur2 = "+str(score2)))
        
        winner = 0
        b=True
        if(socre1 > score2 ):
            b = False
            winner = 1
            self.ganeur_aff.setText(_translate("Frame", "Joueur "+str(winner)+" Gagne !!"))
        if(socre1 < score2 ) :
            b = False
            winner = 2
            self.ganeur_aff.setText(_translate("Frame", "Joueur "+str(winner)+" Gagne !!"))
        if(b):
            self.ganeur_aff.setText(_translate("Frame", "La Partie est nulle"))
            
        
        #print("////////////////////(    ",socre1,'|',score2,"   )////////////////////////////////")
        
            


if __name__ == "__main__":
    import sys
    joueur = 1
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame,joueur)
    Frame.show()
    sys.exit(app.exec_())


