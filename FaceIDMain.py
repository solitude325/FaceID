# author:Solitude0325 time:2022/9/8
# -*- coding: utf-8 -*-
import pickle
import sys
import cv2
import threading
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox, QGroupBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PIL import Image, ImageFont, ImageDraw
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

# 定义人脸标签和初始化标签对应的人物名称
id = 0
data = {}

import time

# 导入OpenCV自带的数据集，定义多个是因为在后面有多次调用，用一个的话会报错
faceCascade = cv2.CascadeClassifier(
    './haarcascade_frontalface_default.xml')
faceCascade2 = cv2.CascadeClassifier(
    './haarcascade_frontalface_default.xml')
faceCascade3 = cv2.CascadeClassifier(
    './haarcascade_frontalface_default.xml')


# 继承QLineEdit，重写mouseReleaseEvent函数
class mylineedit(QLineEdit):
    clicked = pyqtSignal()  # 定义clicked信号

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit()  # 发送clicked信号


class Student():
    def __init__(self, id, name, age, sex, parent):
        self.id = id
        self.name = name
        self.age = age
        self.sex = sex
        self.parent = parent


# 创建主界面类
class Ui_Menu(QWidget):
    def __init__(self):
        super(Ui_Menu, self).__init__()
        # 创建label并设置文本内容
        self.label = QLabel('欢迎使用Face-ID识别系统', self)
        # 创建普通用户和管理员按键
        self.btn_ordinary = QPushButton('身份辨认', self)
        self.btn_admin = QPushButton('人脸注册', self)
        self.btn_edit = QPushButton('信息编辑', self)

        file = open("./datafile.txt", 'ab+')
        file.close()

        if os.path.getsize("./datafile.txt"):
            self.datafile = open("./datafile.txt", 'rb')
            global data
            data = pickle.load(self.datafile)
            self.datafile.close()
        print(data)

        # 初始化界面
        self.init_ui()

    def init_ui(self):
        # 设置窗口大小
        self.resize(1280, 800)
        # 设置label框的位置
        self.label.move(140, 200)

        # 设置按键框的位置和大小
        self.btn_ordinary.setGeometry(550, 420, 181, 61)
        self.btn_admin.setGeometry(550, 510, 181, 61)
        self.btn_edit.setGeometry(550, 600, 181, 61)

        # 设置label样式（字体、大小、颜色等）
        self.label.setStyleSheet(
            "QLabel{color:rgb(0,0,0,255);"  # 字体颜色为黑色
            "font-size:82px;font-weight:bold;"  # 大小为70 加粗
            "font-family:Roman times;}")  # Roman times字体

        self.btn_ordinary.setStyleSheet(
            "QPushButton{color:rgb(0,0,0,255);"  # 字体颜色为黑色
            "font-size:30px;"  # 大小为30 
            "font-family:Roman times;}")  # Roman times字体

        self.btn_admin.setStyleSheet(
            "QPushButton{color:rgb(0,0,0,255);"  # 字体颜色为黑色
            "font-size:30px;"  # 大小为30 
            "font-family:Roman times;}")  # Roman times字体

        self.btn_edit.setStyleSheet(
            "QPushButton{color:rgb(0,0,0,255);"  # 字体颜色为黑色
            "font-size:30px;"  # 大小为30 
            "font-family:Roman times;}")  # Roman times字体

        # 点击管理员按钮事件
        self.btn_admin.clicked.connect(self.slot_btn_admin)
        # 点击普通用户按钮事件
        self.btn_ordinary.clicked.connect(self.slot_btn_ordinary)
        self.btn_edit.clicked.connect(self.slot_btn_edit)

    # 点点击管理员按钮事件
    def slot_btn_admin(self):
        self.manager_face = Ui_manager_face()
        self.manager_face.show()
        self.hide()

    # 点击普通用户按钮事件
    def slot_btn_ordinary(self):
        self.face_reco = Ui_face_reco()
        self.face_reco.show()
        self.hide()

    def slot_btn_edit(self):
        self.edit = Ui_edit()
        self.edit.show()
        self.hide()


