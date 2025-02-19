import serial
import time
import re

sensor = serial.Serial("/dev/ttyUSB2", 19200)

time.sleep(2);

while True:
	sensor.write(b'M\n')
	time.sleep(2)
	ret_str = sensor.read_all().decode('utf-8')
	# print(ret_str)

	regex_o2 = "^[0-9]*\.[0-9]*"
	regex_te = "[0-9]*\.[0-9]*\B"
	regex_pr = "[0-9]{4}|[0-9]{3}"
			

	o2 = re.search(regex_o2, ret_str).group()
	temp = re.search(regex_te, ret_str).group()
	pressure = re.search(regex_pr, ret_str).group()

	print("Returned: " + o2 + " : " + temp + " : " + pressure )
