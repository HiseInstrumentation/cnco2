'''
    Copyright 2024, Hise Scientific Instrumentation, LLC

    cnco2.py

    Purpose:
    Library for main CNCO2 components
'''
def getAbout():
    print("#############################")
    print("##   CNCO2 V0.1            ##")
    print("##   Griffin Lab, 2024     ##")
    print("#############################")

class BatchRuns:
    def createFromTemplate(template_access_key):
        return 1

class BatchRun:
    accessKey = ""
    name = ""
    description = ""
    sampleSets = []
    
    def addSampleSet(self, sample_set):
        self.sampleSets.append(sample_set)

class SampleSet:
    homeX = 0
    homeY = 0
    colCount = 0
    rowCount = 0
    rowSpacing = 0
    colSpacing = 0
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
    gantry_serial = ""
    
    def goHome():
        commands = []
        commands.append(b'G28\n')
        self.runCommands(commands)
    
    def findHome(self):
        commands = []
        commands.append(b'$H\n')
        self.runCommands(commands)
    
    def connect(self, serial_port, baud_rate):
        self.gantry_serial = serial.Serial(serial_port, baud_rate)
        time.sleep(2)
        commands = []
        commands.append(b'$5=0\n')   # Treat switches as normally open
        commands.append(b'$21=1\n')  # Enable physical limit switches
        commands.append(b'$22=1\n')  # Enable homing
        commands.append(b'G21\n')    # Metric mm
        commands.append(b'G90\n')    # Absolute mode
        
        self.runCommands(command)
        
    def runCommands(self, commands):
        for c in commands:
            print(c)
            self.gantry_serial.write(c)
            time.sleep(2)
            print(self.gantry_serial.read_all().decode('utf-8'))
            time.sleep(4)
        
    def moveTo(self, x, y):
        commands = []
        commands.append(b'G00 X'+x+' Y'+y+'\n')
        self.runCommands(commands)
        
    def initialize(self, serial_port, baud_rate):
        self.connect(serial_port, baud_rate)
        self.goHome()
        
class O2Sensor:
    
    def initialize():
        return 1
            
    def getReading():
        return 1
