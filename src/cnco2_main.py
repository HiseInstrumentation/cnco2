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

        if command.commandText == "SYS_INIT":
            CNCO2Sys.initialize()
        
        if command.commandText == "COMP_DISCOVERY":
            CNCO2Sys.discoverComponents()
            command.setComplete('Finished Component Discovery')
                
        if command.commandText == "COMP_COMMAND":
            if command.parms['command_type'] == 'GANTRY_HOME':
                CNCO2Sys.C_Gantry.findHome()
                command.setComplete('Gantry Homed')
                
            if command.parms['command_type'] == 'ADJUST_GANTRY':
                move_x = command.parms.get('x')
                move_y = command.parms.get('y')
                
                if move_x:
                    print("Moving X" + str(move_x))
                    CNCO2Sys.C_Gantry.adjustX(move_x) 
                
                if move_y:
                    print("Moving Y" + str(move_y))                
                    CNCO2Sys.C_Gantry.adjustY(move_y) 
                    
                command.setComplete('Finished Moving')

            
            if command.parms['command_type'] == 'TEMP_SET':
                CNCO2Sys.C_TempControllers.setTemp(command.parms['controller_id'], command.parms['target_temp'])
                command.setComplete('Finished Setting Temp')

            if command.parms['command_type'] == 'TEMP_STAT':
                CNCO2Sys.C_TempControllers.tempStat(command.parms['controller_id'])
                command.setComplete('Finished Temp Controller Stat')

            if command.parms['command_type'] == 'TEMP_STOP':
                CNCO2Sys.C_TempControllers.stopDevice(command.parms['controller_id'])
                command.setComplete('Finished Stopping Temp Controller')

 
            if command.parms['command_type'] == 'O2_READ':
                o2_reading = CNCO2Sys.C_O2Sensor.getReading()
                command.setComplete('Finished O2 Read')


        if command.commandText == "SYS_HALT":
            sys.exit(0)

        # RUN COMMAND
        if command.commandText == "EXECUTE_RUN":
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
                
                for tcont in CNCO2Sys.C_TempControllers:     # This will only returned what is discovered
                    for sample_pos in tcont.samplePositions: # Need to generate these during device discovery as well as the labels
                        if cnco2.System.isRunning():
                            cnco2.Logging.write("\tSampling: " + sample_pos.label + " at " + str(sample_pos.x) + "," + str(sample_pos.y))
                            gantry.moveTo(sample_pos.x, sample_pos.y)
                            tcont.getStat()
                            current_temp = tcont.currentTemp
                            reading = o2.getReading()
                            cnco2.Logging.write("\t"+reading.status)
                            cnco2.Storage().write(batch_access_key, su.x, su.y, su.sampleStatus, reading.o2, current_temp, reading.pressure, reading.status)

                '''
                for ss in batch.sampleSets:
                    for su in ss.execPlan:
                        if cnco2.System.isRunning():
                            cnco2.Logging.write("\tSampling: " + str(su.x) + "," + str(su.y))
                            gantry.moveTo(su.x, su.y)
                            reading = o2.getReading()
                            cnco2.Logging.write("\t"+reading.status)
                            cnco2.Storage().write(batch_access_key, su.x, su.y, su.sampleStatus, reading.o2, reading.temp, reading.pressure, reading.status)
                '''


            gantry.findHome()
            cnco2.Logging.write("Job Complete", True)
        cnco2.Logging.write("Waiting for commands")
        time.sleep(1)
