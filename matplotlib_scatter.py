import numpy as np
import matplotlib.pyplot as plt

# Fixing random state for reproducibility
#np.random.seed(19680801)


N = 50
x = np.random.rand(N)
y = np.random.rand(N)
colors = np.random.rand(N)
area = (30 * np.random.rand(N))**2  # 0 to 15 point radii

plt.scatter(x, y, s=area, c=colors, alpha=0.5)
plt.show()

# draw the figure so the animations will work
fig = plt.gcf()
fig.show()
fig.canvas.draw()

while True:
    x = np.random.rand(N)
    y = np.random.rand(N)
    plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    #plt.pause(0.01)  # I ain't needed!!!
    fig.canvas.draw()