import serial
import serial.tools.list_ports
import time

all_port = serial.tools.list_ports.comports()
print("Checking for heaters")

for port in all_port:
    print("*", end="")
    try:
        dev = serial.Serial(port.device, 115200, timeout=4)
        dev.reset_input_buffer()
        time.sleep(2)
        response = dev.readline().decode('utf-8').strip()
        if(response[0:5] == "CNCO2"):
            heater_name = response[6:]
            print("\nFound Heater at " + port.device + ": " + heater_name + "\n")
            

    except serial.serialutil.SerialException:
        print(".", end='')

 
