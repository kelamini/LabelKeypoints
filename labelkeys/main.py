import os
import sys
import json
import cv2 as cv
import numpy as np
import os.path as osp
from glob import glob
from collections import defaultdict
from functools import partial

from qtpy.QtGui import (QPixmap, QImage, QTextCursor, QPainter, QPen, QColor, QIcon)
from qtpy import QtCore
from qtpy.QtCore import Qt, QSize, QTimer, QEventLoop, QRect
from qtpy.QtWidgets import QApplication, QMainWindow, QFileDialog, QMenu, QLabel
from PyQt5.QtWidgets import QAction

from labelkeys.widgets import myWindow, __appname__
from labelkeys.point_dialog import SelectDialog

here = osp.dirname(osp.abspath(__file__))


class EmittingStr(QtCore.QObject):
    textWritten = QtCore.Signal(str)
    def write(self, text):
    #   text = f"({os.getcwd()})=> {text}\n"
      self.textWritten.emit(text)
      loop = QEventLoop()
      QTimer.singleShot(10, loop.quit)
      loop.exec_()

    def flush(self):
        pass


def read_json(filepath):
    with open(filepath, "r", encoding="utf8") as fp:
        return json.load(fp)

def write_json(filepath, data):
    with open(filepath, "w", encoding="utf8") as fp:
         json.dump(data, fp, indent=2)


