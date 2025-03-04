import cnco2
import sys
import time

if __name__ == '__main__':
    temp_ready = False

    CNCO2Sys = cnco2.System()
    CNCO2Sys.discoverComponents()
    
    cont = CNCO2Sys.C_TempControllers.getDeviceById("HEATER 4")
    cont.setTemp(33)
    cont.getStat()
    
    while not temp_ready:
        cont.getStat()
        
        uf = "Target: %s\tCurrent: %s\tPower: %s\tStatus: %s" % (cont.targetTemp, cont.currentTemp, cont.peltierPowerLevel, cont.currentStatus)
        print(uf)
        
        if(float(cont.currentTemp) > (float(cont.targetTemp) - 1)):
            temp_ready = True
            print("TEMP IS READY!")

        
        time.sleep(1)
        
 
    # Gantry
    gantry = CNCO2Sys.C_Gantry
    gantry.findHome()
    
    for x in range(3):
        for y in range(3):
            r_x = x * 10
            r_y = y * 10
            gantry.moveTo(r_x,r_y)
            CNCO2Sys.C_O2Sensor.getReading()
            print(CNCO2Sys.C_O2Sensor.currentO2)
