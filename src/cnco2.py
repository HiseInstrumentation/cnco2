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
import re




class BatchRuns:
    
    def hasRun(self, batch_access_key):
        con = sqlite3.connect("cnco2_data.db")
        con.row_factory = sqlite3.Row
        
        cur = con.cursor()
        res = cur.execute("select count(*) cnt from sample_store where batch_access_key = '"+batch_access_key+"'").fetchone()
        cnt = res['cnt']
        
        if(cnt == 0):
            return False
        else:
            return True
        
    
    def archiveAndClear(self, batch_access_key):
        con = sqlite3.connect("cnco2_data.db")
        con.row_factory = sqlite3.Row
        
        cur = con.cursor()
        cur.execute("insert into sample_store_archive select datetime('now', 'localtime'), batch_access_key, x_pos, y_pos, o2_value, temp_value, pressure_value, status, sample_type, collected from sample_store where batch_access_key = '"+batch_access_key+"'")
        con.commit()
        
        cur.execute("delete from sample_store where batch_access_key = '"+batch_access_key+"'")
        con.commit()
        
    
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
    
    def createFromTemplate(template_access_key, t_new_name = ""):
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
        if t_new_name == "":
            new_name = res['name']
        else:
            new_name = t_new_name

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
            new_ctl_x = tss['ctl_x']
            new_ctl_y = tss['ctl_y']
            new_blnk_x = tss['blnk_x']
            new_blnk_y = tss['blnk_y']

            cur.execute("insert into sample_set (batch_access_key, name, home_x, home_y, row_count, col_count, row_spacing, col_spacing, ctl_x, ctl_y, blnk_x, blnk_y) values ('"+new_access_key+"', '"+new_name+"', "+str(new_home_x)+", "+str(new_home_y)+", "+str(new_row_count)+", "+str(new_col_count)+", "+str(new_row_spacing)+", "+str(new_col_spacing)+", "+str(new_ctl_x)+", "+str(new_ctl_y)+", "+str(new_blnk_x)+", "+str(new_blnk_y)+")")
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

class BatchTemplate:
    accessKey = ""
    name = ""
    description = ""
    
