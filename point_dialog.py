import os
import sys

from qtpy import QtCore
from qtpy.QtWidgets import (QDialog, QDialogButtonBox, QVBoxLayout, QLabel,
                            QGridLayout, QRadioButton, QLineEdit, QListWidget)


class SelectDialog(QDialog):
    def __init__(self):
        super(SelectDialog, self).__init__()
        self.setWindowTitle("Selected Points")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        # 
        self.categories = QLineEdit()
        self.labellist = QListWidget()

        # categories radio button
        self.nose = QRadioButton()
        self.nose.setText("Nose")
        self.lefteye = QRadioButton()
        self.lefteye.setText("Left Eye")
        self.righteye = QRadioButton()
        self.righteye.setText("Right Eye")
        self.leftear = QRadioButton()
        self.leftear.setText("Left Ear")
        self.rightear = QRadioButton()
        self.rightear.setText("Right Ear")
        self.leftshoulder = QRadioButton()
        self.leftshoulder.setText("Left Shoulder")
        self.rightshoulder = QRadioButton()
        self.rightshoulder.setText("Right Shoulder")
        self.leftelbow = QRadioButton()
        self.leftelbow.setText("Left Elbow")
        self.rightelbow = QRadioButton()
        self.rightelbow.setText("Right Elbow")
        self.leftwrist = QRadioButton()
        self.leftwrist.setText("Left Wrist")
        self.rightwrist = QRadioButton()
        self.rightwrist.setText("Right Wrist")
        self.lefthip = QRadioButton()
        self.lefthip.setText("Left Hip")
        self.righthip = QRadioButton()
        self.righthip.setText("Right Hip")
        self.leftknee = QRadioButton()
        self.leftknee.setText("Left Knee")
        self.rightknee = QRadioButton()
        self.rightknee.setText("Right Knee")
        self.leftankle = QRadioButton()
        self.leftankle.setText("Left Ankle")
        self.rightankle = QRadioButton()
        self.rightankle.setText("Right Ankle")

        self.radiobuttondict = {"nose": self.nose, 
                                "lefteye": self.lefteye, "righteye": self.righteye,
                                "leftear": self.leftear, "rightear": self.rightear,
                                "leftshoulder": self.leftshoulder, "rightshoulder": self.rightshoulder,
                                "leftelbow": self.leftelbow, "rightelbow": self.rightelbow,
                                "leftwrist": self.leftwrist, "rightwrist": self.rightwrist,
                                "lefthip": self.lefthip, "righthip": self.righthip,
                                "leftknee": self.leftknee, "rightknee": self.rightknee,
                                "leftankle": self.leftankle, "rightankle": self.rightankle,
                                }

        # categories gridLayout
        gridLayout = QGridLayout()
        gridLayout.addWidget(self.nose, 0, 0)
        gridLayout.addWidget(self.lefteye, 1, 0)
        gridLayout.addWidget(self.righteye, 1, 1)
        gridLayout.addWidget(self.leftear, 2, 0)
        gridLayout.addWidget(self.rightear, 2, 1)
        gridLayout.addWidget(self.leftshoulder, 3, 0)
        gridLayout.addWidget(self.rightshoulder, 3, 1)
        gridLayout.addWidget(self.leftelbow, 4, 0)
        gridLayout.addWidget(self.rightelbow, 4, 1)
        gridLayout.addWidget(self.leftwrist, 5, 0)
        gridLayout.addWidget(self.rightwrist, 5, 1)
        gridLayout.addWidget(self.lefthip, 6, 0)
        gridLayout.addWidget(self.righthip, 6, 1)
        gridLayout.addWidget(self.leftknee, 7, 0)
        gridLayout.addWidget(self.rightknee, 7, 1)
        gridLayout.addWidget(self.leftankle, 8, 0)
        gridLayout.addWidget(self.rightankle, 8, 1)


        global_layout = QVBoxLayout()
        global_layout.addWidget(self.categories)
        global_layout.addWidget(self.labellist)
        global_layout.addLayout(gridLayout)
        global_layout.addWidget(self.buttonBox)
        self.setLayout(global_layout)
