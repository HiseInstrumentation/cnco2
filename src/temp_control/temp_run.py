import serial
import time
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", required=True, help="Specify which port to read from. Example /dev/ttyUSB0")
    parser.add_argument("-b", "--batch", required=True, help="Specify the batch access key.")

    args = parser.parse_args()

    port = args.port

    # Use the port batch access key to get the target temp
