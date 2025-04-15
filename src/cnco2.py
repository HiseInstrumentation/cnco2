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
from urllib.request import urlopen
import re as r
from socket import timeout
from urllib.error import HTTPError, URLError
import serial.tools.list_ports
import cnco2_data

my_heater = None

class BatchRuns:

    def hasRun(self, batch_access_key):
        res = cnco2_data.CNCDataDB.getOne("select count(*) cnt from sample_store where batch_access_key = '"+batch_access_key+"'")
        cnt = res['cnt']
        
        if(cnt == 0):
            return False
        else:
            return True
        
    
    def archiveAndClear(self, batch_access_key):
        cnco2_data.CNCDataDB.execute("insert into sample_store_archive select datetime('now', 'localtime'), batch_access_key, x_pos, y_pos, o2_value, temp_value, pressure_value, status, sample_type, collected from sample_store where batch_access_key = '"+batch_access_key+"'")
        cnco2_data.CNCDataDB.execute("delete from sample_store where batch_access_key = '"+batch_access_key+"'")
        
    
    def getAll(self):
        batches = []
                
        # Get batch template for this template_id
        res = cnco2_data.CNCSystemDB.getAll("select access_key from batch order by created desc")
        
        for row in res:
            temp_b = BatchRuns().getByAccessKey(row['access_key'])
            batches.append(temp_b)
        
        return batches
    
    def createFromTemplate(template_access_key, t_new_name = ""):
        # Needed for the new batch access key
        seed = str(round(time.time() * 1000))
        b_seed = hashlib.md5(seed.encode('utf-8'))

        # Get batch template for this template_id
        res = cnco2_data.CNCSystemDB.getOne("select * from template_batch where access_key = '"+template_access_key+"'")
        new_description = res['description']
        new_name = res['name']        
        if t_new_name == "":
            new_name = res['name']
        else:
            new_name = t_new_name

        new_access_key = b_seed.hexdigest()
        
        # Create new batch db record from template values
        cnco2_data.CNCSystemDB.excute("insert into batch (created, access_key, name, description) values (datetime('now', 'localtime'), '"+new_access_key+"', '"+new_name+"', '"+new_description+"')")

        # Get sample set templates
        res = cnco2_data.CNCSystemDB.getAll("select * from template_sample_set where t_batch_access_key = '"+template_access_key+"'")

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
            new_temp_enable = tss['temp_enable']
            new_temp_target = tss['temp_target']

            cnco2_data.CNCSystemDB.execute("insert into sample_set (batch_access_key, name, home_x, home_y, row_count, col_count, row_spacing, col_spacing, ctl_x, ctl_y, blnk_x, blnk_y, temp_enable, temp_target) values ('"+new_access_key+"', '"+new_name+"', "+str(new_home_x)+", "+str(new_home_y)+", "+str(new_row_count)+", "+str(new_col_count)+", "+str(new_row_spacing)+", "+str(new_col_spacing)+", "+str(new_ctl_x)+", "+str(new_ctl_y)+", "+str(new_blnk_x)+", "+str(new_blnk_y)+","+str(new_temp_enable)+", "+str(new_temp_target)+")")

        # Return new batch access key
        return new_access_key		
        
    def getByAccessKey(self, access_key):
        res = cnco2_data.CNCSystemDB.getOne("select * from batch where access_key = '"+access_key+"'")
    
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
        templates = []
        temps = cnco2_data.CNCSystemDB.getAll("select access_key from template_batch order by name")
        
        for temp in temps:
            templates.append(BatchTemplates.getByAccessKey(temp['access_key']))
            
 
        return templates
 
    def getByAccessKey(access_key):
        res = cnco2_data.CNCSystemDB.getOne("select * from template_batch where access_key = '"+access_key+"'")
        
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
        
        res = cnco2_data.CNCSystemDB.getAll("select * from sample_set where batch_access_key = '"+batch_access_key+"'")
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

class SystemComponent:
    componentType = ""
    componentId = ""
    comPort = ""