class MainWindow(myWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.image_path = None
        self.json_path = None
        self.image_list = []
        self.json_list = []
        self.json_data = None
        self.imageheight = None
        self.imagewidth = None
        self.current_image = None
        self.current_image_id = 0
        self.categories_name = set()
        self.current_category_name = None
        self.current_keypoint_name = None
        self.keypoints = defaultdict(dict)
        self.categoties = defaultdict(dict)
        self.left_point = 0
        self.top_point = 0
        self.current_pos = None
        self.current_keypoints = [0, 0]
        self.pos_visual = None
        self.pen_visual = QPen()
        self.pen_visual.setWidth(8)
        self.pen_invisual = QPen()
        self.pen_invisual.setWidth(8)
        self.pen_pre = QPen()
        self.pen_pre.setWidth(12)
        self.pen_pre.setBrush(Qt.red)

        # dialog
        self.dlg = SelectDialog()
        # painter
        self.ptr = QPainter()

        # 输出重定向到 textbrowser
        sys.stdout = EmittingStr()
        sys.stdout.textWritten.connect(self.outputWritten)
        sys.stderr = EmittingStr()
        sys.stderr.textWritten.connect(self.outputWritten)

        # button
        self.openimagedir.clicked.connect(self.open_image_dir)
        self.openjsondir.clicked.connect(self.open_json_dir)
        self.nextimage.clicked.connect(self.next_image)
        self.previmage.clicked.connect(self.previous_image)

        # menubar
        self.muopenimagedir = QAction('OpenImage(&I)', self)
        self.muopenimagedir.setShortcut('I')
        self.muopenimagedir.triggered.connect(self.open_image_dir)
        self.filemenu.addAction(self.muopenimagedir)
        self.muopenjsondir = QAction('OpenJson(&J)', self)
        self.muopenjsondir.setShortcut('J')
        self.muopenjsondir.triggered.connect(self.open_json_dir)
        self.filemenu.addAction(self.muopenjsondir)
        self.musavejson = QAction('SaveJson(&J)', self)
        self.musavejson.setShortcut('Ctrl+S')
        self.musavejson.triggered.connect(self.save_current_json)
        self.filemenu.addAction(self.musavejson)
        self.munextimage = QAction('NextImage(&D)', self)
        self.munextimage.setShortcut('D')
        self.munextimage.triggered.connect(self.next_image)
        self.editmenu.addAction(self.munextimage)
        self.mupreviousimage = QAction('PreviousImage(&A)', self)
        self.mupreviousimage.setShortcut('A')
        self.mupreviousimage.triggered.connect(self.previous_image)
        self.editmenu.addAction(self.mupreviousimage)

        self.dlg.radiobuttondict["nose"].setChecked(True)
        self.dlg.radiobuttondict["nose"].setStyleSheet("background-color: red")
        self.current_keypoint_name = "nose"

        if not self.labellist.items == None:
            self.labellist.itemClicked.connect(self.labellist_clicked)
            self.labellist.itemDoubleClicked.connect(self.labellist_doubleclicked)
        if not self.imagelist.items == None:
            self.imagelist.itemClicked.connect(self.imagelist_clicked)

    def outputWritten(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    def open_image_dir(self):
        self.image_path = QFileDialog.getExistingDirectory(None, "请选择文件路径")
        print("===> Now, you open this images dir: ", self.image_path)
        try:
            self.image_list = sorted(glob(f"{self.image_path}/*jpg"))
            for im in self.image_list:
                self.imagelist.addItem(osp.basename(im))
            self.load_image(self.image_list[0])
            self.imagelist.sortItems()
        except:
            pass

    def check_image_json(self):
        for imagepath in self.image_list:
            filename = osp.basename(imagepath).replace(".jpg", "")
            filepath = osp.join(self.json_path, filename+".json")
            if not filepath in self.json_list:
                self.json_list.append(osp.join(self.json_path, filename+".json"))
        self.json_list = sorted(self.json_list)
    
    def open_json_dir(self):
        self.json_path = QFileDialog.getExistingDirectory(None, "请选择文件路径")
        print("===> Now, you open this json file dir: ", self.json_path)
        try:
            self.json_list = sorted(glob(f"{self.json_path}/*json"))
            self.check_image_json()
            self.load_json(self.json_list[0])
        except:
            pass

    def load_image(self, filepath):
        if not osp.exists(filepath):
            print(f"===> {filepath} not exists!")
            return
        image = cv.imread(filepath)
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        self.imageheight, self.imagewidth, self.channel = image.shape
        print(f"===> ({self.current_image_id+1}/{len(self.image_list)}) Current image: {osp.basename(self.image_list[self.current_image_id])}")
        self.scale = np.round(self.height() / max(self.imagewidth, self.imageheight), 1)
        if int(self.imagewidth/self.imageheight) == int(self.displayimage.width()/self.height()):
            self.scale = round(0.8*(self.height()/self.imageheight), 1)
        print("===> scale: ", self.scale)
        self.current_image = QImage(image.data, self.imagewidth, self.imageheight, self.imagewidth*self.channel, QImage.Format_RGB888)
        self.current_image = QPixmap.fromImage(self.current_image)
        self.current_image = self.current_image.scaled(self.current_image.width()*self.scale, self.current_image.height()*self.scale)
        # self.displayimage.setPixmap(self.current_image)
        self.update()

    def init_json(self):
        self.json_data = {
            "imagePath": osp.basename(self.image_list[self.current_image_id]),
            "imageWidth": self.imagewidth,
            "imageHeight": self.imageheight,
            "keypoints": defaultdict(dict),
        }

    def update_save_json(self):
        if self.current_image:
            if np.sum(self.current_keypoints) > 0:
                self.json_data = {
                    "imagePath": osp.basename(self.image_list[self.current_image_id]),
                    "imageWidth": self.imagewidth,
                    "imageHeight": self.imageheight,
                    "keypoints": self.keypoints,
                }
                write_json(self.json_list[self.current_image_id], self.json_data)
                self.current_pos = None
                self.current_keypoints = [0, 0]
                # self.current_category_name = None
                # self.current_keypoint_name = None
                # self.keypoints = defaultdict(dict)

    def load_json(self, filepath):
        if not osp.exists(filepath):
            print(f"===> {filepath} not exists, will create!")
            self.init_json()
            write_json(filepath, self.json_data)
        self.dlg.labellist.clear()
        self.labellist.clear()
        self.json_data = read_json(filepath)
        if "keypoints" in self.json_data:
            self.keypoints = self.json_data["keypoints"]
            for cats, keypoints in self.keypoints.items():
                self.categories_name.add(cats)
                if cats in self.categories_name:
                    self.dlg.labellist.addItem(cats)
                for cat, keypoint in keypoints.items():
                    self.labellist.addItem(f"${cats}@{cat}")
        else:
            self.keypoints = defaultdict(dict)
        self.dlg.labellist.sortItems()
        self.labellist.sortItems()
        self.update()


        # print("===> keypoints: ", self.keypoints)

    def next_image(self):
        if len(self.image_list) == 0:
            print("===> No loaded image...")
            return
        if self.current_image_id < len(self.image_list)-1:
            self.update_save_json()
            self.current_image_id += 1
            print(f"===> ({self.current_image_id+1}/{len(self.image_list)}) Current image: {osp.basename(self.image_list[self.current_image_id])}")
            self.load_image(self.image_list[self.current_image_id])

            # 加载 json 文件
            try:
                self.load_json(self.json_list[self.current_image_id])
            except:
                print("===> Not load json file!")

    def previous_image(self):
        if len(self.image_list) == 0:
            print("===> No loaded image...")
            return
        if self.current_image_id > 0:
            self.update_save_json()
            self.current_image_id -= 1
            print(f"===> ({self.current_image_id+1}/{len(self.image_list)}) Current image: {osp.basename(self.image_list[self.current_image_id])}")
            self.load_image(self.image_list[self.current_image_id])
            
            # 加载 json 文件
            try:
                self.load_json(self.json_list[self.current_image_id])
            except:
                print("===> Not load json file!")

    def get_color_from_name(self, name):
        color = QColor()
        color_map = dict()
        color_list = list()
        for color_name in color.colorNames():
            color_list.append(color_name)
        step = len(color.colorNames()) // len(self.dlg.radiobuttondict)
        for i, cat in enumerate(self.dlg.radiobuttondict):
            color_map[cat] = color_list[i+step]
        
        self.color_name = color_map[name]
        # print("color_name", self.color_name)

    def paintEvent(self, event):
        self.ptr.begin(self)
        if self.current_image:
            self.left_point = (abs(self.displayimage.width() - self.current_image.width())) // 2
            self.top_point = (abs(self.height() - self.current_image.height())) // 2
            self.ptr.drawPixmap(self.left_point, self.top_point, self.current_image)
            for cats, keypoints in self.keypoints.items():
                for cat, keypoint in keypoints.items():
                    if keypoint[2] == 0:
                        self.get_color_from_name(cat)
                        self.pen_invisual.setColor(QColor(self.color_name))
                        self.ptr.setPen(self.pen_invisual)
                        self.ptr.drawPoint(int(keypoint[0]*self.scale+self.left_point), int(keypoint[1]*self.scale+self.top_point))
                    if keypoint[2] == 1:
                        self.get_color_from_name(cat)
                        self.pen_visual.setColor(QColor(self.color_name))
                        self.ptr.setPen(self.pen_visual)
                        self.ptr.drawPoint(int(keypoint[0]*self.scale+self.left_point), int(keypoint[1]*self.scale+self.top_point))
            self.ptr.setPen(self.pen_pre)
            self.ptr.drawPoint(int(self.current_keypoints[0]+self.left_point), int(self.current_keypoints[1]+self.top_point))
        self.ptr.end()

    def mousePressEvent(self, event):
        if not self.current_image == None:
            if event.buttons() == Qt.LeftButton:
                self.pos_visual = 1
                self.current_pos = [event.pos().x()-self.left_point, event.pos().y()-self.top_point]
                self.current_keypoints = [self.current_pos[0], self.current_pos[1]]
                print(f"===> Clicked left mouse: ({self.current_pos[0]}, {self.current_pos[1]})")
                self.update()
                # self.lastPoint = e.pos()
                self.dialogkeypoints()

            if event.buttons() == Qt.RightButton:
                self.pos_visual = 0
                self.current_pos = [event.pos().x()-self.left_point, event.pos().y()-self.top_point]
                self.current_keypoints = [self.current_pos[0], self.current_pos[1]]
                print(f"===> Clicked left mouse: ({self.current_pos[0]}, {self.current_pos[1]})")
                self.update()
                # self.lastPoint = e.pos()
                self.dialogkeypoints()

    def checkkeypoints(self, cat_name):
        self.current_keypoint_name = cat_name
        self.dlg.radiobuttondict[cat_name].setChecked(True)
        for cat, btn in self.dlg.radiobuttondict.items():
            btn.setStyleSheet("background-color: None")
        self.dlg.radiobuttondict[cat_name].setStyleSheet("background-color: red")

    def dialogkeypoints(self):
        self.dlg.buttonBox.accepted.connect(self.validated)
        self.dlg.buttonBox.rejected.connect(self.dlg.reject)
        self.dlg.categories.returnPressed.connect(self.text_pressed)
        self.dlg.categories.textEdited.connect(self.text_edited)
        self.dlg.labellist.itemClicked.connect(self.change_category)
        for cat_name, btn in self.dlg.radiobuttondict.items():
            btn.clicked.connect(partial(self.checkkeypoints, cat_name))

        if self.dlg.exec_():
            print("===> Success!")
            print("===> current category:", self.current_category_name)
            print("===> current keypoint: ", self.current_keypoint_name)

            if not self.current_category_name in self.keypoints:
                self.keypoints[self.current_category_name] = dict()
            self.keypoints[self.current_category_name][self.current_keypoint_name] = [self.current_keypoints[0]/self.scale, self.current_keypoints[1]/self.scale, self.pos_visual]
            self.labellist.addItem(f"${self.current_category_name}@{self.current_keypoint_name}")
            self.labellist.sortItems()
            # print("===> keypoints: ",  self.keypoints)
        else:
            print("===> Cancel!")

    def validated(self):
        if not self.current_category_name in self.categories_name:
            self.categories_name.add(self.current_category_name)
            # print("===> categories_name: ", self.categories_name)
            self.dlg.labellist.addItem(self.current_category_name)
            self.dlg.labellist.sortItems()
        self.dlg.accept()
        # print("===> categories_name: ", self.current_category_name)

    def text_edited(self, text):
        self.current_category_name = text

    def text_pressed(self):
        self.validated()

    def change_category(self, item):
        self.dlg.categories.setText(item.text())
        self.current_category_name = item.text()

    def labellist_clicked(self, item):
        cats = item.text().split("@")[0].split("$")[-1]
        cat = item.text().split("@")[-1]
        keypoints = self.keypoints[cats][cat]
        print(f"===> {item.text()} clicked: ", keypoints)
        self.current_keypoints = [int(i*self.scale) for i in keypoints[0:-1]]
        self.update()

    def labellist_doubleclicked(self, item):
        cats = item.text().split("@")[0].split("$")[-1]
        cat = item.text().split("@")[-1]
        self.labellist.takeItem(self.labellist.row(item))
        if cat in self.keypoints[cats]:
            self.keypoints[cats].pop(cat)
            self.json_data["keypoints"] = self.keypoints
            # write_json(self.json_list[self.current_image_id], self.json_data)
        print(f"===> {item.text()} deleted")
        self.update()

    def imagelist_clicked(self, item):
        current_image_path = osp.join(self.image_path, item.text())
        # print("===> current_image_path: ", current_image_path)
        self.current_image_id = self.imagelist.row(item)
        self.load_image(current_image_path)
        # print("===> current_image_id: ", self.current_image_id)
        self.current_keypoints = [0, 0]

        # 加载 json 文件
        try:
            self.load_json(self.json_list[self.current_image_id])
        except:
            print("===> Not load json file!")

    def save_current_json(self):
        if np.sum(self.current_keypoints) > 0:
            self.json_data["keypoints"] = self.keypoints
            write_json(self.json_list[self.current_image_id], self.json_data)
            print("Save result to: ", self.json_list[self.current_image_id])


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(__appname__)
    app.setWindowIcon(QIcon(osp.join(":/", here, "icons/coffe.png")))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
