import os
from math import cos, sin, pi, floor, radians
from adafruit_rplidar import RPLidar
import numpy as np
import matplotlib.pyplot as plt
from drawnow import drawnow, figure
import time

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME)

scan_data = [0]*360
pass_fail = [0]*20

curr_angles = []
curr_radii = []

figure()
frames = 0
start_time = time.time()

def draw_fig():
    global frames, start_time
    frames += 1
    title = 'Frame Rate: {fps:.3f}FPS'.format(fps= ((frames) / (time.time() - start_time)) ) 
    plt.gcf().clf()
    #plt.polar(np.linspace(0,2*pi,num=360), scan_data)

    ax = plt.subplot(111, projection='polar')
    ax.scatter(np.radians(curr_angles), curr_radii, s=1)#, c=(['g']*45+['r']*315))
    ax.set_rmax(10000)
    #ax.set_rticks([0.5, 1, 1.5, 2])  # Less radial ticks
    #ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
    #ax.grid(True)
    ax.set_title(title, va='bottom')
    #plt.show()

def dist_at_angle(angle, baseline):
    return baseline/cos(radians(angle))

def process_data(data):
    print(data[0])
    for n in range(len(pass_fail)):
        dist = scan_data[n]
        expected = dist_at_angle(n, scan_data[0])
        pass_fail[n] = 1 if ((dist<expected+20) and dist>(expected-20)) else 0
    print(pass_fail)

try:
    print(lidar.info)
    for scan in lidar.iter_scans():
        curr_angles = [x[1] for x in scan]
        curr_radii = [x[2] for x in scan]
        drawnow(draw_fig)
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
        process_data(scan_data)
except KeyboardInterrupt:
    print('Stoping.')
lidar.stop()
lidar.disconnect()