class SystemCommand:
    created = ""
    commandText = ""
    status = ""
    executed = ""
    systemResponse = ""
    parameters = ""
    
    def setComplete(self, message):
        # sql = "update sys_command set executed = CURRENT_TIMESTAMP, system_response = '"+message+"' where created = '"+self.created+"'"
        sql = "update sys_command set executed = CURRENT_TIMESTAMP, system_response = '"+message+"' where command_text = '"+self.commandText+"' and parameters = '"+self.parameters+"' and executed = ''";
        cnco2_data.CNCSystemDB.execute(sql)

class System:
    components = []     
    ipAddress = "127.0.0.1"
    version = ""
    heater1 = None
    
    C_O2Sensor = None
    C_Gantry = None
    C_TempControllers = None
    
    def __init__(self):
        self.C_TempControllers = TempControllers()
        self.initialize()
        

    def getNextCommand(self):
        # Get the next command that has not been executed
        res = cnco2_data.CNCSystemDB.getOne("select * from sys_command where executed = '' order by created limit 1")
        cm = SystemCommand()
 
        if res != None:
            cm.created = res['created']
            cm.commandText = res['command_text']
            cm.status = res['status']
            cm.executed = res['executed']
            cm.systemResponse = res['system_response']
            cm.parameters = res['parameters']

            if cm.parameters != None:
                l_parms = {}
                if cm.parameters != "":
                    parms = cm.parameters.split('&')

                    for parm in parms:
                        parm_parts = parm.split('=')
                        p_key = parm_parts[0];
                        p_value = parm_parts[1];
                        l_parms[p_key] = p_value
                    
                cm.parms = l_parms
            
        
        return cm
    
    # Before any run can be executed, this must be called
    def initialize(self):
        ip_address = self.getIp()
        cnco2_data.CNCSystemDB.execute("delete from sys_command where executed = ''")
        cnco2_data.CNCSystemDB.execute("update cnco2_system set is_running = 0, prepared_to_run = 0, ip_address = '"+ip_address+"'")
        cnco2_data.CNCSystemDB.execute("update gantry set current_x = 0, current_y = 0, was_homed = 0, serial = ''")
        cnco2_data.CNCSystemDB.execute("update o2_sensor set serial = '', current_o2 = 0, current_temp = 0, current_pressure = 0")
        cnco2_data.CNCSystemDB.execute("delete from temp_controller")


    # This should be called during the execution of a batch so
    # that we know that we should stop executing.
    def isRunning():
        res = cnco2_data.CNCSystemDB.getOne("select is_running from cnco2_system")
        if(res['is_running'] == 0):
            return False
        else:
            return True

    def start():
        Logging.write("Starting System")
        res = cnco2_data.CNCSystemDB.getOne("select prepared_to_run from cnco2_system")
        if(res['prepared_to_run'] == 1):
            res = cnco2_data.CNCSystemDB.execute("update cnco2_system set is_running = 1")
            return True
        else:
            print("System not prepared for run")
            return False

    def stop():
        Logging.write("Stopping System")
        res = cnco2_data.CNCSystemDB.execute("update cnco2_system set is_running = 0")


    def getVersion(self):
        res = cnco2_data.CNCSystemDB.getOne("select version from cnco2_system")
        self.version = res['version']
        return res['version']

    def getIp(self):
        ip_address = '127.0.0.1'        

        try:
            url = 'http://checkip.dyndns.com/';
            d = str(urlopen(url, timeout=10).read())
            ip_address = r.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)
        except  HTTPError as error:
            Logging.write('HTTP Error: Data not retrieved: '+ error)
        except URLError as error:
            if(isinstance(error.reason, timeout)):
                Logging.write("Error timeout")
            else:
                Logging.write('URL Error')
     
        self.ipAddress = ip_address
     
        return ip_address

    def componentsReady(self):
        # Do we have all components?
        # Does each component report ready?
        return True
            

    def discoverComponents(self):

        all_port = serial.tools.list_ports.comports()
        Logging.write("Polling Serial Devices")
        
        for port in all_port:
            Logging.write(port.device)

        for port in all_port:
            connected = False
            try:
                # First connect at 115200 for temp controllers and gantry
                dev = serial.Serial(port.device, 115200, timeout=4)
                dev.reset_input_buffer()
                time.sleep(2)
                response = dev.readline().decode('utf-8').strip()
                if "CNCO2" in response:
                    connected = True
                    device_name = response[6:]
                    Logging.write("Found temp controller at " + port.device + ": " + device_name)
                    dev_exists = False
                    
                    for device in self.C_TempControllers.getAllDevices():
                        if(device.device_id == device_name):
                            device.serial = dev        # Just update the device
                            dev_exists = True
                    
                    if(dev_exists == False):
                        tc = TempController()
                        tc.device_id = device_name
                        tc.serial = dev
                        tc.connect(port.device, 115200)
                        tc.initialize()
                        self.C_TempControllers.addController(tc)
                else:
                    dev.write(b'?\n')
                    time.sleep(2)
                    response = dev.readline().decode('utf-8').strip()
                    dev.write(b'?\n')
                    time.sleep(2)
                    response = dev.readline().decode('utf-8').strip()
                    if "ok" in response:
                        connected = True
                        Logging.write("Found Gantry at " + port.device)
                        gant = Gantry()
                        gant.serial = dev
                        gant.connect(port.device, 115200)
                        self.C_Gantry = gant
                        
            except UnicodeDecodeError:
                continue
            except serial.serialutil.SerialException:
                print(".", end='')
                
            if connected == False:
                try:
                    # Second connect at 19200 for o2 sensor
                    dev = serial.Serial(port.device, 19200, timeout=4)
                    dev.reset_input_buffer()
                    time.sleep(2)
                    dev.write(b'I\n')
                    time.sleep(2)
                    response = dev.readline().decode('utf-8').strip()
                    if(response[0:9] == "ID:Oxygen"):
                        Logging.write("Found O2 at " + port.device)
                        o2sensor = O2Sensor()
                        o2sensor.connect(port.device, 19200)
                        o2sensor.serial = dev
                        self.C_O2Sensor = o2sensor

                except UnicodeDecodeError:
                    continue
                except serial.serialutil.SerialException:
                    print(".", end='')

