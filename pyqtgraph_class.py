import sys
import time
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg


class App(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)

        # Set white background and black foreground
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        # Create the view
        self.view = pg.PlotWidget()
        self.view.resize(800, 600)
        self.view.setWindowTitle('Scatter plot fps=')
        self.view.setAspectLocked(True)
        self.view.show()

        self.scatter = pg.ScatterPlotItem(pen=pg.mkPen(width=5, color='r'), symbol='o', size=1)
        self.view.addItem(self.scatter)

        self.counter = 0
        self.fps = 0.
        self.lastupdate = time.time()

        #### Start  #####################
        self._update()

    def _update(self):

        # Generate random points
        n = 1000
        #print('Number of points: ' + str(n))
        self.data = np.random.normal(size=(2, n))
        self.pos = [{'pos': self.data[:, i]} for i in range(n)]
        self.scatter.setData(self.pos)

        now = time.time()
        dt = (now-self.lastupdate)
        if dt <= 0:
            dt = 0.000000000001
        fps2 = 1.0 / dt
        self.lastupdate = now
        self.fps = self.fps * 0.9 + fps2 * 0.1
        tx = 'Scatter plot fps:  {fps:.3f} FPS'.format(fps=self.fps )
        self.view.setWindowTitle(tx)
        QtCore.QTimer.singleShot(1, self._update)
        self.counter += 1


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    thisapp = App()
    thisapp.show()
    
    sys.exit(app.exec_())
