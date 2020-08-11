# RPLIDAR A1M8 Plotting Test With Blitting
# (C) 2020 Alex Whittemore
# Written for the Hackaday Prize 2020 CalEarth Dream Team
# 
# This program collects a point cloud from a SLAMTEC RPLIDAR A1, and looks for an orthogonal wall at theta=0
# If points fall within +/- 3cm of a vertical wall at the same distance as the point at 0 degrees,
# they'll render blue in the feedback plot (in-spec). Otherwise, they'll render red.

# Makes liberal use of the following references:
# 
# This Stack Overflow question about how to efficiently animate a python plot:
# https://stackoverflow.com/questions/40126176/fast-live-plotting-in-matplotlib-pyplot#answer-40139416
#
# How to mask a list, used for separating the "passing" points from the "failing" points in the red/blue visualization
# TL;DR, use a numpy.array, which you can index by another array of true/false values. 
# https://stackoverflow.com/questions/10274774/python-elegant-and-efficient-ways-to-mask-a-list
#
# Other useful references, but not used below:
# Using pyqtgraph to draw a scatter plot:
# https://gist.github.com/Lauszus/16d37c476f24596f8bf43a74847a2fc0

import os
from math import cos, sin, pi, floor, radians
from adafruit_rplidar import RPLidar
import numpy as np
import matplotlib.pyplot as plt
import time

# PARAMETERS

tolerance = 50 # mm, single-sided. For instance, 50 means +/- 5cm

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME)

degree_aligned_scan_data = np.array([0]*360)
scan_angles = np.array(np.radians(range(0, 360)))
pass_fail = np.array([0]*360)

curr_angles = []
curr_radii = []

blit = False

angles = curr_angles
radii = curr_radii

# Validation Models
# Straight Wall
def test_output_wall(scan_angles, scan_data):
    """ Returns a numpy.array of True/False called pass_fail, signifying whether the scan_data array points are correct or not per a wall orthogonal to the 0* baseline."""
    baseline = scan_data[0]
    expected_distances = baseline/np.cos(scan_angles)
    # Basically one big matrix comparison that the scan data is within +/-tolerance of "expected" - populates a numpy array of True/False.
    return (scan_data<expected_distances+tolerance) == (scan_data>expected_distances-tolerance)

def test_output_room(scan_angles, scan_data):
    """ Returns a numpy.array of True/False called pass_fail, signifying whether the scan_data array points are correct or not per a rectangular room of defined height and width."""
    height = 2663 # mm
    width = 3901 # mm

    # Distance at 0 degrees. This is the 0th element in our array, but let's search it more robustly anyway.
    range_to_right = scan_data[scan_angles==0]
    # Similar to above, but this is at 90 degrees = pi/2. This will eventually have to get thresholded in case
    # what exists in the array isn't close enough to equal the target.
    range_to_top = scan_data[scan_angles==(pi/2)]
    range_to_bottom = height-range_to_top
    range_to_left = width-range_to_right

    # Calculate angle boundaries between the different zones.
    # Upper right
    angle_boundary_u_r = np.arctan(range_to_top/range_to_right)
    angle_boundary_u_l = pi-np.arctan(range_to_top/range_to_left)
    angle_boundary_l_l = pi+np.arctan(range_to_bottom/range_to_left)
    angle_boundary_l_r = 2*pi-np.arctan(range_to_bottom/range_to_right)

    # Preallocate a list of expected distances that we'll fill in.
    expected_distances = np.array([0]*len(scan_angles))

    # Test only the right-hand wall.
    # The right wall is all angles >lower right and <upper right.
    mask = np.logical_or(scan_angles<angle_boundary_u_r, scan_angles>angle_boundary_l_r)
    expected_distances[mask] = range_to_right/np.cos(scan_angles)[mask]
    # Test only the ceiling. Rotate all angles right by pi/2
    mask = np.logical_and(scan_angles>angle_boundary_u_r, scan_angles<angle_boundary_u_l)
    expected_distances[mask] = range_to_top/np.cos(scan_angles-(pi/2))[mask]
    # Test only the left-hand wall. Rotate all angles right by pi
    mask = np.logical_and(scan_angles>angle_boundary_u_l, scan_angles<angle_boundary_l_l)
    expected_distances[mask] = range_to_left/np.cos(scan_angles-(pi))[mask]
    # Test only the floor. Rotate all angles right by 3pi/2
    mask = np.logical_and(scan_angles>angle_boundary_l_l, scan_angles<angle_boundary_l_r)
    expected_distances[mask] = range_to_bottom/np.cos(scan_angles-(3*pi/2))[mask]
    return (scan_data<expected_distances+tolerance) == (scan_data>expected_distances-tolerance)


    # We'll assume 0* is the distance to the right wall and 90* is the distance to the ceiling.


fig = plt.figure(figsize=(8, 6), dpi=200)
ax1 = plt.subplot(111, projection='polar')
ax1.set_rmax(10000)
ax1.set_rticks([])

sweep_g, = ax1.plot([],[], marker='.', markersize=0.5, color='b', linestyle='None')
sweep_b, = ax1.plot([],[], marker='.', markersize=0.5, color='r', linestyle='None')

text = ax1.text(3*pi/8,10000, "")

fig.canvas.draw()   # note that the first draw comes before setting data 


if blit:
    # cache the background
    axbackground = fig.canvas.copy_from_bbox(ax1.bbox)

plt.show(block=False)


t_start = time.time()
k=0.
i = 0
def redraw():
    global i,k,curr_angles,curr_radii,degree_aligned_scan_data,scan_angles
    i+=1
    sweep_g.set_data(list(scan_angles[pass_fail==1]), list(degree_aligned_scan_data[pass_fail==1]))
    sweep_b.set_data(list(scan_angles[pass_fail!=1]), list(degree_aligned_scan_data[pass_fail!=1]))
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
        ax1.draw_artist(sweep_g)
        ax1.draw_artist(sweep_b)
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

def process_data(data):
    # print(data[0])
    # for n in range(len(pass_fail)):
    #     dist = degree_aligned_scan_data[n]
    #     expected = dist_at_angle(n, degree_aligned_scan_data[0])
    #     pass_fail[n] = 1 if ((dist<expected+tolerance) and dist>(expected-tolerance)) else 0
    # print(pass_fail[:20])
    global pass_fail
    pass_fail = test_output_room(scan_angles, degree_aligned_scan_data)
    redraw()

try:
    print(lidar.info)
    for scan in lidar.iter_scans():
        #curr_angles = [x[1] for x in scan]
        #curr_radii = [x[2] for x in scan]
        for (_, angle, distance) in scan:
            degree_aligned_scan_data[min([359, floor(angle)])] = distance
        process_data(degree_aligned_scan_data)
except KeyboardInterrupt:
    print('Stoping.')
lidar.stop()
lidar.disconnect()