class Storage:
    def write(self, batch_access_key, run_no, x_pos, y_pos, sample_type, o2_val, temp_val, pressure_val, status):
        o2_val = o2_val.replace(",", "")
        temp_val = temp_val.replace(",", "")
        pressure_val = pressure_val.replace(",", "")

        sql = "insert into sample_store values ('"+batch_access_key+"', "+str(run_no)+", "+str(x_pos)+", "+str(y_pos)+", "+str(o2_val)+", "+str(temp_val)+", "+str(pressure_val)+", '"+status+"', "+str(sample_type) + ",'"+strftime("%Y-%m-%d %H:%M:%S", localtime())+"')"
        cnco2_data.CNCDataDB.execute(sql)

        
    def getByAccessKey(self, batch_access_key):
        outfile = open(batch_access_key+".csv", "w")
        outfile.write("'batch_access_key','collected','x_pos','y_pos','o2_pct','temp_c','pressure_mb','status'\n")
        
        sql = "select * from sample_store where batch_access_key = '"+batch_access_key+"' order by collected"
        res = cnco2_data.CNCDataDB.getAll(sql)
        for row in res:
            outfile.write("'"+row['batch_access_key']+"', "+str(run_no)+", '"+row['collected']+"',"+str(row['x_pos'])+","+str(row['y_pos'])+","+str(row['o2_value'])+","+str(row['temp_value'])+","+str(row['pressure_value'])+",'"+row['status']+"'\n")

        outfile.close()

