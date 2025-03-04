import cnco2
import sys
import time

if __name__ == '__main__':
    heater_found = False

    CNCO2Sys = cnco2.System()

    CNCO2Sys.discoverComponents()
      
    # Gantry
    gantry = CNCO2Sys.C_Gantry
    gantry.findHome()
    
    for x in range(5):
        for y in range(5):
            r_x = x * 10
            r_y = y * 10
            gantry.moveTo(r_x,r_y)
            CNCO2Sys.C_O2Sensor.getReading()
            print(CNCO2Sys.C_O2Sensor.currentO2)

    
    ''' 

    '''
        
    ''' 
    # Temp Controller
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