class BatchTemplates:
    
    def getAll():
        con = sqlite3.connect("cnco2.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        templates = []
        
        temps = cur.execute("select access_key from template_batch order by name").fetchall()
        
        for temp in temps:
            templates.append(BatchTemplates.getByAccessKey(temp['access_key']))
            
 
        return templates
 
    def getByAccessKey(access_key):
        con = sqlite3.connect("cnco2.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        res = cur.execute("select * from template_batch where access_key = '"+access_key+"'").fetchone()
    
        if(res == None):
            return(BatchTemplate())
        else:
            # Create BatchRun object
            batch = BatchTemplate()
            batch.accessKey = access_key
            batch.name = res['name']
            batch.description = res['description']
            
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
            temp_sample_set.controlX = ss['ctl_x']
            temp_sample_set.controlY = ss['ctl_y']
            temp_sample_set.blankX = ss['blnk_x']
            temp_sample_set.blankY = ss['blnk_y']
            
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
    controlX = 0
    controlY = 0
    blankX = 0
    blankY = 0
    execPlan = []

    def initializePlan(self):
        self.execPlan = []

        if(self.controlX > 0):
            ctl_su = SampleUnit()
            ctl_su.x = self.controlX
            ctl_su.y = self.controlY
            ctl_su.sampleStatus = 1
            self.execPlan.append(ctl_su)

        if(self.blankX > 0):
            blnk_su = SampleUnit()
            blnk_su.x = self.blankX
            blnk_su.y = self.blankY
            blnk_su.sampleStatus = 2
            self.execPlan.append(blnk_su)

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
    SAMPLE_TYPE_REG = 0
    SAMPLE_TYPE_CTL = 1
    SAMPLE_TYPE_BLNK = 2

class System:

    # This should be called during the execution of a batch so
    # that we know that we should stop executing.
    def isRunning():
        con = sqlite3.connect("cnco2.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        
        res = cur.execute("select is_running from cnco2_system").fetchone()
        if(res['is_running'] == 0):
            return False
        else:
            return True

    def start():
        Logging.write("Starting System")
        con = sqlite3.connect("cnco2.db")
        cur = con.cursor()
        
        res = cur.execute("update cnco2_system set is_running = 1")
        con.commit()
        
    def stop():
        Logging.write("Stopping System")
        con = sqlite3.connect("cnco2.db")
        cur = con.cursor()
        
        res = cur.execute("update cnco2_system set is_running = 0")
        con.commit()

class Storage:
    def write(self, batch_access_key, x_pos, y_pos, sample_type, o2_val, temp_val, pressure_val, status):
        con = sqlite3.connect("cnco2_data.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        sql = "insert into sample_store values ('"+batch_access_key+"', "+str(x_pos)+", "+str(y_pos)+", "+str(o2_val)+", "+str(temp_val)+", "+str(pressure_val)+", '"+status+"', "+str(sample_type) + ",'"+strftime("%Y-%m-%d %H:%M:%S", localtime())+"')"
        cur.execute(sql)
        con.commit()
        
    def getByAccessKey(self, batch_access_key):
        con = sqlite3.connect("cnco2_data.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        outfile = open(batch_access_key+".csv", "w")
        outfile.write("'batch_access_key','collected','x_pos','y_pos','o2_pct','temp_c','pressure_mb','status'\n")
        
        sql = "select * from sample_store where batch_access_key = '"+batch_access_key+"' order by collected"
        res = cur.execute(sql)
        for row in res:
            outfile.write("'"+row['batch_access_key']+"','"+row['collected']+"',"+str(row['x_pos'])+","+str(row['y_pos'])+","+str(row['o2_value'])+","+str(row['temp_value'])+","+str(row['pressure_value'])+",'"+row['status']+"'\n")

        outfile.close()

class Gantry:
    gantry_serial = ""
    
    def goHome(self):
        commands = []
        commands.append(b'G28\n')
        self.runCommands(commands)
    
    def findHome(self):
        Logging.write("Finding Home", True)
        commands = []
        commands.append(b'$H X\n')
        commands.append(b'$H Y\n')        
        self.runCommands(commands)
        time.sleep(10)

    
    def connect(self, serial_port, baud_rate):
        self.gantry_serial = serial.Serial(serial_port, baud_rate)
        Logging.write("Connecting to gantry on "+serial_port+" Baud Rate:"+str(baud_rate), True)
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
            self.gantry_serial.write(c)
            Logging.write(c.decode('utf-8'))
            time.sleep(1)
            Logging.write(self.gantry_serial.read_all().decode('utf-8'))
        
    def moveTo(self, x, y):
        commands = []
        commands.append(bytes('G00 X'+str(x)+' Y'+str(y)+'\n', 'utf-8'))
        self.runCommands(commands)
        
    def initialize(self, serial_port, baud_rate):
        self.connect(serial_port, baud_rate)
        self.findHome()
        
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
        Logging.write("Connecting to O2 Sensor on "+serial_port+" Baud Rate:"+str(baud_rate), True)
        try:
            self.sensor_serial = serial.Serial(serial_port, baud_rate)
            return True
        except serial.serialutil.SerialException:
            Logging.write("Could not connect to sensor")
            System.stop()
            return False
            
    def getReading(self):
        return_value = O2SensorReading()
        value_rec = False
        
        while(value_rec == False):
            self.sensor_serial.write(b'M\n')
            time.sleep(1.5)
            return_str = self.sensor_serial.read_all().decode('utf-8')
            Logging.write(return_str)
            
            if(return_str[:10] == "Low signal"):
                return_value.status = "Low Signal"
                Logging.write("Received Low Signal, waiting 30 seconds", True)
                time.sleep(30)
            elif(return_str.strip() == ""):
                Logging.write("Received no value, waiting 3 seconds", True)
                time.sleep(3)
            else:
                regex_o2 = "^[0-9]*\.[0-9]*"
                regex_te = "[0-9]*\.[0-9]*\B"
                regex_pr = "[0-9]{4}|[0-9]{3}"
            
                return_value.o2 = re.search(regex_o2, return_str).group()
                return_value.temp = re.search(regex_te, return_str).group()
                return_value.pressure = re.search(regex_pr, return_str).group()
                return_value.status = "O2 Read Successful"
                value_rec = True

        return return_value

class Logging:
    
    def write(message, echo = False ):
        pre_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
        log_file = open('cnco2_log.txt', 'a')
        log_file.write(pre_time+": " + message + "\n")
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