class Gantry:
    serial = None
    serial_name = ""
    current_x = 0
    current_y = 0
    wasHomed = False
            
    def adjustX(self, offset):
        if self.wasHomed:
            self.current_x = float(offset)
            commands = []
            commands.append(bytes('$J=G90 G21 X'+str(self.current_x)+' F2050\n', 'utf-8'))
            self.runCommands(commands)
            Logging.write("Moving to X:"+str(self.current_x))
            self.waitForReady()
            sql = "update gantry set current_x = '"+str(self.current_x)+"' where device_id = 'GANTRY'"
            res = cnco2_data.CNCSystemDB.execute(sql)

    def adjustY(self, offset):
        if self.wasHomed:
            self.current_y = float(offset)
            commands = []
            commands.append(bytes('$J=G90 G21 Y'+str(self.current_y)+' F2050\n', 'utf-8'))
            self.runCommands(commands)
            Logging.write("Moving to Y:"+str(self.current_y))
            self.waitForReady()
            sql = "update gantry set current_y = '"+str(self.current_y)+"' where device_id = 'GANTRY'"
            res = cnco2_data.CNCSystemDB.execute(sql)

    def goHome(self):
        if self.wasHomed:
            commands = []
            commands.append(b'G28\n')
            self.runCommands(commands)
            self.current_x = 0
            self.current_y = 0

    def waitForReady(self):
        command_complete = False
        while not command_complete:
            response = self.serial.readline().decode('utf-8').strip()
            if "ok" in response:
                command_complete = True
                
            time.sleep(.5)
    
    def findHome(self):
        Logging.write("Finding Home", True)
        commands = []
        commands.append(b'$H\n')
        self.runCommands(commands)
        self.waitForReady()
        sql = "update gantry set current_x = '0', current_y= '0', was_homed = 1 where device_id = 'GANTRY'"
        res = cnco2_data.CNCSystemDB.execute(sql)
        self.wasHomed = True
        self.current_x = 0
        self.current_y = 0
    
    def connect(self, serial_port, baud_rate):
        Logging.write("Connecting to gantry on "+serial_port+" Baud Rate:"+str(baud_rate), True)
        sql = "update gantry set serial = '"+serial_port+"'";
        cnco2_data.CNCSystemDB.execute(sql)
        commands = []
        commands.append(b'$0=10.0\n')
        commands.append(b'$1=255\n')
        commands.append(b'$2=0\n')
        commands.append(b'$3=3\n')   # Reverse axis
        commands.append(b'$4=0\n')
        commands.append(b'$5=7\n')   # Treat switches as normally open
        commands.append(b'$6=1\n')
        commands.append(b'$8=0\n')
        commands.append(b'$9=1\n')
        commands.append(b'$10=511\n')
        commands.append(b'$21=1\n')  # Enable physical limit switches
        commands.append(b'$22=1\n')  # Enable homing
        commands.append(b'$23=7\n')
        commands.append(b'$25=1500.0\n')
        commands.append(b'$27=5.000\n')
        commands.append(b'$28=0.100\n')
        commands.append(b'$29=0.0\n')
        commands.append(b'$30=1000.000\n')
        commands.append(b'$31=0.000\n')
        commands.append(b'$32=1\n')
        commands.append(b'$33=5000.0\n')
        commands.append(b'$34=0.0\n')
        commands.append(b'$35=0.0\n')
        commands.append(b'$36=100.0\n')
        commands.append(b'$100=57.14000\n')
        commands.append(b'$101=57.14000\n')
        commands.append(b'$102=57.14000\n')
        commands.append(b'$110=5000.000\n')
        commands.append(b'$111=5000.000\n')
        commands.append(b'$112=5000.000\n')
        commands.append(b'$120=500.000\n')
        commands.append(b'$121=500.000\n')
        commands.append(b'$122=500.000\n')
        commands.append(b'$130=300.000\n')
        commands.append(b'$131=300.000\n')
        commands.append(b'$132=70.000\n')
        commands.append(b'$320=grblHAL\n')
        commands.append(b'$341=0\n')
        commands.append(b'$342=30.0\n')
        commands.append(b'$343=25.0\n')
        commands.append(b'$344=200.0\n')
        commands.append(b'$345=200.0\n')
        commands.append(b'$346=1\n')
        commands.append(b'$384=0\n')
        commands.append(b'$394=4.0\n')
        commands.append(b'$396=30\n')
        commands.append(b'$397=0\n')
        commands.append(b'$398=100\n')
        commands.append(b'$481=0\n')
        commands.append(b'$484=1\n')
        commands.append(b'$486=0\n')
        commands.append(b'$650=0\n')
        commands.append(b'$673=1.0\n')
        
        time.sleep(3)

        self.runCommands(commands)
        
    def runCommands(self, commands):
        for c in commands:
            self.serial.write(c)
            time.sleep(.5)
        
    def reportPosition(self):
        gp = GantryPosition()
        
        res = cnco2_data.CNCSystemDB.getOne("select * from gantry limit 1")
        gp.x_pos = res['current_x']
        gp.y_pos = res['current_y']
        if self.wasHomed:
            gp.wasHomed = 1
        else:
            gp.wasHomed = 0
        
        return gp
        
    def moveTo(self, x, y):
        if self.wasHomed:
            self.current_y = y
            self.current_x = x
            commands = []
            commands.append(bytes('$J=G90 G21 X'+str(x)+' Y'+str(y)+' F2050\n', 'utf-8'))
            self.runCommands(commands)
            Logging.write("Moving to X:"+str(x)+" Y:"+str(y))
            self.waitForReady()
            sql = "update gantry set current_x = '"+str(x)+"', current_y= '"+str(y)+"' where device_id = 'GANTRY'"
            res = cnco2_data.CNCSystemDB.execute(sql)
        
    def close(self):
        self.gantry_serial.close()		
        