# 创建登录界面类
class Ui_edit(QWidget):
    clicked = pyqtSignal()

    def __init__(self):
        super(Ui_edit, self).__init__()

        # 初始化数值
        self.ID_num = ""
        self.name = ""
        self.sex = ""
        self.parent_num = ""

        print(data)

        # 创建账号、密码以、输入框以及登录返回等按键
        self.lab_ID = QLabel('账号', self)
        # self.lab_key = QLabel('密码', self)
        self.lab_name = QLabel('姓名', self)
        self.lab_sex = QLabel('性别', self)
        self.lab_parent = QLabel('监护', self)
        self.Edit_ID = mylineedit(self)
        self.Edit_name = mylineedit(self)
        self.Edit_sex = mylineedit(self)
        self.Edit_parent = mylineedit(self)
        self.selected = self.Edit_ID  # 输入位置标识位
        self.btn_logon = QPushButton('查询', self)
        self.btn_edit = QPushButton('修改', self)
        self.btn_back = QPushButton('返回', self)

        # 设置容器存放数字键，使用栅格布局

        # 点击mylineedit事件
        self.Edit_ID.clicked.connect(self.changeEdit_ID)
        # self.Edit_key.clicked.connect(self.changeEdit_key)

        # 初始化界面
        self.init_ui()

    # 点击Edit_ID事件
    def changeEdit_ID(self):
        self.selected = self.Edit_ID

    # 点击Edit_key事件
    # def changeEdit_key(self):
    #     self.selected = self.Edit_key

    # 初始化界面
    def init_ui(self):
        # 设置窗口大小
        self.resize(1280, 800)
        # 设置lab_ID位置
        self.lab_ID.setGeometry(380, 130, 71, 41)
        self.lab_name.setGeometry(380, 200, 71, 41)
        self.Edit_ID.setGeometry(470, 130, 411, 41)
        self.Edit_name.setGeometry(470, 200, 411, 41)
        self.lab_sex.setGeometry(380, 270, 71, 41)
        self.lab_parent.setGeometry(380, 340, 71, 41)
        self.Edit_sex.setGeometry(470, 270, 411, 41)
        self.Edit_parent.setGeometry(470, 340, 411, 41)
        self.btn_logon.setGeometry(490, 670, 91, 51)
        self.btn_edit.setGeometry(592, 670, 91, 51)
        self.btn_back.setGeometry(690, 670, 91, 51)

        # 设置数字键高度

        # 设置容器位置

        # 将数字存放进容器

        # 对lab_ID字体大小进行设置
        self.lab_ID.setStyleSheet(
            "QLabel{color:rgb(0,0,0,255);"  # 字体颜色为黑色
            "font-size:30px;"  # 大小为30 
            "font-family:Roman times;}")  # Roman times字体

        # 对lab_key字体大小进行设置
        self.lab_name.setStyleSheet(
            "QLabel{color:rgb(0,0,0,255);"  # 字体颜色为黑色
            "font-size:30px;"  # 大小为30 
            "font-family:Roman times;}")  # Roman times字体

        # 对Edit_ID字体大小进行设置
        self.Edit_ID.setStyleSheet(
            "QLineEdit{color:rgb(0,0,0,255);"  # 字体颜色为黑色
            "font-size:30px;"  # 大小为30 
            "font-family:Roman times;}")  # Roman times字体

        # 对Edit_key字体大小进行设置
        self.Edit_name.setStyleSheet(
            "QLineEdit{color:rgb(0,0,0,255);"  # 字体颜色为黑色
            "font-size:30px;"  # 大小为30
            "font-family:Roman times;}")  # Roman times字体
        # 设置密码隐藏
        # self.Edit_key.setEchoMode(QLineEdit.Password)
        self.lab_sex.setStyleSheet(
            "QLabel{color:rgb(0,0,0,255);"  # 字体颜色为黑色
            "font-size:30px;"  # 大小为30 
            "font-family:Roman times;}")  # Roman times字体

        # 对lab_key字体大小进行设置
        self.lab_parent.setStyleSheet(
            "QLabel{color:rgb(0,0,0,255);"  # 字体颜色为黑色
            "font-size:30px;"  # 大小为30 
            "font-family:Roman times;}")  # Roman times字体

        # 对Edit_ID字体大小进行设置
        self.Edit_sex.setStyleSheet(
            "QLineEdit{color:rgb(0,0,0,255);"  # 字体颜色为黑色
            "font-size:30px;"  # 大小为30 
            "font-family:Roman times;}")  # Roman times字体

        # 对Edit_key字体大小进行设置
        self.Edit_parent.setStyleSheet(
            "QLineEdit{color:rgb(0,0,0,255);"  # 字体颜色为黑色
            "font-size:30px;"  # 大小为30
            "font-family:Roman times;}")  # Roman times字体

        # 对数字按键字体大小进行设置

        # 对登录返回按键字体大小进行设置
        self.btn_logon.setStyleSheet(
            "QPushButton{color:rgb(0,0,0,255);"  # 字体颜色为黑色
            "font-size:30px;"  # 大小为30 
            "font-family:Roman times;}")  # Roman times字体
        self.btn_back.setStyleSheet(
            "QPushButton{color:rgb(0,0,0,255);"  # 字体颜色为黑色
            "font-size:30px;"  # 大小为30 
            "font-family:Roman times;}")  # Roman times字体
        self.btn_edit.setStyleSheet(
            "QPushButton{color:rgb(0,0,0,255);"  # 字体颜色为黑色
            "font-size:30px;"  # 大小为30 
            "font-family:Roman times;}")  # Roman times字体

        # 点击返回按钮事件
        self.btn_back.clicked.connect(self.slot_btn_back)
        # 点击登录按钮事件 (查询)
        self.btn_logon.clicked.connect(self.slot_btn_logon)
        # 存储
        self.btn_edit.clicked.connect(self.slot_btn_edit)

        # 点击数字按钮输入用户名和密码

    # 点击返回按钮事件
    def slot_btn_back(self):
        self.menu = Ui_Menu()
        self.menu.show()
        self.hide()

    def slot_btn_edit(self):
        global data
        if self.Edit_ID.text() in data:
            student = Student(self.Edit_ID.text(), self.Edit_name.text(), "", self.Edit_sex.text(),
                              self.Edit_parent.text())
            data[self.Edit_ID.text()] = student
            self.datafile = open("./datafile.txt", 'wb')
            pickle.dump(data, self.datafile)
            self.datafile.close()

        else:
            QMessageBox.warning(self, "提示", "该人员未注册！", QMessageBox.Close)

    # 点击登录按钮事件
    def slot_btn_logon(self):
        # 判断账号和密码是否输入正确
        global data
        if self.Edit_ID.text() in data:
            self.Edit_name.setText(data[self.Edit_ID.text()].name)
            self.Edit_sex.setText(data[self.Edit_ID.text()].sex)
            self.Edit_parent.setText(data[self.Edit_ID.text()].parent)
        else:
            QMessageBox.warning(self, "提示", "该人员未注册！", QMessageBox.Close)

    # 点击数字按钮输入用户名和密码


