import serial
import time

sensor = serial.Serial("/dev/ttyUSB1", 19200)

sensor.write(b'M\n')
time.sleep(2)
ret_str = sensor.read_all().decode('utf-8')
print(ret_str)
vals = ret_str.split(",")
print(vals)
