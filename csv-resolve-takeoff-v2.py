import csv
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from datetime import datetime, time, date, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backend_bases import MouseButton


def prop_P(v):
    return (
        (6914260054825037 * v**15) / 1267650600228229401496703205376
        - (465975034830941 * v**14) / 309485009821345068724781056
        + (438546751597867 * v**13) / 2417851639229258349412352
        - (3848533357633813 * v**12) / 302231454903657293676544
        + (2757069114498035 * v**11) / 4722366482869645213696
        - (5459705683898567 * v**10) / 295147905179352825856
        + (3845400541620467 * v**9) / 9223372036854775808
        - (7799509199559873 * v**8) / 1152921504606846976
        + (355565129980795 * v**7) / 4503599627370496
        - (5890296412221353 * v**6) / 9007199254740992
        + (4209679236237963 * v**5) / 1125899906842624
        - (7914493034490199 * v**4) / 562949953421312
        + (9006155510541971 * v**3) / 281474976710656
        - (1337187439795785 * v**2) / 35184372088832
        + (7678943032343733 * v) / 281474976710656
        + 5388791348096689 / 576460752303423488
    )


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
route_set = []
accel_z_set = []
accel_y_set = []
accel_x_set = []

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
        route_set.append(float(line[10]) * 1000)
        accel_z_set.append(float(line[17]))
        accel_y_set.append(float(line[16]))
        accel_x_set.append(float(line[15]))

        prev_line = line

time_s_set = [item - time_set[0] for item in time_set]
time_s_set = [item.total_seconds() for item in time_s_set]

# PLOT ARE PRODUCED
plt.figure(100)
plt.plot(time_s_set, speed_set, label="Speed [m/s]")
plt.plot(time_s_set, altitude_set, label="Altitude [m]")
plt.legend()


def on_move(event):
    if event.inaxes:
        global x_coord
        x_coord = event.xdata


def on_click(event):
    global to_start_time
    global to_rotate_time

    if event.button is MouseButton.RIGHT:
        if "to_start_time" in globals() and not "to_rotate_time" in globals():
            to_rotate_time = x_coord
            plt.axvline(x=to_rotate_time, color="r")
            plt.draw()
        if "to_start_time" not in globals():
            to_start_time = x_coord
            plt.axvline(x=to_start_time, color="g")
            plt.draw()
        if "to_start_time" in globals() and "to_rotate_time" in globals():
            plt.disconnect(binding_id)


binding_id = plt.connect("motion_notify_event", on_move)
plt.connect("button_press_event", on_click)

plt.show()

plt.figure(200)
plt.plot(time_s_set, accel_z_set, label="Acceleration - z axis [g]")
plt.plot(time_s_set, accel_y_set, label="Acceleration - y axis [g]")
plt.plot(time_s_set, accel_x_set, label="Acceleration - x axis [g]")
plt.legend()
plt.axvline(x=to_start_time, color="g")
plt.axvline(x=to_rotate_time, color="r")
plt.draw()
plt.show()

# Find nearest indexes
to_start_index = min(
    range(len(time_s_set)), key=lambda i: abs(time_s_set[i] - to_start_time)
)
to_rotate_index = min(
    range(len(time_s_set)), key=lambda i: abs(time_s_set[i] - to_rotate_time)
)

to_distance = route_set[to_rotate_index] - route_set[to_start_index]
to_speed = speed_set[to_rotate_index]
print("Real takeoff distance: " + str(to_distance))

""" integral = 0
index = to_start_index
for v in speed_set[to_start_index : to_rotate_index + 1]:
    integral = integral + ((1 / prop_P(v)) * (v**2) * (v - speed_set[index - 1]))
    index = index + 1
print("Integral: " + str(integral)) """

mass = float(input("Enter total mass: "))

integral = 0
index = to_start_index
for v in speed_set[to_start_index : int(to_rotate_index * 1.1)]:
    integral = integral + ((1 / prop_P(v)) * (v**2) * (v - speed_set[index - 1]))
    index = index + 1

    print(integral * mass)
    if (integral * mass) > to_distance:
        print("Expected takeoff speed: " + str(speed_set[index]))
        break

print("Real takeoff speed: " + str(to_speed))