class GantryPosition:
    x_pos = 0
    y_pos = 0
    wasHomed = 0
        
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
    serial = None
    serial_name = ""
    currentTemp = 0
    currentO2 = 0
    currentPressure = 0
    
        
    def connect(self, serial_port, baud_rate):
        sql = "update o2_sensor set serial = '"+serial_port+"'";
        cnco2_data.CNCSystemDB.execute(sql)
        Logging.write("Connecting to O2 Sensor on "+serial_port+" Baud Rate:"+str(baud_rate), True)
    
    def reportReading(self):
        return_value = O2SensorReading()

        res = cnco2_data.CNCSystemDB.getOne("select * from o2_sensor limit 1")
        return_value.ot_pct = res['current_o2']
        return_value.temp = res['current_temp']
        return_value.pressure = res['current_pressure']
        
        return return_value
            
    def getReading(self):
        return_value = O2SensorReading()
        value_rec = False
        
        while(value_rec == False):
            self.serial.write(b'M\n')
            time.sleep(1)
            return_str = self.serial.read_all().decode('utf-8').strip()
            Logging.write(return_str)
            
            if(return_str[:10] == "Low signal"):
                return_value.status = "Low Signal"
                Logging.write("Received Low Signal, waiting 4 seconds", True)
                time.sleep(5)
            elif(return_str.strip() == ""):
                Logging.write("Received no value, waiting 3 seconds", True)
                time.sleep(3)
            else:
                regex_o2 = "^[0-9]*.[0-9]*"
                regex_te = ",[0-9]*.[0-9]*"
                regex_pr = "[0-9]{4}|[0-9]{3}"
            
                return_value.o2_pct = self.currentO2 = re.search(regex_o2, return_str).group()
                return_value.temp = self.currentTemp = re.search(regex_te, return_str).group().replace(',', '')
                return_value.pressure = self.currentPressure = re.search(regex_pr, return_str).group()
                return_value.status = "O2 Read Successful"
                value_rec = True
                
                sql = "update o2_sensor set current_temp = '"+self.currentTemp+"', current_o2 = '"+self.currentO2+"', current_pressure = '"+self.currentPressure+"' where device_id = 'O2 Sensor'"
                res = cnco2_data.CNCSystemDB.execute(sql)

        return return_value

class TempControllers:
    controllers = []
    
    def addController(self, controller):
        self.controllers.append(controller)
    
    def getDeviceById(self, device_id):
        for cont in self.controllers:
            if cont.device_id == device_id:
                return cont
                
        Logging.write("Could not find device: " + device_id)
    
    def getAllDevices(self):
        return self.controllers
    
    def setTemp(self, device_id, target_temp):
        cont = self.getDeviceById(device_id)
        if(cont != None):
            cont.setTemp(target_temp)
        
    def tempStat(self, device_id):
        cont = self.getDeviceById(device_id)
        if(cont != None):
            cont.getStat()
        
    def stopDevice(self, device_id):
        cont = self.getDeviceById(device_id)
        cont.stop()

class SamplePosition:
    tray_id = ""
    x = 0
    y = 0
    label = ""

labels_x = ['1','2','3','4','5','6','7','8']
labels_y = ['A','B','C','D','E','F']


