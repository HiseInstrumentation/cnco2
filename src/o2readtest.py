import serial
import time

sensor = serial.Serial("/dev/ttyUSB1", 19200)

sensor.write(b'M\n')
time.sleep(2)
print(sensor.read_all().decode('utf-8'))