# 创建管理人脸数据界面类
class Ui_manager_face(QWidget):
    def __init__(self):
        super(Ui_manager_face, self).__init__()

        # 初始化 ID
        self.ID_num = ""
        self.lab_face = QLabel(self)

        # 初始化进度条定时器
        self.timer = QBasicTimer()
        self.step = 0

        # 创建数字按键

        # 创建容器存放数字键，使用栅格布局

        # 创建groupBox控件
        self.groupBox = QtWidgets.QGroupBox(self)

        # 创建lab_ID控件
        self.lab_ID = QLabel(self.groupBox)
        self.Edit_ID = QLineEdit(self.groupBox)
        self.btn_enter = QPushButton(self.groupBox)
        self.progressBar = QtWidgets.QProgressBar(self.groupBox)
        self.btn_back = QPushButton(self)

        # 创建定时器
        self.timer_camera = QtCore.QTimer()

        # 初始化摄像头数据
        self.camera_init()

        # 初始化界面
        self.init_ui()

        # 显示人脸识别视频界面
        self.face_rec()

        # 定时器函数
        self.timer_camera.timeout.connect(self.show_camera)

        # 点击按钮开启线程
        self.btn_enter.clicked.connect(self.slot_btn_enter)

    # 初始化摄像头数据
    def camera_init(self):
        # 打开设置摄像头对象
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        self.__flag_work = 0
        self.x = 0
        self.count = 0
        self.cap.set(4, 951)  # set Width
        self.cap.set(3, 761)  # set Height

    # 初始化界面
    def init_ui(self):
        self.resize(1280, 800)
        self.lab_face.setGeometry(15, 40, 960, 720)
        self.lab_face.setFrameShape(QtWidgets.QFrame.Box)
        self.lab_face.setText("")
        self.lab_ID.setGeometry(10, 40, 31, 41)

        # 设置容器位置

        # 设置数字键高度

        # 对数字按键字体大小进行设置

        # 对groupBox进行设置
        self.groupBox.setTitle("录入人脸")
        self.groupBox.setGeometry(990, 120, 281, 191)
        self.groupBox.setStyleSheet(
            "QGroupBox {\n"
            "border-width:2px;\n"
            "border-style:solid;\n"
            "border-color:lightGray;\n"
            "font: 75 20pt \"Aharoni\";\n"
            "margin-top: 0.5ex;\n"
            "}\n"
            "QGroupBox::title {\n"
            "subcontrol-origin: margin;\n"
            "subcontrol-position: top left;\n"
            "left:10px;\n"
            "margin-left: 0px;\n"
            "padding:0px;\n"
            "}")

        # 设置groupBox里面的控件
        self.lab_ID.setText("ID")
        self.lab_ID.setGeometry(10, 40, 31, 41)
        self.lab_ID.setStyleSheet("font: 18pt;")

        self.Edit_ID.setGeometry(50, 40, 221, 41)
        self.Edit_ID.setStyleSheet("font: 18pt;")

        self.btn_enter.setText("开始录入")
        self.btn_enter.setGeometry(80, 90, 121, 51)
        self.btn_enter.setStyleSheet("font: 75 16pt;")

        self.progressBar.setGeometry(10, 150, 261, 31)
        # self.progressBar.setProperty("value", 0)

        self.btn_back.setText("返回")
        self.btn_back.setGeometry(1090, 670, 81, 51)
        self.btn_back.setStyleSheet("font: 75 16pt;")

        # 点击数字按钮输入用户名和密码

        # 点击返回按键返回上一界面
        self.btn_back.clicked.connect(self.slot_btn_back)

    # 点击数字按钮输入用户名和密码

    # 点击返回按键返回上一界面
    def slot_btn_back(self):
        self.menu = Ui_Menu()
        self.menu.show()
        self.timer_camera.stop()
        self.cap.release()
        self.hide()

    # 显示人脸识别视频界面
    def face_rec(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(30)
        else:
            self.timer_camera.stop()
            self.cap.release()

    def show_camera(self):
        flag, self.image = self.cap.read()
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(20, 20)
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(self.image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = self.image[y:y + h, x:x + w]

        # 将视频显示在了label上
        show = cv2.resize(self.image, (960, 720))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.lab_face.setPixmap(QtGui.QPixmap.fromImage(showImage))

    # 点击按钮开启线程
    def slot_btn_enter(self):
        self.count = 0
        self.step = 0
        # 创建线程并开启
        self.thread = threading.Thread(target=self.thread_pic)
        self.thread.start()

        # 开启进度条定时器
        self.timer.start(100, self)

    def reflash(self):
        self.progressBar.setProperty("value", self.step)

    # 加载进度条
    def timerEvent(self, e):
        if self.step == 100:
            self.progressBar.setValue(self.step)
            self.timer.stop()
            return
        elif self.step > 58:
            self.progressBar.setValue(self.step)
            return
        self.step = self.count + 1
        self.progressBar.setValue(self.count)

    # 录入人脸线程
    def thread_pic(self):
        print("线程出没！！！")
        print(self.Edit_ID.text())

        # 创建目录，将获取的人脸照片放入指定的文件夹
        self.file = "./Face_data/"

        while (True):
            ret, self.img = self.cap.read()
            # 垂直翻转视频图像
            # 灰度化处理
            gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade2.detectMultiScale(gray, 1.3, 5)

            # 判断是否存在文件夹如果不存在则创建为文件夹
            self.folder = os.path.exists(self.file)
            if not self.folder:
                # makedirs 满权限创建文件时如果路径不存在会创建这个路径
                os.makedirs(self.file)
                os.chmod(self.file, 0o777)

            for (x, y, w, h) in faces:
                cv2.rectangle(self.img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                self.count += 1
                # 将捕获的图像保存到指定的文件夹中
                bool = cv2.imwrite(self.file + "/User." + str(self.Edit_ID.text()) + '.' + str(self.count) + ".png",
                                   gray[y:y + h, x:x + w])

            # 取60张人脸样本，停止录像
            if self.count >= 60:
                print("OK!")
                break
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

        # 函数获取图像和标签数据
        def getImagesAndLabels(path):
            imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
            faceSamples = []
            ids = []
            self.step = 65
            # self.progressBar.setProperty("value", self.step)
            for imagePath in imagePaths:
                # 转换为灰度
                PIL_img = Image.open(imagePath).convert('L')
                img_numpy = np.array(PIL_img, 'uint8')
                id = int(os.path.split(imagePath)[-1].split(".")[1])

                faces = faceCascade3.detectMultiScale(img_numpy)
                for (x, y, w, h) in faces:
                    faceSamples.append(img_numpy[y:y + h, x:x + w])
                    ids.append(id)
            return faceSamples, ids

        self.step = 75
        # self.progressBar.setProperty("value", self.step)
        print("\n [INFO] Training faces. It will take a few seconds. Wait ...")

        # 调用函数，传递文件夹路径参数
        faces, ids = getImagesAndLabels(self.file)
        self.recognizer.train(faces, np.array(ids))
        self.step = 85
        # self.progressBar.setProperty("value", self.step)

        # 创建文件夹
        self.triningfile = "./Face_training/"
        self.folder1 = os.path.exists(self.triningfile)
        if not self.folder1:
            os.makedirs(self.triningfile)
            os.chmod(self.triningfile, 0o777)

        # 将训练好的数据保存到指定文件夹中
        self.recognizer.write(self.triningfile + "/trainer.yml")

        global data
        student = Student(str(self.Edit_ID.text()), "未命名", "", "", "")
        data[self.Edit_ID.text()] = student
        self.datafile = open("./datafile.txt", 'wb')
        pickle.dump(data, self.datafile)
        self.datafile.close()
        print(data)

        # 打印经过训练的人脸编号和结束程序
        print(" [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
        self.step = 100
        # self.progressBar.setProperty("value", self.step)


# 创建人脸识别通用户界面类
class Ui_face_reco(QWidget):
    def __init__(self):
        super(Ui_face_reco, self).__init__()

        # 创建控件
        self.lab_face = QLabel(self)
        self.btn_back = QPushButton(self)
        self.lab_body = QLabel(self)
        self.lab_ID = QLabel(self)
        self.lab_ID_E = QLabel(self)
        self.lab_SEX = QLabel(self)
        self.lab_SEX_E = QLabel(self)
        self.lab_PARENT = QLabel(self)
        self.lab_PARENT_E = QLabel(self)
        self.lab_T_F = QLabel(self)

        # 创建定时器
        self.timer_camera = QtCore.QTimer()
        self.user = []

        # 初始化摄像头数据
        self.camera_init()

        print(data)

        # 初始化界面
        self.init_ui()

        # 点击返回按键返回上一界面
        self.btn_back.clicked.connect(self.slot_btn_back)

        # 显示人脸识别视频界面
        self.face_rec()

        # 定时器函数
        self.timer_camera.timeout.connect(self.show_camera)

        # 将照片显示在lab上

        # self.User = Ui_manager_face()
        # print(self.User.Edit_ID.text())

    def camera_init(self):
        # 打开设置摄像头对象
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        self.__flag_work = 0
        self.x = 0
        self.count = 0
        self.minW = 0.1 * self.cap.get(3)
        self.minH = 0.1 * self.cap.get(4)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

        # 读取训练好的数据
        self.recognizer.read('./Face_training//trainer.yml')
        self.cascadePath = "./haarcascade_frontalface_default.xml"
        self.faceCascade4 = cv2.CascadeClassifier(self.cascadePath);
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    # 初始化界面
    def init_ui(self):
        # 设置控件位置
        self.lab_face.setGeometry(15, 40, 960, 720)
        self.btn_back.setGeometry(1090, 670, 81, 51)
        self.lab_body.setGeometry(1000, 350, 281, 91)
        self.lab_ID.setGeometry(1000, 100, 70, 21)
        self.lab_ID_E.setGeometry(1100, 100, 150, 30)
        self.lab_SEX.setGeometry(1000, 200, 70, 21)
        self.lab_SEX_E.setGeometry(1100, 200, 150, 30)
        self.lab_PARENT.setGeometry(1000, 300, 70, 21)
        self.lab_PARENT_E.setGeometry(1100, 300, 150, 30)
        self.lab_T_F.setGeometry(1060, 450, 171, 81)

        # 设置lab有边框
        self.lab_face.setFrameShape(QtWidgets.QFrame.Box)

        # 设置返回按钮
        self.btn_back.setText("返回")
        self.btn_back.setStyleSheet("font: 75 16pt;")

        self.lab_body.setStyleSheet("font: 75 16pt \"Aharoni\";")
        self.lab_body.setText("身份认证")

        self.lab_ID.setStyleSheet("font: 75 16pt \"Aharoni\";")
        self.lab_ID_E.setStyleSheet("font: 75 16pt \"Aharoni\";")
        self.lab_SEX.setStyleSheet("font: 75 16pt \"Aharoni\";")
        self.lab_SEX_E.setStyleSheet("font: 75 16pt \"Aharoni\";")
        self.lab_PARENT.setStyleSheet("font: 75 16pt \"Aharoni\";")
        self.lab_PARENT_E.setStyleSheet("font: 75 16pt \"Aharoni\";")
        self.lab_T_F.setStyleSheet("font: 75 16pt \"Aharoni\";")

        self.lab_ID.setText("姓名：")
        self.lab_SEX.setText("性别：")
        self.lab_PARENT.setText("亲属：")

    # 点击返回按键返回上一界面
    def slot_btn_back(self):
        self.logon = Ui_Menu()
        self.logon.show()
        self.timer_camera.stop()
        self.cap.release()
        self.hide()

    # 显示人脸识别视频界面
    def face_rec(self):
        # 先对摄像头设备进行检测，没有则弹出提示信息
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(10)
        else:
            self.timer_camera.stop()
            self.cap.release()

    def show_camera(self):

        flag, self.image = self.cap.read()
        # 垂直翻转
        # self.image = cv2.flip(self.image, -1)

        # 将图片变化成灰度图
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # 探测图片中的人脸
        faces = self.faceCascade4.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(self.minW), int(self.minH)),
        )

        # 判断是否检测到人脸，没检测到设置为低电平
        # 检测的时候当矩阵为空的时候能执行代码，当矩阵不为空的时候会有异常，这里将异常抛出
        try:
            if any(faces) == False:
                time.sleep(0.2)

        except Exception as e:
            print(e)

        # faces中的四个量分别为左上角的横坐标、纵坐标、宽度、长度
        for (x, y, w, h) in faces:

            # 围绕脸的框
            cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # 把要分析的面部的捕获部分作为参数，并将返回其可能的所有者，指示其ID以及识别器与该匹配相关的置信度
            id, confidence = self.recognizer.predict(gray[y:y + h, x:x + w])

            # 对置信度进行判断，高于预定值显示出提示信息，并控制GPIO输出高低电平来控制门的开关
            if (confidence < 80):
                # id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
                # GPIO.output(25, GPIO.HIGH)   #GPIO25 输出3.3V
                self.lab_T_F.setText("成功！")
                self.lab_ID_E.setText(data[str(id)].name)
                self.lab_SEX_E.setText(data[str(id)].sex)
                self.lab_PARENT_E.setText(data[str(id)].parent)
                id = data[str(id)].name
                time.sleep(0.05)
            else:
                id = "未知"
                # GPIO.output(25, GPIO.LOW)   #GPIO25 输出0.0V

                confidence = "  {0}%".format(round(100 - confidence))
                self.lab_T_F.setText("失败！")
                self.lab_ID_E.setText("无法识别")
                self.lab_SEX_E.setText("无法识别")
                self.lab_PARENT_E.setText("无法识别")
                time.sleep(0.1)

            img_PIL = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
            font = ImageFont.truetype('font.ttf', 20)
            color = (0, 255, 0, 0)
            position = (x, y)

            draw = ImageDraw.Draw(img_PIL)
            draw.text(position, str(id), font=font, fill=color)
            self.image = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)

            # 给图片添加文本 图片矩阵, 添加文本名称, 设置文本显示位置,
            # 字体样式, 字体大小, 字体颜色, 字体粗细
            # cv2.putText(self.image, str(id), (x + 5, y - 5), self.font, 1, (255, 255, 255), 2)
            cv2.putText(self.image, str(confidence), (x + 5, y + h - 5), self.font, 1, (255, 255, 0), 1)

            # 将视频显示在了label上
        show = cv2.resize(self.image, (960, 720))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.lab_face.setPixmap(QtGui.QPixmap.fromImage(showImage))
        k = cv2.waitKey(10) & 0xff


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Ui_Menu()
    w.show()
    sys.exit(app.exec_())
