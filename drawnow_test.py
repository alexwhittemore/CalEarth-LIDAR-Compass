import numpy as np
import matplotlib.pyplot as plt
from drawnow import drawnow, figure


figure()
def draw_fig():
    N = 50
    x = np.random.rand(N)
    y = np.random.rand(N)
    plt.scatter(x, y)

while 1:
    drawnow(draw_fig)