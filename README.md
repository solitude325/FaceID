<p align="center">
	<img alt="logo" src="https://avatars.githubusercontent.com/u/56633317?s=48&v=4" height="50px" width="50px">
</p>
<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">FaceI</h1>
<h4 align="center">FaceID人脸识别</h4>

## 技术选型
* PyQt5 + Python3.7 + OpenCV
* 原型来源: https://github.com/oneStarLR/faceReco

## 功能概述
实现人员注册,信息修改,人脸识别获取相关信息

人员信息通过序列化存储在**datafile.txt**文件中

**haarcascade_frontalface_default.xml**是OpenCV中自带的训练模型

**font.ttf**是为了在cv2中显示中文而引入的字体文件

## 运行环境
* Python3.7
* PyQt5
* 开发环境: Windows11 + PyCharm
* 依赖: PyQt5 PyQt5-tools Pillow numpy opencv-python opencv-contrib-python matplotlib
* 打包: pyinstaller

## 用户手册
### 主界面
![](https://s3.bmp.ovh/imgs/2022/09/11/e88953003fe05fe0.png)
### 人脸注册
![](https://s3.bmp.ovh/imgs/2022/09/11/b29e0da5f4c781b6.png)
连续拍摄约60张图片,经灰度处理后进行训练模型,数据保存在**Face_training/trainer.yml**

同时对**datafile**文件重写,持久化用户数据
### 信息编辑
![](https://s3.bmp.ovh/imgs/2022/09/11/4a2c3a6c7236b51c.png)
读取**datafile**文件,实例化为student对象然后修改信息并持久化
### 身份检测
![](https://s3.bmp.ovh/imgs/2022/09/11/6fbb97d513db50a4.png)
通过OpenCV识别人员编号,根据编号确定相关人员信息

## 总结
* 通过Pillow模块对图像进行二次处理解决OpenCV.puttext无法显示中文名称的问题
* 修改ProcessBar的step更新时间,解决程序异常终止的问题
* 通过pickle序列化保存人员身份信息,实现数据持久化
* 使用pyinstaller模块实现exe打包
* 新增人员信息编辑界面

具体实现部分后续将开放在个人博客: https://solitude0325.top
