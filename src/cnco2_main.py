#!/usr/bin/python3

import cnco2
import sys
import sqlite3
import time

CNCO2Sys = cnco2.System

if __name__ == '__main__':
    cnco2.getAbout()

    # SYSTEM START
    
    # Initialize DB and environment variables (IP) 
    CNCO2Sys.initialize()
    
    # Find attached components
    CNCO2Sys.discoverComponents()
    
    while True:
        command = CNCO2Sys.getCommand()
        
        if command.type == "ADJUST_GANTRY":
            # Gantry, move x/y, record offset
            CNCO2Sys.Components.Gantry.adjust(command.parms)
            
        # RUN COMMAND
        if command.type == "EXECUTE_RUN":
            parms = command.parms
            
            batch_key = parms.batch_key
            run_count = parms.run_count
            comp_parms = parms.component.parms
            
            for current_run in run_count:            
                # For each component (object wrapper)
                CNCO2Sys.components.runParms = comp_parms
                
                while CNCO2Sys.componentsReady == FALSE:
                    Logging.write("Components Initializing")
                    time.sleep(5)

                # All cmponents are ready
                Logging.write("Components Initialized")
                
                # Start run
                    # Check exception (pause, resume, stop)
                    # Read O2
                    # Move
                    
            # end run x times
        # END RUN COMMAND
        
        time.sleep(1)
