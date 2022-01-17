import threading
import time
from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
# seed the pseudorandom number generator


xs = [0] #store trials here (n)
ys = [0] #store relative frequency here

fps = 30 #target frames per second
ms_per_frame = 60/fps
keep_running = True

def receive_data():
    #subscribe to serial event here instead of initializing the random seed
    from random import seed
    from random import random
    seed(1)
    while(keep_running):
        time.sleep(0.01) # this may be too long, I don't have a good concept of the time involved here
        
        # remove this next part! this is just for testing.
        # in reality, we're going to subscribe to the serial port event and then loop forever while doing nothing here
        for _ in range(6):
            xs.append(random())
            ys.append(random())

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