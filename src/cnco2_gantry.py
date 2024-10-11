'''
    Copyright 2024, Hise Scientific Instrumentation, LLC

    cnco2_gantry.py

    Purpose:
    Gantry rack system abstraction
'''

class Gantry:
    def initilize():
        serial_port = "/dev/ttyUSB0"
        baud_rate = 115200
        ser = serial.Serial(serial_port, baud_rate)
        time.sleep(2)
        print(ser.read_all().decode('utf-8'))
        command = []
        command.append(b'G21\n')    # Movement units: millimeters
        command.append(b'G90\n')    # Absolute positioning
        command.append(b'G54\n')    # Use coordinate system 1
        for c in command:
            print(c)
            ser.write(c)
            time.sleep(2)
            print(ser.read_all().decode('utf-8'))
            time.sleep(4)

    def positionHome(x, y):
        print("AT HOME")

    def positionNext(new_x, new_y):
        print("New Postition")
