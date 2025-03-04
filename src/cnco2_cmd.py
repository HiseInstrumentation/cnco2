import cnco2
import sys
import time

if __name__ == '__main__':
    heater_found = False

    CNCO2Sys = cnco2.System()

    command = CNCO2Sys.getNextCommand()

    CNCO2Sys.discoverComponents()
    
    o2_sensor = CNCO2Sys.C_O2Sensor.getReading()
    
    '''
    cont = CNCO2Sys.C_TempControllers.getDeviceById("HEATER 1")
    
    print("Found Heater 1")
    cont.getStat()

    print("Target Temp: ", end = "")
    print(cont.targetTemp)
    print("Current Temp: ", end = "")
    print(cont.currentTemp)
    print("Peltier Power Level: ", end = "")
    print(cont.peltierPowerLevel)
    print("Status: ", end = "")
    print(cont.currentStatus)

    '''
