import serial
import time

if __name__ == '__main__':

        # Open up serial to heater
        port = "/dev/ttyUSB0"
        heater = serial.Serial(port, 115200, timeout=3)
        heater.reset_input_buffer()
        time.sleep(2)

        response = heater.readline().decode('utf-8').strip()
        print(response)
        if(response[0:5] == "CNCO2"):
                print("\nFound Heater at " + port + "\n")
                heater.reset_input_buffer()
                heater.write(b'start 45')
                time.sleep(1)
                response = heater.readline().decode('utf-8').strip()

                while True:
                        response = heater.readline().decode('utf-8').strip()
                        if(response != ""):
                                print(response)
                        else:
                                print(".")
        else:
                print("\nNo heater found at " + port + "\n")


