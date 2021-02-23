"""
# name: dataplot
# brief: read data from txt and plot with cursor
# author: zxx
# date: 2021.02.23
"""

import numpy as np
import pandas as pd
# import torch
# from torch.autograd import Variable
# import torch.nn.functional as F
import os
import matplotlib.pyplot as plt


class Cursor(object):
    def __init__(self, ax):
        self.ax = ax
        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line

        # text location in axes coords
        self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)

    def mouse_move(self, event):
        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        plt.draw()


class SnaptoCursor(object):
    """
    Like Cursor but the crosshair snaps to the nearest x,y point
    For simplicity, I'm assuming x is sorted
    """

    def __init__(self, ax, x, y):
        self.ax = ax
        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line
        self.x = x
        self.y = y
        # text location in axes coords
        self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)

    def mouse_move(self, event):
        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata

        indx = min(np.searchsorted(self.x, [x])[0], len(self.x) - 1)
        x = self.x[indx]
        y = self.y[indx]
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        print('x=%1.2f, y=%1.2f' % (x, y))
        plt.draw()


data_path = os.path.abspath(os.getcwd()) + '/data_res'
print(data_path)
file_name = os.listdir(data_path)
print(file_name)

# for file in file_name:
#     file_path = data_path + '/' + file
#     data = np.genfromtxt(file_path, delimiter='\t', skip_header=4)
#     print(data)

file_path = data_path + '/' + file_name[3]
data = np.genfromtxt(file_path, delimiter=' ', skip_header=1)
print(data.shape)

fig, ax = plt.subplots()
t = np.arange(0, data.shape[0], 1)
print(t)
data[:, 44] *= 10

# plt.subplot(3, 1, 1)
# plt.plot(t, data[:, [26, 29, 44]])      # 角度
# plt.legend(['left', 'right', 'state'])
# plt.title('angle')
# plt.grid()
# plt.subplot(3, 1, 2)
# plt.plot(t, data[:, [30, 33, 44]])      # 角速度
# plt.legend(['left', 'right', 'state'])
# plt.title('gyro')
# plt.grid()
# plt.subplot(3, 1, 3)
# plt.plot(t, data[:, [37, 40, 44]])      # 电机电流
# plt.legend(['left', 'right', 'state'])
# plt.title('motor_current')
# plt.grid()

# data[:, [36, 39]] /= 50
# data[:, [0, 6]] /= 17
# data[:, 44] *= 3
# plt.subplot(2, 1, 1)
# plt.plot(t, data[:, [0, 30, 36, 44]])      # mpu角速度&电机速度
# plt.legend(['raw_gyro', 'kalman_gyro', 'motor_rpm', 'state'])
# plt.title('left')
# plt.subplot(2, 1, 2)
# plt.plot(t, data[:, [6, 33, 39, 44]])      # mpu角速度&电机速度
# plt.legend(['raw_gyro', 'kalman_gyro', 'motor_rpm', 'state'])
# plt.title('right')

plt.plot(data[:, [12, 13, 14]])

cursor = Cursor(ax)
# cursor = SnaptoCursor(ax, t, s)
plt.connect('motion_notify_event', cursor.mouse_move)

plt.show()
