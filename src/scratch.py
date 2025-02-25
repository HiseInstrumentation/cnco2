import serial
import time

serial_port = "/dev/ttyUSB0"
baud_rate = 115200

ser = serial.Serial(serial_port, baud_rate)
time.sleep(2)

print(ser.read_all().decode('utf-8'))
		
ser.write(b'$$\n')
time.sleep(3)
print(ser.read_all().decode('utf-8'))
command = []

command.append(b'$5=7\n')
command.append(b'$21=1\n')
command.append(b'$22=1\n')
command.append(b'G21\n')
command.append(b'G90\n')
command.append(b'$H\n')

command.append(b'G00 X1.0 Y1.0\n')
command.append(b'G00 X2.0 Y2.0\n')
command.append(b'G00 X3.0 Y3.0\n')

command.append(b'0x18\n')

for c in command:
	print(c)
		
	ser.write(c)
	time.sleep(2)
	print(ser.read_all().decode('utf-8'))
	time.sleep(3)

ser.reset_output_buffer()
ser.close()
