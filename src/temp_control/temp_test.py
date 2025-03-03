import serial
import time
import serial.tools.list_ports


class System:
        heater_dev = []
        
        def get_heater(self):
                port = '/dev/ttyUSB0'

                heater = serial.Serial(port, 115200, timeout=3)
                heater.reset_input_buffer()
                time.sleep(4)
                
                response = heater.readline().decode('utf-8').strip()
                if(response[0:5] == "CNCO2"):
                        dev = device()
                        dev.serial = heater
                        print("\nFound Heater at " + port + "\n")
                        dev.serial.reset_input_buffer()
                        dev.serial.write(b'start 45')
                        time.sleep(1)
                        response = dev.serial.readline().decode().strip()
                        self.heater_dev.append(dev)
                        
                        
                else:
                        print("\nNo heater found at " + port + "\n")
                

class device:
        serial = None
        
        def getTemp(self):
                self.serial.write(b'stat')
                time.sleep(1)
                response = self.serial.readline().decode('utf-8').strip()


if __name__ == '__main__':
        sys = System()
        sys.get_heater()

        while True:
                for devs in sys.heater_dev:
                        devs.serial.write(b'stat')
                        time.sleep(1)
                        response = devs.serial.readline().decode('utf-8').strip()
                        if(response != ""):
                                print(response)
                        else:
                                print(".")