class TempController:
    serial = None
    currentTemp = 0
    targetTemp = 0
    peltierPowerLevel = 0
    currentStatus = "O"
    isReady = False
    serial_name = ""
    samplePositions = []
    device_id = ""
    
    def initialize(self):
        # Get tray
        sql = "select * from tray where device_id = '"+self.device_id+"'"
        res = cnco2_data.CNCSystemDB.getOne(sql)
        home_x = res['home_x']
        home_y = res['home_y']
        
        # Calculate the positions and labels
        for x in range(8):
            for y in range(6):
                sp = SamplePosition()
                sp.x = x*10
                sp.y = y*10
                sp.label = labels_x[x] + labels_y[y]
            
        
        return self
    
    def setTemp(self, target_temp):
        self.serial.write(bytes('target ' + str(target_temp), 'utf-8'))
        self.waitForReady()

        self.serial.write(bytes('start', 'utf-8'))
        self.waitForReady()
        
        Logging.write(self.device_id + ": Setting target temp to " + str(target_temp))
        
    def stop(self):
        self.serial.write(bytes("stop", 'utf-8'))
        self.waitForReady()
        
    def waitForReady(self):
        response = False
        
        while not response:
            try:
                return_str = self.serial.readline().decode('utf-8').strip()
                if "ready" in return_str:
                    response = True
            except:
                continue
                
            time.sleep(1)
        
        return return_str
        
    def getStat(self):
        self.serial.write(b'stat')
        try:
            t_stat = self.serial.readline().decode('utf-8').strip()
            t_parts = t_stat.split("\t")
            if(len(t_parts) == 4):
                self.targetTemp = t_parts[0]
                self.currentTemp = t_parts[1]
                self.peltierPowerLevel = t_parts[2]
                self.currentStatus = t_parts[3]
                '''
                if (abs(float(self.currentTemp) - float(self.targetTemp)) < 1):
                    self.isReady = True
                '''

                sql = "insert into temp_controller (device_id, target_temp, current_temp, peltier_power_level, current_status) values ('"+self.device_id+"', '"+self.targetTemp+"', '"+self.currentTemp+"', '"+self.peltierPowerLevel+"', '"+self.currentStatus+"') on CONFLICT (device_id) do update set current_temp = '"+self.currentTemp+"', target_temp = '"+self.targetTemp+"', peltier_power_level = '"+self.peltierPowerLevel+"', current_status = '"+self.currentStatus+"'"
                res = cnco2_data.CNCSystemDB.execute(sql)

                return t_stat
            else:
                return None
        except:
            return None

    def reportStatus(self, device_id):
        ts = TempStatus()
        res = cnco2_data.CNCSystemDB.getOne("select * from temp_controller where device_id = '"+device_id+"'")
        ts.deviceId = device_id
        ts.targetTemp = res['target_temp']
        ts.currentTemp = res['current_temp']
        ts.peltierPowerLevel = res['peltier_power_level']
        ts.current_status = res['current_status']
        
        return ts
        
    def connect(self, serial_port, baud_rate):
        Logging.write("Connecting to Temp Controller on "+serial_port+" Baud Rate:"+str(baud_rate), True)
        sql = "insert into temp_controller values ('"+self.device_id+"', '0', '0', '0', '0', '"+serial_port+"') on CONFLICT (device_id) do update set current_temp = '0'"
        res = cnco2_data.CNCSystemDB.execute(sql)
           
class TempStatus:
    deviceId = ""
    targetTemp = 0
    currentTemp = 0
    peltierPowerLevel = 0
    current_status = ""


class Logging:    
    def write(message, echo = False ):
        pre_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
        log_file = open('/home/jhise/cnco2/src/cnco2_log.txt', 'a')
        log_file.write(pre_time+": " + str(message) + "\n")
        if(echo == True):
            print(message)
        log_file.close()
        
    def read():
        log_file = open('cnco2_log.txt', 'r')
        print(log_file.read())
        log_file.close()
    

def getAbout():
    sys = System()
    version = sys.getVersion()
    print("#######################################################")
    print("     CNCO2 V "+version)
    print("     Griffin Lab, 2024")
    print("#######################################################")
