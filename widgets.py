import os
import sys
import os.path as osp
from qtpy.QtCore import Qt, QSize, QRect
from qtpy.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                            QLabel, QPushButton, QFileDialog, QTextBrowser,
                            QGridLayout, QRadioButton, QMenuBar, QListWidget)


class myWindow(QMainWindow):
    def __init__(self):
        super(myWindow, self).__init__()
        self.resize(QSize(1296, 720))
        self.setWindowTitle("COCO 人体关键点标注工具")

        # textbrowser
        self.textBrowser = QTextBrowser()

        # menubar
        menubar = self.menuBar()
        self.filemenu = menubar.addMenu('Files(&F)')
        self.editmenu = menubar.addMenu('Edit(&E)')

        # display label
        self.displayimage = QLabel()
        self.displayimage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # open images dir button
        self.openimagedir = QPushButton()
        self.openimagedir.setText("OpenImageDir")
        # open jsonfile dir button
        self.openjsondir = QPushButton()
        self.openjsondir.setText("OpenJsonDir")
        # next image button
        self.nextimage = QPushButton()
        self.nextimage.setText("NextImage")
        # prev image button
        self.previmage = QPushButton()
        self.previmage.setText("PreviousImage")
        
        # labellist
        self.labellist = QListWidget()
        
        # open image or json file layout
        open_image_json_layout = QHBoxLayout()
        open_image_json_layout.addWidget(self.openimagedir)
        open_image_json_layout.addWidget(self.openjsondir)

        # switch image latout
        switch_image_layout = QHBoxLayout()
        switch_image_layout.addWidget(self.previmage)
        switch_image_layout.addWidget(self.nextimage)
        # button layout
        button_layout = QVBoxLayout()
        button_layout.addLayout(open_image_json_layout)
        button_layout.addLayout(switch_image_layout)
        button_layout.addWidget(self.labellist)
        button_layout.addWidget(self.textBrowser)

        
        global_layout = QHBoxLayout()
        global_layout.addWidget(self.displayimage, 5)
        global_layout.addLayout(button_layout, 1)

        # mainwindow widget
        widget = QWidget()
        widget.setLayout(global_layout)
        self.setCentralWidget(widget)





