'''
    Copyright 2024, Hise Scientific Instrumentation, LLC

    cnco2.py

    Purpose:
    Library for main CNCO2 components
'''
import sqlite3
import hashlib
import time
from time import localtime, strftime
import serial




class BatchRuns:
    
    def getAll(self):
        batches = []
        
        con = sqlite3.connect("cnco2.db")
        con.row_factory = sqlite3.Row
        
        # Get batch template for this template_id
        cur = con.cursor()
        res = cur.execute("select access_key from batch order by created desc").fetchall()
        for row in res:
            temp_b = BatchRuns().getByAccessKey(row['access_key'])
            batches.append(temp_b)
        
        return batches
    
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
        con = sqlite3.connect("cnco2.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        res = cur.execute("select * from batch where access_key = '"+access_key+"'").fetchone()
    
        if(res == None):
            return(BatchRun())
        else:
            # Create BatchRun object
            batch = BatchRun()
            batch.accessKey = access_key
            batch.name = res['name']
            batch.description = res['description']
            batch.created = res['created']
            
            # Get all associated sample sets and add to batch run
            batch.sampleSets = SampleSets().getByBatchAccessKey(access_key)
        
            # Return batch run
            return batch

class BatchRun:
    accessKey = ""
    name = ""
    description = ""
    created = ""
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
            temp_sample_set.name = ss['name']
            temp_sample_set.batchAccessKey = batch_access_key
            temp_sample_set.homeX = ss['home_x']
            temp_sample_set.homeY = ss['home_y']
            temp_sample_set.rowCount = ss['row_count']
            temp_sample_set.colCount = ss['col_count']
            temp_sample_set.rowSpacing = ss['row_spacing']
            temp_sample_set.colSpacing = ss['col_spacing']
            
            sample_sets.append(temp_sample_set)
        
        return sample_sets

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

    def initializePlan(self):
        self.execPlan = []
        for row in range(self.rowCount):
            for col in range(self.colCount):
                t_ss = SampleUnit()
                t_ss.x = (col * self.colSpacing) + self.homeX
                t_ss.y = (row * self.rowSpacing) + self.homeY
                self.execPlan.append(t_ss)
 
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
        return True

    def start(self):
        self
        
    def stop(self):
        self

class Storage:
    def write(self, batch_access_key, x_pos, y_pos, o2_val, temp_val, pressure_val, status):
        con = sqlite3.connect("cnco2.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        sql = "insert into sample_store values ('"+batch_access_key+"', "+str(x_pos)+", "+str(y_pos)+", "+str(o2_val)+", "+str(temp_val)+", "+str(pressure_val)+", '"+status+"', '"+strftime("%Y-%m-%d %H:%M:%S", localtime())+"')"
        cur.execute(sql)
        con.commit()
        

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
        time.sleep(3)
        commands = []
        commands.append(b'$5=0\n')   # Treat switches as normally open
        commands.append(b'$21=1\n')  # Enable physical limit switches
        commands.append(b'$22=1\n')  # Enable homing
        commands.append(b'G21\n')    # Metric mm
        commands.append(b'G90\n')    # Absolute mode
        
        self.runCommands(commands)
        
    def runCommands(self, commands):
        for c in commands:
            print(c)
            self.gantry_serial.write(c)
            time.sleep(1)
            print(self.gantry_serial.read_all().decode('utf-8'))
            time.sleep(1)
        
    def moveTo(self, x, y):
        commands = []
        commands.append(bytes('G00 X'+str(x)+' Y'+str(y)+'\n', 'utf-8'))
        self.runCommands(commands)
        
    def initialize(self, serial_port, baud_rate):
        self.connect(serial_port, baud_rate)
        #self.goHome() #REMOVE
        
class O2SensorReading:
    o2_pct = ""
    temp = ""
    pressure = ""
    status = "Initialized"
    
    def __init__(self):
        self.o2 = 0.0
        self.temp = 0.0
        self.pressure = 0.0
        self.status = "Initialized"
        
        
class O2Sensor:
    sensor_serial = ""
    
    def initialize(self, serial_port, baud_rate):
        self.connect(serial_port, baud_rate)
        
    def connect(self, serial_port, baud_rate):
        self.sensor_serial = serial.Serial(serial_port, baud_rate)

    def getReading(self):
        return_value = O2SensorReading()
        
        self.sensor_serial.write(b'M\n')
        time.sleep(2)
        return_str = self.sensor_serial.read_all().decode('utf-8')
        print("RETURN: ")
        print(return_str)
        if(return_str[0][:10] == "Low signal"):
            return_value.status = "Low Signal"
        else:
            vals = return_str.split(",")
            return_value.o2 = vals[0][:4]
            return_value.temp = vals[1][:4]
            return_value.pressure = vals[2][:4]
            return_value.status = "O2 Read Successful"

        return return_value
        
    def runCommands(self, commands):
        return_values = []
        for c in commands:
            self.sensor_serial.write(c)
            time.sleep(2)
            return_values.append(self.sensor_serial.read_all().decode('utf-8'))
            time.sleep(2)

    
        return return_values

class Logging:
    
    def write(message, echo = False ):
        pre_time = strftime("%a, %d %b %Y %H:%M:%S +0000", localtime())
        log_file = open('cnco2_log.txt', 'a')
        log_file.write(pre_time+": " + message+"\n")
        if(echo == True):
            print(message)
        log_file.close()
        
    def read():
        log_file = open('cnco2_log.txt', 'r')
        print(log_file.read())
        log_file.close()
    

def getAbout():
    print("#######################################################")
    print("##   CNCO2 V0.1                                      ##")
    print("##   Griffin Lab, 2024                               ##")
    print("#######################################################")
