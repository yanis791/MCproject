# -*- coding: utf-8 -*-
# Created by HRex on 2020/12/22
import re
import sys
import threading
import time
from time import sleep
from math import *
from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QApplication, QMainWindow
import serial
from PyQt5.Qt import *
from pyqtgraph import PlotWidget
from PyQt5 import QtCore
import numpy as np
import pyqtgraph as pq
import host

# Global Variable
portx = 0  # 端口号
bps = 0  # 波特率
num_data = 0  # 数据位
num_stop = 0  # 停止位
num_parity_check = 0  # 校验位
timex = 0.1  # 超时设置
SCS = None
ser = None
SERIAL_STATUS = 0
curve = None
data = None
# Variable ends

def data_solve(serData):
    global data
    x = int.from_bytes(serData[1:3], byteorder='big', signed=False)
    y = int.from_bytes(serData[3:5], byteorder='big', signed=False)
    z = int.from_bytes(serData[5:7], byteorder='big', signed=False)

    x = x*4 / 65536
    y = y*4 / 65536
    z = z*4 / 65536
    if x>2 :
        x-=4
    if y>2 :
        y-=4
    if z > 2:
        z -= 4

    print(x, y, z)
    theta_x = atan(x / sqrt(y * y + z * z)) * 180 / pi
    theta_y = atan(y / sqrt(x * x + z * z)) * 180 / pi
    theta_z = atan(z / sqrt(y * y + x * x)) * 180 / pi

    ui.lcdNumber.display(format(theta_x, '.1f'))
    ui.lcdNumber_2.display(format(theta_y, '.1f'))
    ui.lcdNumber_3.display(format(theta_z, '.1f'))

    if len(data)<300:
        data[len(data)] = theta_x
    else:
        data[:-1] = data[1:]
        data[-1] = theta_x


def data_received(thread_name):
    global ser, SERIAL_STATUS
    while True:
        if SERIAL_STATUS == 1:
            try:
                if not ser.in_waiting:
                    ui.label_10.setText("串口接收中...")
                if ser.in_waiting:
                    data_from_c51 = bytes()
                    data_from_c51 = ser.read(10)  # .decode("utf-8")
                    data_solve(data_from_c51)
                    sleep(0.02)
            except Exception as e:
                try:
                    ui.label_10.setText("ERROR!!!!")
                except Exception as e:
                    pass
            data_from_c51 = None
        else:
            try:
                ui.label_10.setText("串口未开启")
            except Exception as e:
                pass


def serial_open():
    global ser, SERIAL_STATUS
    if SERIAL_STATUS == 0:
        try:
            # DATA PROCEED
            portx = ui.comboBox_2.currentText()
            bps = ui.comboBox.currentText()
            num_data = ui.comboBox_4.currentText()
            if num_data == "5": num_data = serial.FIVEBITS
            if num_data == "6": num_data = serial.SIXBITS
            if num_data == "7": num_data = serial.SEVENBITS
            if num_data == "8": num_data = serial.EIGHTBITS
            num_stop = ui.comboBox_3.currentText()
            if num_stop == "1": num_stop = serial.STOPBITS_ONE
            if num_stop == "1.5": num_stop = serial.STOPBITS_ONE_POINT_FIVE
            if num_stop == "2": num_stop = serial.STOPBITS_TWO
            num_parity_check = ui.comboBox_5.currentText()
            if num_parity_check == "无校验": num_parity_check = serial.PARITY_NONE
            if num_parity_check == "奇校验": num_parity_check = serial.PARITY_ODD
            if num_parity_check == "偶校验": num_parity_check = serial.PARITY_EVEN

            # OPEN SERIES
            ser = serial.Serial(port=portx, baudrate=bps, bytesize=num_data,
                                parity=num_parity_check, stopbits=num_stop, timeout=timex)
            print(portx, bps, num_data, num_stop, num_parity_check)
            ui.serial_now.setText("已连接上" + portx)
            SERIAL_STATUS = 1
        except serial.SerialException:
            ui.serial_now.setText("连接" + portx + "失败")
            SERIAL_STATUS = 0
        ui.pushButton.setText("关闭串口")
    else:
        try:
            ser.close()
            ui.serial_now.setText("关闭成功")
            ui.pushButton.setText("打开串口")
            SERIAL_STATUS = 0
        except Exception as e:
            ui.serial_now.setText("关闭失败")
            SERIAL_STATUS = 1

# 数据左移
def update_data():
    global data,curve
    data[:-1] = data[1:]
    data[-1] = np.random.normal()
    # 数据填充到绘制曲线中
    curve.setData(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = host.Ui_mainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # Thread
    Received_Thread = threading.Thread(target=data_received, args=("Received_Thread",))
    Received_Thread.setDaemon(True)
    Received_Thread.start()
    # Set default num
    ui.comboBox.setCurrentIndex(3)
    ui.comboBox_2.setCurrentIndex(2)
    ui.comboBox_3.setCurrentIndex(0)
    ui.comboBox_4.setCurrentIndex(0)
    ui.comboBox_5.setCurrentIndex(0)
    # Link to the button function
    ui.pushButton.clicked.connect(serial_open)  # Open Serial
    #plot
    plt = PlotWidget()
    ui.verticalLayout.addWidget(plt)
    plt.setGeometry(QtCore.QRect(25, 25, 550, 550))
    # # 仿写 mode1 代码中的数据
    # # 生成 300 个正态分布的随机数
    # data = np.random.normal(size=300)
    # curve = plt.plot(data, name="mode1")
    # # 设定定时器,绑定 update_data 函数
    # timer = pq.QtCore.QTimer()
    # timer.timeout.connect(update_data)
    # timer.start(50)

    sys.exit(app.exec_())
