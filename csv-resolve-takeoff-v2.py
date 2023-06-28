import csv
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from datetime import datetime, time, date, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backend_bases import MouseButton


def thrust_P_WT(v):
    return (
        (1924372607210241 * v**3) / 9223372036854775808
        - (2146875790398649 * v**2) / 144115188075855872
        - (247125505414387 * v) / 2251799813685248
        + 4090701349013563 / 281474976710656
    )


def prop_P_6000(v):
    return (
        (7452174069988735 * v**15) / 19807040628566084398385987584
        - (1411576336712313 * v**14) / 19342813113834066795298816
        + (7467788127410425 * v**13) / 1208925819614629174706176
        - (2878032578356725 * v**12) / 9444732965739290427392
        + (5794986302310945 * v**11) / 590295810358705651712
        - (8063401666702695 * v**10) / 36893488147419103232
        + (7981140027021897 * v**9) / 2305843009213693952
        - (177727621249703 * v**8) / 4503599627370496
        + (1457441243828713 * v**7) / 4503599627370496
        - (8482489163130903 * v**6) / 4503599627370496
        + (4259704092479997 * v**5) / 562949953421312
        - (1406817603285175 * v**4) / 70368744177664
        + (8998878264340199 * v**3) / 281474976710656
        - (7510614484268341 * v**2) / 281474976710656
        + (7576506330183035 * v) / 562949953421312
        + 7469326223227113 / 2305843009213693952
    )


def prop_P_7200(v):
    return (
        (6689020810040607 * v**15) / 158456325028528675187087900672
        - (3040852157647053 * v**14) / 309485009821345068724781056
        + (4826188434542003 * v**13) / 4835703278458516698824704
        - (4463949822096019 * v**12) / 75557863725914323419136
        + (5392961454667059 * v**11) / 2361183241434822606848
        - (4502404287431999 * v**10) / 73786976294838206464
        + (5347766124979759 * v**9) / 4611686018427387904
        - (2286460274945703 * v**8) / 144115188075855872
        + (5624981068362727 * v**7) / 36028797018963968
        - (4910713538337547 * v**6) / 4503599627370496
        + (5918504390372919 * v**5) / 1125899906842624
        - (586396811579855 * v**4) / 35184372088832
        + (9002298828327761 * v**3) / 281474976710656
        - (281755089599931 * v**2) / 8796093022208
        + (5457158143667673 * v) / 281474976710656
        + 6457195838750757 / 1152921504606846976
    )


def prop_P_8539(v):
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


# WIND TUNNEL
def prop_P_WT(v):
    return (
        (596806206510041 * v) / 35184372088832
        - (1764926744503765 * v**2) / 4503599627370496
        - (4201288066369975 * v**3) / 2305843009213693952
        - 1931954908392021 / 281474976710656
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
plt.xlabel("Time [s]")
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
plt.xlabel("Time [s]")
plt.ylabel("Acceleration [g]")
plt.plot(time_s_set, accel_z_set, label="z axis")
plt.plot(time_s_set, accel_y_set, label="y axis")
plt.plot(time_s_set, accel_x_set, label="x axis")
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

mass = float(input("Enter total mass: "))


def to_distance_estimate(step):
    integral = 0
    prev_v = -1
    for index in range(to_start_index, to_rotate_index + 1, step):
        v = speed_set[index]

        if prev_v != -1 and prop_P_WT(v) != 0:
            integral = integral + ((1 / prop_P_WT(v)) * (v**2) * (v - prev_v))

        prev_v = v
    print(
        "Expected takeoff distance (step = " + str(step) + "): " + str(integral * mass)
    )


def to_speed_estimate(step):
    integral = 0
    prev_v = -1
    for index in range(to_start_index, to_rotate_index + 1, step):
        v = speed_set[index]

        if prev_v != -1 and prop_P_WT(v) != 0:
            integral = integral + ((1 / prop_P_WT(v)) * (v**2) * (v - prev_v))

        if (integral * mass) > to_distance:
            print(
                "Expected takeoff speed (step = "
                + str(step)
                + "): "
                + str(speed_set[index])
            )
            break

        prev_v = v


def to_resulting_force(step):
    F_net = []
    v_axis = []
    prev_v = -1
    for index in range(to_start_index, to_rotate_index + 1, step):
        v = speed_set[index]

        if prev_v != -1:
            F_i = mass * (v - prev_v) / (step * 0.1)
            F_net.append(F_i)
            v_axis.append(v)

        prev_v = v

    T_a = [thrust_P_WT(v) for v in v_axis]

    plt.plot(v_axis, F_net, label="Net force [N] (step = " + str(step) + "): ")
    plt.plot(v_axis, T_a, label="Thrust force [N]")
    plt.legend()


# Risulta che mediando ogni intervallino si ha la stessa curva della funzione precedente
def to_resulting_force_v2(step):
    F_net = []
    F_avg = 0
    v_avg = 0
    v_axis = []
    prev_v = -1
    for index in range(to_start_index, to_rotate_index + 1):
        v = speed_set[index]
        v_avg = v_avg + v

        if prev_v != -1:
            F_avg = F_avg + (mass * (v - prev_v) / (0.1))

        if (index - to_start_index) % step == 0:
            F_net.append(F_avg / step)
            v_axis.append(v_avg / step)
            F_avg = 0
            v_avg = 0

        prev_v = v

    T_a = [thrust_P_WT(v) for v in v_axis]

    plt.plot(v_axis, T_a, label="T - Wind tunnel")
    plt.plot(v_axis, F_net, label="R - GPS (step = " + str(step) + "): ")
    plt.legend()


# PROVVISORIA
# Controllare asse (x o y) accelerometro e segno
def to_resulting_force_acc():
    F_net = []
    v_axis = []
    acc = -accel_x_set[to_start_index]
    for index in range(to_start_index, to_rotate_index + 1):
        v = speed_set[index]
        acc = acc * (0.85) - accel_x_set[index] * 0.15

        F_i = mass * acc * 9.81
        F_net.append(F_i)
        v_axis.append(v)

    # T_a = [thrust_P_WT(v) for v in v_axis]

    plt.plot(v_axis, F_net, label="Accelerometer [N]: ")
    # plt.plot(v_axis, T_a, label="Thrust force [N]")
    plt.legend()


def to_resulting_force_acc_v2(step):
    F_net = []
    acc_avg = 0
    v_avg = 0
    v_axis = []
    for index in range(to_start_index, to_rotate_index + 1):
        v_avg = v_avg + speed_set[index]
        acc_avg = acc_avg + accel_x_set[index]

        if (index - to_start_index) % step == 0:
            F_net.append(mass * (acc_avg / step) * 9.806)
            v_axis.append(v_avg / step)
            acc_avg = 0
            v_avg = 0

    plt.plot(
        v_axis,
        F_net,
        label="R - Accelerometer (step = " + str(step) + "): ",
    )
    plt.legend()


to_distance_estimate(1)
to_distance_estimate(2)
to_distance_estimate(3)
to_distance_estimate(4)
to_distance_estimate(5)
print("Real takeoff distance: " + str(to_distance))

to_speed_estimate(1)
to_speed_estimate(2)
to_speed_estimate(3)
to_speed_estimate(4)
to_speed_estimate(5)
print("Real takeoff speed: " + str(to_speed))

plt.figure(101)
plt.ylabel("Force [N]")
plt.xlabel("Speed [m/s]")
to_resulting_force_v2(5)
to_resulting_force_acc_v2(5)
plt.xlim([0, speed_set[to_rotate_index]])
plt.ylim([0, 15])
plt.show()
