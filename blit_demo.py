import time
from matplotlib import pyplot as plt
import numpy as np


def live_update_demo(blit = True):
    angles = [45, 135, 225, 315]
    radii = [5000,5000,5000,5000]
    
    fig = plt.figure()
    ax1 = plt.subplot(111, projection='polar')
    ax1.set_rmax(10000)
    ax1.set_rticks([])

    sweep, = ax1.plot([],[])

    text = ax1.text(0.8,0.5, "")

    fig.canvas.draw()   # note that the first draw comes before setting data 


    if blit:
        # cache the background
        axbackground = fig.canvas.copy_from_bbox(ax1.bbox)

    plt.show(block=False)


    t_start = time.time()
    k=0.

    for i in np.arange(1000):
        sweep.set_data(np.radians(angles)+(.01*i), radii)
        ax1.set_rmax(10000)
        ax1.set_rticks([5000, 10000])
        tx = 'Mean Frame Rate:\n {fps:.3f}FPS'.format(fps= ((i+1) / (time.time() - t_start)) ) 
        text.set_text(tx)
        #print tx
        k+=0.11
        if blit:
            # restore background
            fig.canvas.restore_region(axbackground)

            # redraw just the points
            ax1.draw_artist(sweep)
            ax1.draw_artist(text)

            # fill in the axes rectangle
            fig.canvas.blit(ax1.bbox)

            # in this post http://bastibe.de/2013-05-30-speeding-up-matplotlib.html
            # it is mentionned that blit causes strong memory leakage. 
            # however, I did not observe that.

        else:
            # redraw everything
            fig.canvas.draw()

        fig.canvas.flush_events()
        #alternatively you could use
        #plt.pause(0.000000000001) 
        # however plt.pause calls canvas.draw(), as can be read here:
        #http://bastibe.de/2013-05-30-speeding-up-matplotlib.html


live_update_demo(True)   # 175 fps
#live_update_demo(False) # 28 fps