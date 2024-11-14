import serial
import time

if __name__ == '__main__':

        # Open up serial to heater
        heater = serial.Serial("/dev/ttyUSB0", 9600)
        heater.reset_input_buffer()
        time.sleep(5)

        # Write something to it


        # Read something from it
        while True:
                heater.write(b'testy\n')
                time.sleep(2)
                response = heater.readline().decode('utf-8').strip()
                if(response != ""):
                        print("\nResponse:")
                        print("\n"+response+"\n")


