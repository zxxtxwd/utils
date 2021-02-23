"""
# name: witmotionmpu_driver
# brief: read accel data from witmotion module by uart
# author: zxx
# date: 20201124
"""

import time
import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
from drawnow import *


class Motion:
    ACCX = []
    ACCY = []
    ACCZ = []

    def __init__(self):
        port_list = list(serial.tools.list_ports.comports())
        print(port_list)
        if len(port_list) == 0:
            print('无可用串口')
        else:
            for i in range(0, len(port_list)):
                print(port_list[i])
        # 端口，GNU / Linux上的/ dev / ttyUSB0 等 或 Windows上的 COM3 等
        portx = "COM7"
        # 波特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
        bps = 115200
        # 超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
        timex = 0.1
        # 打开串口，并得到串口对象
        self.ser = serial.Serial(portx, bps, timeout=timex)
        print(self.ser.port)  # 获取到当前打开的串口名
        print(self.ser.baudrate)  # 获取波特率

        for i in range(1000):
            self.ACCX.append(0)
            self.ACCY.append(0)
            self.ACCZ.append(0)

    def __del__(self):
        time.sleep(1)
        print("del")
        self.ser.close()  # 关闭串口

    def datatoshort(self, a):
        if a & 0x8000 == 0x8000:
            b = bin(a)
            c = b[2:18]

            vv = []
            for i in c:
                if i == '1':
                    v = 0
                    vv.append(v)
                else:
                    v = 1
                    vv.append(v)
            # print(vv)
            s = ''
            for i in vv:
                s += str(i)
            aa = int(s, 2)
            c = ~aa
            # print(c)
        else:
            c = a
        return c

    def getAcc(self, header, id, length):
        res = self.ser.read(length)
        # print(res)
        # print("rec：", res.hex())
        crc = self.calcrc(res, length - 1)
        # print("crc:", res[length - 1], "crc_cal:", crc)
        # print("res[1]:", res[1], "header:", header)
        if not res[0] == header:    # 0x55
            print("ERROR: data need align")
            self.align(0x55, 11)       # 数据重新对齐
            return False
        if not res[1] == id:    # 0x51
            print("ERROR: data is not accel")
            return False
        if crc == res[length - 1]:
            accx = res[3] << 8 | res[2]
            accy = res[5] << 8 | res[4]
            accz = res[7] << 8 | res[6]

            accx_short = self.datatoshort(accx)
            accy_short = self.datatoshort(accy)
            accz_short = self.datatoshort(accz)
            # print("accx:", accx_short, "accy:", accy_short, "accz:", accz_short)
            # print("---------------")
            return True, accx_short, accy_short, accz_short
        else:
            print("ERROR: data crc error")
            return False

    def align(self, header, length):
        align_flag = False
        while not align_flag:
            res_s = self.ser.read(1)
            # print(res_s, res_s.hex())
            if res_s[0] == header:  # 0x55":
                res_e = self.ser.read(length - 1)
                res = res_s + res_e
                # print(res_s, res_s.hex())
                # print(res_e, res_e.hex())
                # print(res, res.hex())
                crc = self.calcrc(res, length - 1)
                # print("crc:", res[length - 1], "crc_cal:", crc)
                if crc == res[length - 1]:
                    align_flag = True
                    print("Data successfully aligned!")

    def calcrc(self, data, length):
        crc = 0
        for i in range(length):
            crc += data[i]

        crc = crc & 0xFF
        return crc

    def show(self):
        plt.title('accel data')
        plt.grid(True)
        plt.plot(self.ACCX, 'r', label='accel_x')
        plt.plot(self.ACCY, 'g', label='accel_y')
        plt.plot(self.ACCZ, 'b', label='accel_z')
        plt.legend(loc='upper right')

    def start(self):
        # 模块发数据是0x51、0x54两个数据包交替发送，所以要读两次才有一次加速度的数据包
        self.align(0x55, 11)    # 数据包帧头为0x55， accel数据包长度为11
        while True:
            self.getAcc(0x55, 0x51, 11)  # 数据包帧头为0x55，accel命令字为0x51， 包长度为11
            [isvalid, accx, accy, accz] = self.getAcc(0x55, 0x51, 11)
            if isvalid:
                self.ACCX.append(accx)
                self.ACCX.pop(0)
                self.ACCY.append(accy)
                self.ACCY.pop(0)
                self.ACCZ.append(accz)
                self.ACCZ.pop(0)
                # drawnow(self.show)    # 加上画图延时会特别大
                print("accx:", accx, "accy:", accy, "accz:", accz)
                print("---------------")


mt = Motion()

if __name__ == "__main__":
    mt.start()
