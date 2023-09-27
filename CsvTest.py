import time
import serial
from datetime import datetime
import csv
import numpy as np
import matplotlib.pyplot as plt

plt.axis([0, 10, 0, 1])

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

beacons_positions = {
    "6C1DEBAFB644": np.array([0, 0]),
    "6C1DEBAFB3B5": np.array([5, 0])
}

def get_relative_position(beaconA: ValidResponse, beaconB: ValidResponse):
    if (beaconA.found_id in beacons_positions) and (beaconB.found_id in beacons_positions):
        alpha = np.deg2rad(90 - np.abs(beaconA.azimuth))
        beta = np.deg2rad(90 - np.abs(beaconB.azimuth))
        gamma = np.deg2rad(np.abs(beaconA.azimuth) + np.abs(beaconB.azimuth))

        c = np.linalg.norm(beacons_positions[beaconA.found_id] - beacons_positions[beaconB.found_id])

        b = (c * np.sin(beta)) / np.sin(gamma)
        f = np.sin(alpha) * b

        # print(beaconA.azimuth, beaconB.azimuth, f)
        return f
    else:
        return "Not valid ids"

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

    configComands = ['']*8
    # Minimum interval between +UUDF events for each tag in milliseconds.
    configComands[0] = 'AT+UDFCFG=1,50'
    # User defined string that can be set to any value.
    configComands[1] = 'AT+UDFCFG=2,""'
    # Angle calculations enabled at startup.
    configComands[2] = 'AT+UDFCFG=3,1'
    configComands[3] = 'AT+UDFCFG=4,""'  # Anchor ID.
    # Configure if the anchor is to calculate both azimuth and elevation angles.
    configComands[4] = 'AT+UDFCFG=5,1'
    # Do post processing of the angle. It is advisable to keep this enabled.
    configComands[5] = 'AT+UDFCFG=8,1'
    configComands[6] = 'AT+UDFCFG=11,20'  # Fixed smoothing factor.
    configComands[7] = 'AT+UDFENABLE=1'

    # configure the serial connections (the parameters differs on the device you are connecting to)
    ser = serial.Serial(
        port='COM5',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        rtscts=True
    )
    ser.isOpen()

    # Loop for sending configuraton commands to antenna board.
    for command in configComands:
        yinput = command
        ser.write(yinput.encode('utf-8'))

        out = ''
        out = out.encode('utf-8')

        time.sleep(1)
        while ser.inWaiting() > 0:
            out += ser.read()

        print(out.decode('utf-8'))
        if out != b'':
            print(">>" + out.decode('utf-8'))
            if 'ERROR' in out.decode('utf-8'):
                print('Error confuguring target')
                ser.close()
                exit()

    # keeps serial port open listening to angle reports
    last_found_unique_beacon_data = {}

    timer_start = time.time()
    curr_counter = 0
    curr_sum = 0
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
                f = get_relative_position(last_found_unique_beacon_data["6C1DEBAFB644"], last_found_unique_beacon_data["6C1DEBAFB3B5"])
                curr_sum += f
                curr_counter += 1
            else:
                print(response.found_id, response.azimuth, response.elevation)

        if time.time() - timer_start > 1:
            print("average =", curr_sum / curr_counter)
            timer_start = time.time()
            curr_sum = 0
            curr_counter = 0

            plt.plot(t, f, "*")

        plt.pause(0.05)
    plt.show()