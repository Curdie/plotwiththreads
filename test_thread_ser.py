#!/usr/bin/env python
import threading
import time
from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
import serial

#initialize serial port
ser = serial.Serial()
ser.port = '/dev/ttyUSB0' #Arduino serial port
ser.baudrate = 19200
ser.timeout = 10 #specify timeout when using readline()
ser.open()
if ser.is_open==True:
	print("\nAll right, serial port now open. Configuration:\n")
	print(ser, "\n") #print serial parameters
xs = [0] #store trials here (n)
ys = [0] #store relative frequency here
I=0
xx=0
yy=0

xs = [0] #store trials here (n)
ys = [0] #store relative frequency here

fps = 30 #target frames per second
ms_per_frame = 60/fps
keep_running = True

def receive_data():
    while(keep_running):
        #Aquire and parse data from serial port
        line=ser.readline()      #ascii
        line_as_list = line.split(b',')
        xx = float(line_as_list[0])/125
        yy = float(line_as_list[1])/250000
        print(str(I) + "  " + str(line) + "  " + str(xx) + "  " + str(yy) + "  " + str(ser.in_waiting))   
        # Add x and y to lists
        xs.append(xx)
        ys.append(yy)
        I=I+1
        time.sleep(0.01) # this may be too long, I don't have a good concept of the time involved here

class MyWidget(pg.GraphicsWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100) # in milliseconds
        self.timer.start()
        self.timer.timeout.connect(self.onNewData)

        self.plotItem = self.addPlot(title="V/I Pairs")

        self.plotDataItem = self.plotItem.plot([], pen=None, 
            symbolBrush=(255,255,255), symbolSize=10, symbolPen=None)

    def onNewData(self):
        self.plotDataItem.setData(xs, ys)

def main():
    print("Entered Main")
          
    app = QtWidgets.QApplication([])

    pg.setConfigOptions(antialias=False) # True seems to work as well

    win = MyWidget()
    win.show()
    win.resize(1500,1000) 
    win.raise_()
 
    app.exec_()


if __name__ == "__main__":
    # create and start a separate thread for serial port data
    receiving_thread = threading.Thread(target=receive_data)
    receiving_thread.start()
    # start the ui
    main()
    # now that the UI has closed, break the loop in the receiving thread
    keep_running = False