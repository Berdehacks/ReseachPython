import time
import serial

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

print('Enter your commands below.\r\nInsert "exit" to leave the application.')

quantity = ser.inWaiting

while 1:
    # get keyboard input
    #input = raw_input(">> ")
    # Python 3 users'
    yinput = input(">>")
    yinput = yinput + '\r\n'

    if input == 'exit':
        ser.close()
        exit()
    else:
        # send the character to the device
        # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
        ser.write(yinput.encode('utf-8'))
        out = ''
        out = out.encode('utf-8')
        # let's wait one second before reading output (let'sat give device time to answer)
        time.sleep(1)
        while ser.inWaiting() > 0:
            out += ser.read()

        if out != '':
            print(">>" + out.decode('utf-8'))
