import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import requests
import serial

arduino_port = 'COM3'
form_class = uic.loadUiType("main.ui")[0]

class WindowClass(QMainWindow, form_class):

    serialFromArduino = serial.Serial(arduino_port, 9600, timeout=1)

    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.run()

        self.btn_2.clicked.connect(self.button1Function)

    def button1Function(self) :
        print("btn_1 Clicked")

    def run(self):
        line = []
        dust_density = 0.0  # [ug/m^3]
        temperature = 0.0  # [C]
        humidity = 0.0  # [%]

        while True:
            # 데이터가 있다면
            for c in self.serialFromArduino.read():
                if not c == 124:  # 아스키코드 |
                    line.append(chr(c))
                if c == 124:
                    tmp = self.parsing_data(line) # 데이터 처리 함수로 호출
                    if 'a' in tmp:
                        tmp = tmp.lstrip()
                        tmp = tmp.replace('a', '')
                        tmp = tmp[:(len(tmp) - 1)]
                        dust_density = tmp
                    elif 'b' in tmp:
                        tmp = tmp.lstrip()
                        tmp = tmp.replace('b', '')
                        tmp = tmp[:(len(tmp) - 1)]
                        temperature = tmp
                    elif 'c' in tmp:
                        tmp = tmp.lstrip()
                        tmp = tmp.replace('c', '')
                        tmp = tmp.replace('-', '')
                        tmp = tmp[:(len(tmp) - 1)]
                        humidity = tmp

                        print(f'----{temperature} {humidity} {dust_density}----')
                        URL = f'http://175.118.126.63/dnsm_dust/api.cfm?temperature={temperature}&humidity={humidity}&dust1={dust_density}&dust2={dust_density}&dust3={dust_density}&idx_location=2'
                        requests.get(URL)
                    del line[:]

    def parsing_data(self, data): # 리스트 구조로 들어 왔기 때문에 작업하기 편하게 스트링으로 합침
        tmp = ''.join(data)
        return tmp


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()