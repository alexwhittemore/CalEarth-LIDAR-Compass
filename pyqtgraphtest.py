#!/usr/bin/python3
#
# Scatter plot example using pyqtgraph with PyQT5
#
# Install instructions for Mac:
#   brew install pyqt
#   pip3 install pyqt5 pyqtgraph
#   python3 pyqtgraph_pyqt5.py

import sys

import numpy as np
import pyqtgraph as pg
import time

# Set white background and black foreground
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

# Generate random points
n = 1000
print('Number of points: ' + str(n))
data = np.random.normal(size=(2, n))

# Create the main application instance
app = pg.mkQApp()

# Create the view
view = pg.PlotWidget()
view.resize(800, 600)
view.setWindowTitle('Scatter plot using pyqtgraph with PyQT5')
view.setAspectLocked(True)
view.show()

# Create the scatter plot and add it to the view
scatter = pg.ScatterPlotItem(pen=pg.mkPen(width=5, color='r'), symbol='o', size=1)
view.addItem(scatter)

# Convert data array into a list of dictionaries with the x,y-coordinates
pos = [{'pos': data[:, i]} for i in range(n)]


while 1:
    now = pg.ptime.time()
    scatter.setData(pos)
    print("Plot time: {} sec".format(pg.ptime.time() - now))
    data = np.random.normal(size=(2, n))
    pos = [{'pos': data[:, i]} for i in range(n)]
    time.sleep(1)


# Gracefully exit the application
sys.exit(app.exec_())