# -*- coding: utf-8 -*-
# Created by HRex on 2020/12/22
import re
import sys
import threading
from time import sleep

from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QApplication, QMainWindow
import serial

import host

from PyQt5 import QtGui, QtWidgets
font = QtGui.QFont()
font.setFamily("Arial") #括号里可以设置成自己想要的其它字体
font.setPointSize(21)   #括号里的数字可以设置成自己想要的字体大小


# Global Variable
portx = 0   #端口号
bps = 0     #波特率
num_data = 0    #数据位
num_stop = 0    #停止位
num_parity_check = 0    #校验位
timex = 0.1   #超时设置
SCS = None
ser = None
SERIAL_STATUS = 0
# Variable ends


def data_send():
    global ser, SERIAL_STATUS
    if SERIAL_STATUS == 1:
        try:
            SCS = time_stage + str(control_stage) + "!"
            print(SCS)
            ui.label_12.setText(SCS)
            # WRITE
            result = ser.write(SCS.encode("utf-8"))
            print("写总字节数:", result)
            ui.label_11.setText("连接成功！")
        except Exception as e:
            ui.label_11.setText("SEND_ERROR!")
    else:
        ui.label_11.setText("串口未开启，发送失败！")

def data_received(thread_name):
    global ser, SERIAL_STATUS
    while True:
        if SERIAL_STATUS == 1:
            ui.label_10.setText("串口已开启，准备接收")
            try:
                if ser.in_waiting:
                    data_from_c51 = ser.read(ser.in_waiting).decode("utf-8")
                    sleep(0.02)
                    print(data_from_c51)
                    ui.textBrowser.insertPlainText(data_from_c51)
            except Exception as e:
                ui.label_10.setText("ERROR!!!!")
            data_from_c51 = None
        else:
            ui.label_10.setText("串口未开启，接收失败")


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

            print(portx, bps, num_data, num_stop, num_parity_check)

            # OPEN SERIES
            ser = serial.Serial(port=portx, baudrate=bps, bytesize=num_data,
                                parity=num_parity_check, stopbits=num_stop, timeout=timex)
            ui.label_9.setText("已连接上"+portx)
            SERIAL_STATUS = 1
        except serial.SerialException:
            ui.label_9.setText("连接"+portx+"失败")
            SERIAL_STATUS = 0
        ui.pushButton.setText("关闭串口")
    else:
        try:
            ser.close()
            ui.label_9.setText("关闭成功")
            ui.pushButton.setText("打开串口")
            SERIAL_STATUS = 0
        except Exception as e:
            ui.label_9.setText("关闭失败")
            SERIAL_STATUS = 1




if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = host.Ui_mainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # Thread
    Received_Thread = threading.Thread(target=data_received, args=("Received_Thread",))
    Received_Thread.start()
    # Set default num
    ui.comboBox.setCurrentIndex(3)
    ui.comboBox_3.setCurrentIndex(0)
    ui.comboBox_4.setCurrentIndex(3)
    ui.comboBox_5.setCurrentIndex(0)
    # Link to the button function
    ui.pushButton.clicked.connect(serial_open)#Open Serial
    #setdata
    ui.textEdit.setFont(font)
    sys.exit(app.exec_())

