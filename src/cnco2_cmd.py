import cnco2
import sys
import time

if __name__ == '__main__':
    heater_found = False

    CNCO2Sys = cnco2.System()

    command = CNCO2Sys.getNextCommand()

    CNCO2Sys.discoverComponents()

    for cont in CNCO2Sys.C_TempControllers.controllers:
        heater_found = True
        print(cont.device_id)
        cont.setTemp(30)
        time.sleep(2)
        while True:
            res = cont.getTemp()
            print(res)
            time.sleep(1)
