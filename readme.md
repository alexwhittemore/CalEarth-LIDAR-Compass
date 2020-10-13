# Hackaday Prize 2020 CalEarth Dream Team LIDAR Compass

As part of the Hackaday Prize 2020, the CalEarth Dream Team is developing a LIDAR-based cross-sectional profilometer to make construction of SuperAdobe domes easier and less time-consuming.

Dome construction typically requires some kind of measurement device to ensure that the correct profile is being followed layer-by-layer. The LIDAR Compass concept is designed to take a 2D dimensioned drawing corresponding to the cross-section of such a dome, and measure an as-built dome during construction on the job site for comparision to the 2D design. Where reality matches the design, the device projects a visible red laser line. If everything's in the right place, you should see one continuous red-line sweep of your construction. If a bag is out of place, it will remain dark.

This Raspberry Pi-based component relies on an Arduino component at https://github.com/alexwhittemore/CalEarth_Compass_Feedback_Laser for laser feedback.

## Code

As it stands, this code is extremely messy. At time of writing, the most relevant file is `lidar_mpl_blit_laser.py` which implements LIDAR data collection, plotting, and pass/fail checking for a simple wall and a square room. The other files are due for reorganization or removal - all are basically just intermediate tests and trials.

## Installation Instructions

1. Bring up a raspberry pi using Noobs with the latest Raspberry Pi OS
1. Open a terminal
1. `git clone https://github.com/alexwhittemore/CalEarth-LIDAR-Compass.git python_lidar`
1. sudo apt-get install python3-numpy
1. `pip3 install -r requirements.txt`

## Using

1. Run `python3 lidar_mpl_blit_laser.py`

## Current Status

The current functionality amounts to a functional proof-of-concept.

- [x] Collect LIDAR data
- [x] Calculate expected ranges for simple use-cases (wall, square room)
- [ ] DXF-based calculation for arbitrary geometry
- [ ] DXF upload
- [x] Visible laser feedback based on measurement 
- [x] Software-plotted feedback including pass/fail

All of the key features are implemented and functional, but lack polish and accuracy. Certain aspects are in need of functional improvement.

## Operational Overview

The LIDAR module returns data in the form of <angle, range> pairs. The measurement angle is an arbitrary decimal value - wherever the LIDAR happens to be at that moment the range was measured. There is no guarantee any particular angle will ever be measured, and no guarantee a previously measured range remains accurate. That is, assuming "every angle ever measured is still accurate" allows the application to achieve high angular resolution as measurements fill in the circle. On the other hand, assuming that only RECENT measurements remain valid limits the spatial resolution available to the application.

The current implementation revolves around an array of 360 values, one per degree of a full circle. All measurements are rounded to the nearest degree, and expected range is calculated on the basis of the rounded degree. Naturally, this makes processing much more simple and avoids the need for "garbage cleaning" stale values, communicating arbitrary timings/angles to the feedback laser, and so on. On the other hand, it may also reduce accuracy substantially, both in terms of feedback and unnderlying calculation. 

As sample values stream in from the LIDAR, they're thresholded into this 360-degree array. After each packet of measurements, the array is processed and measured values are compared to expected values per the model to create a pass/fail array, true where the range at X degree is as-expected, and false where it's out of bounds (more than some threshold away from expected, as set in the code). 

This pass/fail array is sent via serial to the laser feedback module, and at the same time the measurement array is used to plot a polar diagram of measurements, colorized by the pass/fail array for software-based feedback. This is mostly for debugging, but at present is very revealing. 

## Areas of improvement

* Thresholding angular measurements to the nearest degree is a source of inaccuracy, and re-architecting around data as-measured offers lots of room for improvement. 
* A higher sample-rate LIDAR could make the overall system more immediately responsive by filling in all angles much faster than the current LIDAR, which might take a few rotations to "hit" on the angle of interest.
* Spinning the LIDAR faster could create a smoother image of the feedback laser, rather than it appearing to blink quickly. 
* Future: Add automatic rotation