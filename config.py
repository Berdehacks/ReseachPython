import time
import serial


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

# configuration commands and description
# prettier-ignore


configComands = ['']*8
# Minimum interval between +UUDF events for each tag in milliseconds.
configComands[0] = 'AT+UDFCFG=1,50'
# User defined string that can be set to any value.
configComands[1] = 'AT+UDFCFG=2,""'
configComands[2] = 'AT+UDFCFG=3,1'  # Angle calculations enabled at startup.
configComands[3] = 'AT+UDFCFG=4,""'  # Anchor ID.
# Configure if the anchor is to calculate both azimuth and elevation angles.
configComands[4] = 'AT+UDFCFG=5,1'
# Do post processing of the angle. It is advisable to keep this enabled.
configComands[5] = 'AT+UDFCFG=8,1'
configComands[6] = 'AT+UDFCFG=11,20'  # Fixed smoothing factor.
configComands[7] = 'AT+UDFENABLE=1'

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='COM7',
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

while 1:
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

        print(response.__dict__)
