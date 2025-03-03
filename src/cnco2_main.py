#!/usr/bin/python3

import cnco2
import sys
import sqlite3
import time

if __name__ == '__main__':
    CNCO2Sys = cnco2.System()
    
    cnco2.getAbout()
    
    # Initialize DB and environment variables (IP) 
    CNCO2Sys.initialize()

    while True:
        command = CNCO2Sys.getNextCommand()
        
        if command.commandText == "COMP_DISCOVERY:
            # Find attached components (Must give a green light for 
            # running and adjusting gantry
            CNCO2Sys.discoverComponents()        
        
        if command.commandText == "COMP_COMMAND":
            if command.parms['command_type'] == 'ADJUST_GANTRY':
                
                # Gantry, move x/y, record offset
                CNCO2Sys.Gantry.adjust(command.parms['jog_dir'])
            
            if command.parms.commandType == 'TEMP_SET':
                # Set the temperature of the temp controllers
                CNCO2Sys.TempControllers.setTemp(command.parms['controller_id'], command.parms['target_temp'])
                
            if comand.parms.commandType == 'O2_RESET':
                # Reset the O2 sensor
                CNCO2Sys.O2Sensor.reset()
            
        # RUN COMMAND
        if command.type == "EXECUTE_RUN":
            parms = command.parms
            
            batch_key = parms.batch_key
            run_count = parms.run_count
            comp_parms = parms.component.parms
            
            batch = cnco2.BatchRuns().getByAccessKey(batch_key)
            for sample_set in batch.sampleSets:
                sample_set.initializePlan()
            
            for current_run in run_count:            
                
                # We are waiting for the temp controllers to give the OK on reaching target temperatures
                while CNCO2Sys.componentsReady() == FALSE:
                    Logging.write("Components Initializing")
                    time.sleep(5)

                # All cmponents are ready
                cnco2.Logging.write("Components Initialized")
                
                for ss in batch.sampleSets:
                    for su in ss.execPlan:
                        if cnco2.System.isRunning():
                            cnco2.Logging.write("\tSampling: " + str(su.x) + "," + str(su.y))
                            gantry.moveTo(su.x, su.y)
                            reading = o2.getReading()
                            cnco2.Logging.write("\t"+reading.status)
                            cnco2.Storage().write(batch_access_key, su.x, su.y, su.sampleStatus, reading.o2, reading.temp, reading.pressure, reading.status)

            gantry.findHome()
            cnco2.Logging.write("Job Complete", True)

        time.sleep(1)
