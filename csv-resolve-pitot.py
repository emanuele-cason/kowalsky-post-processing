import csv
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from datetime import datetime, time, date, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backend_bases import MouseButton

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

import math

# INDEX
#   date = 0
#   time = 1
#   speed = 2 [km/h]
#   MSL altitude = 3 [m]
#   latitude = 4
#   longitude = 5
#   altitude = 7 [m]
#   RX voltage = 9 [V]
#   route = 10 [km]
#   distance = 11 [m]
#   satellites = 24
#   accel x = 15 [g]
#   accel y = 16 [g]
#   accel z = 17 [g]
#   engine noise level = 18

Tk().withdraw()
file_path = askopenfilename()

if not ".csv" in file_path:
    print("WARNING! Are you sure you selected a .csv file?")
    input()

print("File selected: " + file_path)

time_set = []
time_s_set = []  # Secondi dall'avvio della registrazione
altitude_set = []
speed_set = []

# FILE IS OPEN AND ALL DATA LOADED
with open(file_path, "r", encoding="utf16") as csvf:
    reader = csv.reader(csvf, delimiter=";")
    next(reader, None)

    prev_line = ""
    frame = 0

    for line in reader:
        if prev_line != "":
            if line[1] != prev_line[1]:
                frame = 0
            else:
                frame = frame + 1

        time_set.append(
            datetime.strptime(line[1] + "." + str(frame * 100000), "%H:%M:%S.%f")
        )
        altitude_set.append(float(line[7]))
        speed_set.append(float(line[2]) / 3.6)

        prev_line = line

time_s_set = [item - time_set[0] for item in time_set]
time_s_set = [item.total_seconds() for item in time_s_set]

plt.figure(100)
plt.xlabel("Time [s]")
plt.ylabel("GPS Speed [m/s]")
plt.plot(time_s_set, speed_set)


def on_move(event):
    if event.inaxes:
        global x_coord
        x_coord = event.xdata


def on_click(event):
    global to_start_time

    if event.button is MouseButton.RIGHT:
        to_start_time = x_coord
        plt.axvline(x=to_start_time, color="g")
        plt.draw()
        plt.disconnect(binding_id)


binding_id = plt.connect("motion_notify_event", on_move)
plt.connect("button_press_event", on_click)

plt.show()

Tk().withdraw()
file_path_pitot = askopenfilename()

if not ".csv" in file_path_pitot:
    print("WARNING! Are you sure you selected a .csv file?")
    input()

print("File selected: " + file_path_pitot)

pitot_time_set = []
pitot_press_set = []

# FILE IS OPEN AND ALL DATA LOADED
with open(file_path_pitot, "r", encoding="utf8") as csvf:
    reader = csv.reader(csvf, delimiter=";")
    next(reader, None)

    for line in reader:
        pitot_time_set.append(float(line[0]) / 1000)
        pitot_press_set.append(float(line[2]))


pitot_press_set_avg = signal.savgol_filter(pitot_press_set, 100, 3)

plt.figure(100)
plt.xlabel("Time [s]")
plt.ylabel("Delta pressure")
plt.plot(pitot_time_set, pitot_press_set_avg)


def on_move(event):
    if event.inaxes:
        global x_coord
        x_coord = event.xdata


def on_click(event):
    global pitot_to_start_time

    if event.button is MouseButton.RIGHT:
        pitot_to_start_time = x_coord
        plt.axvline(x=pitot_to_start_time, color="g")
        plt.draw()
        plt.disconnect(binding_id)


binding_id = plt.connect("motion_notify_event", on_move)
plt.connect("button_press_event", on_click)

plt.show()

print(to_start_time)
print(pitot_to_start_time)

pitot_time_set = [
    item - (pitot_to_start_time - to_start_time) for item in pitot_time_set
]
pitot_speed_set = [
    math.sqrt((item * 13789.5144) / 1.2247) for item in pitot_press_set_avg
]

plt.figure(100)
plt.xlabel("Time [s]")
plt.ylabel("Speed [m/s]")
plt.plot(time_s_set, speed_set, label="GPS")
plt.plot(pitot_time_set, pitot_speed_set, label="Pitot tube")
plt.legend()


def on_move(event):
    if event.inaxes:
        global x_coord
        x_coord = event.xdata


def on_click(event):
    global time_A
    global time_B

    if event.button is MouseButton.RIGHT:
        if "time_A" in globals() and not "time_B" in globals():
            time_B = x_coord
            plt.axvline(x=time_B, color="r")
            plt.draw()
        if "time_A" not in globals():
            time_A = x_coord
            plt.axvline(x=time_A, color="g")
            plt.draw()
        if "time_A" in globals() and "time_B" in globals():
            plt.disconnect(binding_id)


binding_id = plt.connect("motion_notify_event", on_move)
plt.connect("button_press_event", on_click)

plt.show()

pitot_index_A = 0
pitot_index_B = 0

for i in range(0, len(pitot_time_set)):
    if pitot_index_A == 0 and pitot_time_set[i] >= time_A:
        pitot_index_A = i

    if pitot_index_A != 0 and pitot_index_B == 0 and pitot_time_set[i] >= time_B:
        pitot_index_B = i

gps_index_A = 0
gps_index_B = 0

for i in range(0, len(time_set)):
    if gps_index_A == 0 and time_s_set[i] >= time_A:
        gps_index_A = i

    if gps_index_A != 0 and gps_index_B == 0 and time_s_set[i] >= time_B:
        gps_index_B = i

gps_speed_avg = 0
pitot_speed_avg = 0

for i in range(pitot_index_A, pitot_index_B):
    pitot_speed_avg = pitot_speed_avg + pitot_speed_set[i]
pitot_speed_avg = pitot_speed_avg / (pitot_index_B - pitot_index_A)

for i in range(gps_index_A, gps_index_B):
    gps_speed_avg = gps_speed_avg + speed_set[i]
gps_speed_avg = gps_speed_avg / (gps_index_B - gps_index_A)

print(gps_speed_avg)
print(pitot_speed_avg)

pitot_speed_set = [item + (gps_speed_avg - pitot_speed_avg) for item in pitot_speed_set]

plt.figure(100)
plt.xlabel("Time [s]")
plt.ylabel("Speed [m/s]")
plt.plot(time_s_set, speed_set, label="GPS")
plt.plot(pitot_time_set, pitot_speed_set, label="Pitot tube")
plt.legend()
plt.show()
