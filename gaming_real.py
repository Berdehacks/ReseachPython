import time
import serial
from datetime import datetime
import csv
import numpy as np
import matplotlib.pyplot as plt

plt.axis([0, 10, 0, 1])

plt.axis('equal')


def cotan(x):
    return 1.0 / np.tan(x)


class ValidResponse:
    def __init__(
        self,
        response_list
    ):
        self.found_id = response_list[0]
        self.rssi = response_list[1]
        self.azimuth = response_list[2]
        self.elevation = response_list[3]
        self.na = response_list[4]
        self.channel = response_list[5]
        self.anchor_id = response_list[6]
        self.user_defined_str = response_list[7]
        self.timestamp_ms = response_list[8]
        self.periodic_event_counter = response_list[9]


# esperamos [1.7, 2.75, 0]

beacons_positions = {
    "6C1DEBAFB644": np.array([3, 0]),
    "6C1DEBAFB3B5": np.array([0, 0])
}


def get_relative_position(beaconA: ValidResponse, beaconB: ValidResponse):
    A = beacons_positions[beaconA.found_id]
    B = beacons_positions[beaconB.found_id]

    Ax, Ay = (A[0], A[1])
    Bx, By = (B[0], B[1])

    phi1 = np.deg2rad(beaconA.elevation)
    theta1 = np.deg2rad(beaconA.azimuth)

    phi2 = np.deg2rad(beaconB.elevation)
    theta2 = np.deg2rad(beaconB.azimuth)

    up = cotan(theta1) * (By - Ay) - Bx + Ax
    down = np.cos(theta2) - cotan(theta1) * np.sin(theta2)

    new_r2 = up / down

    B_e = np.array([
        new_r2 * np.cos(theta2),
        new_r2 * np.sin(theta2)
    ])

    return B + B_e


header = ['id', 'rssi', 'azimuth', 'elevation', 'na', 'channel',
          'anchor_id', 'user_defined_str', 'timestamp_ms', 'periodic_event_counter']
now = datetime.now()
date = now.strftime("%d-%m-%Y %H-%M-%S")

filename = 'data_log/'+date+'.csv'
# Create csv file

with open(filename, 'w') as dataFile:
    csv_writer = csv.writer(dataFile, lineterminator='\n')

    csv_writer.writerow(header)
    # configuration commands and description

    configComands = [
        # Minimum interval between +UUDF events for each tag in milliseconds.
        'AT+UDFCFG=1,50'
        # User defined string that can be set to any value.
        'AT+UDFCFG=2,""',
        # Angle calculations enabled at startup.
        'AT+UDFCFG=3,1',
        'AT+UDFCFG=4,""',  # Anchor ID.
        # Configure if the anchor is to calculate both azimuth and elevation angles.
        'AT+UDFCFG=5,0',
        # Do post processing of the angle. It is advisable to keep this enabled.
        'AT+UDFCFG=8,0',
        'AT+UDFCFG=11,0',  # Fixed smoothing factor.
        'AT+UDFENABLE=1',
        'AT+&w',
        'AT+cpwroff',
        'AT+UDFCFG=5,0',
        'AT+UDFENABLE=1',
    ]

    # configure the serial connections (the parameters differs on the device you are connecting to)
    ser = serial.Serial(
        port='COM8',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        rtscts=True
    )
    ser.isOpen()

    # Loop for sending configuraton commands to antenna board.
    for command in configComands:
        yinput = command + "\r"
        ser.write(yinput.encode('utf-8'))

        out = ''
        out = out.encode('utf-8')

        time.sleep(1)
        while ser.inWaiting() > 0:
            out += ser.read()

        if (out.decode('utf-8') == "OK" or "ERROR"):
            print(out.decode('utf-8'))
        # if out != b'':
        #     print(">>" + out.decode('utf-8'))
        #     if 'ERROR' in out.decode('utf-8'):
        #         print('Error confuguring target')
        #         ser.close()
        #         exit()

    # keeps serial port open listening to angle reports
    last_found_unique_beacon_data = {}

    timer_start = time.time()
    curr_counter = 0
    curr_sum = 0

    found_angles = {
        "6C1DEBAFB644": [[], []],
        "6C1DEBAFB3B5": [[], []]
    }

    t = 0

    while True:
        t += 1
        x = ser.readline().decode('utf-8')
        responses = x.split(",")
        for i in range(len(responses)):
            try:
                responses[i] = int(responses[i])
            except:
                pass

        id_start_index = responses[0].find(":")

        if id_start_index != -1:
            responses[0] = responses[0][id_start_index + 1:]

        if len(responses) == 10:
            response = ValidResponse(responses)
            # print('validresponse')

            data = [response.found_id, response.rssi, response.azimuth, response.elevation, response.na, response.channel,
                    response.anchor_id, response.user_defined_str, response.timestamp_ms, response.periodic_event_counter]

            last_found_unique_beacon_data[response.found_id] = response

            if len(data) == 10:
                csv_writer.writerow(data)

            f = 0
            if len(last_found_unique_beacon_data) == 2:
                found_angles[response.found_id][0].append(response.azimuth)
                found_angles[response.found_id][1].append(response.elevation)
                f = get_relative_position(
                    last_found_unique_beacon_data["6C1DEBAFB644"], last_found_unique_beacon_data["6C1DEBAFB3B5"])
                print(response.found_id, response.azimuth, response.elevation)
                print(f)
            else:
                print(response.found_id, response.azimuth, response.elevation)

        if time.time() - timer_start > 5:
            plt.clf()
            # print("average =", curr_sum / curr_counter)
            timer_start = time.time()
            # curr_sum = 0
            # curr_counter = 0

            # plt.xlim([-45, 45])
            # plt.ylim([-45, 45])

            print(found_angles)
            try:
                plt.scatter(found_angles["6C1DEBAFB644"][0], np.random.rand(
                    len(found_angles["6C1DEBAFB644"][0])), c='red')
                plt.scatter(found_angles["6C1DEBAFB3B5"][0], np.random.rand(
                    len(found_angles["6C1DEBAFB3B5"][0])), c='blue')
                plt.scatter(np.average(
                    found_angles["6C1DEBAFB3B5"][0]), np.random.random(), c='blue', marker="*")
                plt.scatter(np.average(
                    found_angles["6C1DEBAFB644"][0]), np.random.random(), c='red', marker="*")
            except:
                pass

            found_angles = {
                "6C1DEBAFB644": [[], []],
                "6C1DEBAFB3B5": [[], []]
            }

        #     plt.plot(t, f, "*")

        plt.pause(0.05)
    plt.show()
