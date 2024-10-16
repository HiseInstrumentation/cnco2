'''
    Copyright 2024, Hise Scientific Instrumentation, LLC

    cnco2.py

    Purpose:
    Library for main CNCO2 components
'''
def getAbout():
    print("CNCO2 V0.1")
    print("Griffin Lab")


class SampleSet:
    homeX = 0
    homeY = 0
    colCount = 0
    rowCount = 0
    execPlan = []

    def __init__(self, home_x, home_y, col_count, row_count):
        self.homeX = home_x
        self.homeY = home_y
        self.colCount = col_count
        self.rowCount = row_count

    def initializePlan(self):
        self    
        # Loop through all rows
        #   Loop through all cols
        #       Create new SampleUnit
        #       Calculate absolute x,y based on gantry dimensions
        #       Add to execPlan list

class SampleUnit:
    x = 0
    y = 0
    sampleTime = ""
    sampleValue = ""
    sampleStatus = 0

class System:

    # This should be called during the execution of a batch so
    # that we know that we should stop executing.
    def isRunning():
        print("System is running")

class Gantry:
    def goHome():
        x=1
    
    def connect():
        x=1
        
    def initialize(self)
        self.connect()
        self.goHome()
        
    
