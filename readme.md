# Hackaday Prize 2020 CalEarth Dream Team LIDAR Compass

As part of the Hackaday Prize 2020, the CalEarth Dream Team is developing a LIDAR-based cross-sectional profilometer to make construction of SuperAdobe domes easier and less time-consuming.

Dome construction typically requires some kind of measurement device to ensure that the correct profile is being followed layer-by-layer. The LIDAR Compass concept is designed to take a 2D dimensioned drawing corresponding to the cross-section of such a dome, and measure an as-built dome during construction on the job site for comparision to the 2D design. Where reality matches the design, the device projects a visible red laser line. If everything's in the right place, you should see one continuous red-line sweep of your construction. If a bag is out of place, it will remain dark.

## Code

As it stands, this code is extremely messy. At time of writing, the most relevant file is `lidar_mpl_blit.py` which implements LIDAR data collection, plotting, and pass/fail checking for a simple wall. The other files are due for reorganization or removal - all are basically just intermediate tests and trials.