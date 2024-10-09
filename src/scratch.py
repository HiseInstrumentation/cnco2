import serial
import time
serial_port = "/dev/ttyUSB0"
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate)
time.sleep(2)
print(ser.read_all().decode('utf-8'))
		
ser.write(b'$$\n')
print(ser.read_all().decode('utf-8'))
command = []
command.append(b'G20\n')
command.append(b'G90\n')
command.append(b'G54\n')
command.append(b'G00 X3.0 Y2.0 Z0.4\n')
for c in command:
	print(c)
	ser.write(c)
	time.sleep(2)
	print(ser.read_all().decode('utf-8'))
	time.sleep(1)
