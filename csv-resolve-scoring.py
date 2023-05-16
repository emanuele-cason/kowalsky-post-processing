import csv
from tkinter import Tk     
from tkinter.filedialog import askopenfilename
from datetime import datetime, time, date, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

TAKEOFF_SPEED = 5
TARGET_ALTITUDE_TIME = 60;

#INDEX
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

#FLIGHT NODES
#   takeoff (speed > TAKEOFF_SPEED)
#   WPT60 (takeoff time + 60s)
#   WPT180 (takeoff time + 180s)

takeoff_occurred = False
takeoff_ignore = False
data_rate = 10

takeoff = ""
takeoff_frame = 0
WPT60 = ""
WPT180 = ""

Tk().withdraw()
file_path = askopenfilename()

if(not ".csv" in file_path):
    print("WARNING! Are you sure you selected a .csv file?")
    input()

def print_node(line, name):
    print(name + " data: " + "\n\t"
             + "Time: " + str(line[1]) + "\n\t"
             + "Altitude: " + str(line[7]) + " m \n\t"
             + "Position: (Lat " + str(line[4]) + ", Lon " + str(line[5]) +  ") \n\t"
             + "Speed: " + str(line[2]) + " km/h \n\t"
             + "Route: " + str(line[10]) + " km \n\t"
             + "Distance: " + str(line[11]) + " m \n\t"
             + "Fixed satellites: " + str(24) + "\n\n")

plot_input = input("Need help finding takeoff moment? [ENTER]/[all](for complete diagnostic)/[no]: ")

if(not plot_input == "no"):

    time_pl = []
    altitude_pl = []
    speed_pl = []
    accel_z_pl = []
    accel_y_pl = []
    accel_x_pl = []
    rx_volt_pl = []
    enl_pl = []
    
    with open(file_path, 'r', encoding='utf16') as csvf:
        reader_pl = csv.reader(csvf, delimiter=';')
        next(reader_pl, None)

        for line_pl in reader_pl:

            try:
                if(datetime.strptime(line_pl[1], '%H:%M:%S') != time_pl[-1]):
                    time_pl.append(datetime.strptime(line_pl[1], '%H:%M:%S'))
                    altitude_pl.append(float(line_pl[7]))
                    speed_pl.append(float(line_pl[2]))
                    accel_z_pl.append(float(line_pl[17]))
                    accel_y_pl.append(float(line_pl[16]))
                    accel_x_pl.append(float(line_pl[15]))
                    rx_volt_pl.append(float(line_pl[9]))
                    enl_pl.append(float(line_pl[18]))
            except:
                time_pl.append(datetime.strptime(line_pl[1], '%H:%M:%S'))
                altitude_pl.append(float(line_pl[7]))
                speed_pl.append(float(line_pl[2]))
                accel_z_pl.append(float(line_pl[17]))
                accel_y_pl.append(float(line_pl[16]))
                accel_x_pl.append(float(line_pl[15]))
                rx_volt_pl.append(float(line_pl[9]))
                enl_pl.append(float(line_pl[18]))

        enl_pl = [y*((sum(rx_volt_pl)/len(rx_volt_pl))/max(enl_pl)) for y in enl_pl]

    
    myFmt = mdates.DateFormatter('%H:%M:%S')
    plt.figure(100)
    plt.gca().xaxis.set_major_formatter(myFmt)        
    plt.plot(time_pl,speed_pl, label = "Speed [km/h]")
    plt.plot(time_pl,altitude_pl, label = "Altitude [m]")
    plt.legend()

    if (plot_input == "all"):
        plt.figure(200)
        plt.gca().xaxis.set_major_formatter(myFmt)
        plt.plot(time_pl,accel_z_pl, label = "Load factor - z axis [m]")
        plt.plot(time_pl,accel_y_pl, label = "Load factor - y axis [m]")
        plt.plot(time_pl,accel_x_pl, label = "Load factor - x axis [m]")
        plt.legend()

        plt.figure(300)
        plt.gca().xaxis.set_major_formatter(myFmt)
        plt.plot(time_pl,rx_volt_pl, label = "RX Voltage [V]")
        plt.plot(time_pl,enl_pl, label = "Engine Noise Level")
        plt.legend()

    plt.show()

with open(file_path, 'r', encoding='utf16') as csvf:
    reader = csv.reader(csvf, delimiter=';')
    next(reader, None)

    prev_line = ""
    frame = 0 #progressive number of line of every second (ex. from 0 to 10 with 10Hz recordings)

    #Flight nodes data fetching
    for line in reader:

        try:
            if(line[1] != prev_line[1]):
                frame = 0
            else:
                frame = frame+1
        except: pass
        
        if(not takeoff_occurred and takeoff_ignore and float(line[2]) <= TAKEOFF_SPEED):
            takeoff_ignore = False
        
        if(float(line[2]) > TAKEOFF_SPEED and not takeoff_occurred and not takeoff_ignore):
            if(input("\nTakeoff detected at time " + str(line[1]) + "\n\t"
                     + "Altitude: " + str(line[7]) + " m \n\t"
                     + "Distance: " + str(line[11]) + " m \n\t"
                     + "Fixed satellites: " + str(24) + "\n"
                     + "is this Dario's takeoff? [ENTER]/[no]: ") == "no"):
                takeoff_ignore = True
            else:
                takeoff_occurred = True
                takeoff_ignore = False
                takeoff = line
                takeoff_frame = frame

        if(takeoff_occurred and datetime.strptime(line[1], '%H:%M:%S') == datetime.strptime(takeoff[1], '%H:%M:%S') + timedelta(0,60) and frame == takeoff_frame):
            WPT60 = line

        if(takeoff_occurred and datetime.strptime(line[1], '%H:%M:%S') == datetime.strptime(takeoff[1], '%H:%M:%S') + timedelta(0,180) and frame == takeoff_frame):
            WPT180 = line
 
        prev_line = line
        
    if (not takeoff_occurred):
        print("ERROR!: No other takeoff detected!")
        input("")
    if (WPT60 == ""):
        print("ERROR!: Waypoint T+60s not found!")
        input("")
    if (WPT180 == ""):
        print("ERROR!: Waypoint T+180s not found!")
        input("")

    #Displaying result
    print("\n------------------------------------------")
    print_node(takeoff, "Takeoff")
    print_node(WPT60, "T+60s")
    print_node(WPT180, "T+180s")

    print("Delta altitude at T+60s: " + str(float(WPT60[7]) - float(takeoff[7])) + " m")
    print("Delta distance between T+60 and T+180 waypoints: "+ str(float(WPT180[10]) - float(WPT60[10])) + " km")
input("")
