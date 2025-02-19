import serial
import serial.tools.list_ports
import time

all_port = serial.tools.list_ports.comports()
print("Scanning for components")

for port in all_port:
    print(port.device)

    try:
        # First connect at 115200 for temp controllers and gantry
        dev = serial.Serial(port.device, 115200, timeout=3)
        dev.reset_input_buffer()
        time.sleep(2)
        response = dev.readline().decode('utf-8').strip()
        if(response[0:5] == "CNCO2"):
            device_name = response[6:]
            print("\nFound temp controller at " + port.device + ": " + device_name + "\n")
        else:
            dev.write(b'?\n')
            time.sleep(1)
            response = dev.readline().decode('utf-8').strip()
            if(response[0:5] == "<Idle"):
               print("\nFound Gantry at " + port.device + "\n")

        dev.close()

        # Second connect at 19200 for o2 sensor
        dev = serial.Serial(port.device, 19200, timeout=4)
        dev.reset_input_buffer()
        time.sleep(2)
        dev.write(b'I\n')
        time.sleep(1.5)
        response = dev.readline().decode('utf-8').strip()
        if(response[0:9] == "ID:Oxygen"):
            heater_name = response[6:]
            print("\nFound O2 at " + port.device + "\n")

        dev.close()

    except UnicodeDecodeError:
        continue
    except serial.serialutil.SerialException:
        print(".", end='')

 
