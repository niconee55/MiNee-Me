import serial
import time

num = ["0","1","2","3","4","5"]

# Give data to arduino serial
arduino = serial.Serial(port='COM5', baudrate=31250, timeout=.1)
time.sleep(2)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    data = arduino.readline().decode()
    return data

for i in num:
    value = write_read(i)
    print(value)