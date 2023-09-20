import time
import serial


configComands = ['']*7


# prettier-ignore
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

out = ''
out = out.encode('utf-8')

for command in configComands:
    yinput = command
    ser.write(yinput.encode('utf-8'))
    time.sleep(2)
    while ser.inWaiting() > 0:
        out += ser.read()

    if out != '':
        print(">>" + out.decode('utf-8'))
        if 'ERROR' in out.decode('utf-8'):
            print('Error confuguring target')
            ser.close()
            exit()

while 1:
    x = ser.readline()
    print(x)
