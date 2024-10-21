'''
    Copyright 2024, Hise Scientific Instrumentation, LLC

    cnco2.py

    Purpose:
    Library for main CNCO2 components
'''
import sqlite3
import hashlib
import time


class BatchRuns:
    def createFromTemplate(template_access_key):
        # Needed for the new batch access key
        seed = str(round(time.time() * 1000))
        b_seed = hashlib.md5(seed.encode('utf-8'))
        
        # Connect to DB
        con = sqlite3.connect("cnco2.db")
        con.row_factory = sqlite3.Row
        
        # Get batch template for this template_id
        cur = con.cursor()
        res = cur.execute("select * from template_batch where access_key = '"+template_access_key+"'").fetchone()
        new_description = res['description']
        new_name = res['name']        
        new_access_key = b_seed.hexdigest()
        
        # Create new batch db record from template values
        cur1 = con.cursor()
        res = cur1.execute("insert into batch (created, access_key, name, description) values (datetime('now', 'localtime'), '"+new_access_key+"', '"+new_name+"', '"+new_description+"')")
        con.commit()

        # Get sample set templates
        res = cur.execute("select * from template_sample_set where t_batch_access_key = '"+template_access_key+"'").fetchall()

        # Create new sample sets based on templates
        for tss in res:
            new_name = tss['name']
            new_home_x = tss['home_x']
            new_home_y = tss['home_y']
            new_row_count = tss['row_count']
            new_col_count = tss['col_count']
            new_row_spacing = tss['row_spacing']
            new_col_spacing = tss['col_spacing']

            cur.execute("insert into sample_set (batch_access_key, name, home_x, home_y, row_count, col_count, row_spacing, col_spacing) values ('"+new_access_key+"', '"+new_name+"', "+str(new_home_x)+", "+str(new_home_y)+", "+str(new_row_count)+", "+str(new_col_count)+", "+str(new_row_spacing)+", "+str(new_col_spacing)+")")
            con.commit()

        con.close()

        # Return new batch access key
        return new_access_key		
        
    def getByAccessKey(self, access_key):
        self

class BatchRun:
    accessKey = ""
    name = ""
    description = ""
    sampleSets = []
    
    def addSampleSet(self, sample_set):
        self.sampleSets.append(sample_set)

class SampleSets:
    def getByBatchAccessKey(self, batch_access_key):
        sample_sets = []
        
        con = sqlite3.connect("cnco2.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        
        res = cur.execute("select * from sample_set where batch_access_key = '"+batch_access_key+"'").fetchall()
        
        for ss in res:
            temp_sample_set = SampleSet()
            temp_sample_set.name = res['name']
            temp_sample_set.batchAccessKey = batch_access_key
            temp_sample_set.homeX = res['home_x']
            temp_sample_set.homeY = res['home_y']
            temp_sample_set.rowCount = res['row_count']
            temp_sample_set.colCount = res['col_count']
            temp_sample_set.rowSpacing = res['row_spacing']
            temp_sample_set.colSpacing = res['col_spacing']
            
            sample_sets.append(temp_sample_set)
        
        return sampe_sets

class SampleSet:
    batchAccessKey = ""
    name = ""
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


def getAbout():
    print("#############################")
    print("##   CNCO2 V0.1            ##")
    print("##   Griffin Lab, 2024     ##")
    print("#############################")
