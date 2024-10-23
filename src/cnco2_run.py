"""
Copyright 2024, Hise Scientific Instrumentation, LLC

cnco2_run.py

Purpose:
Execute a batch

Command line parameters:
batch_id

Program Structures
	Batch stored parameters
	. Name
	. Description
	. Enable
	. action on failure
	. included_sample_sets ([1,2,3,4])

	Sample Set structure
	. home_x
	. home_y
	. col_count
	. row_count
	. name

	Element Structure
	. x offset			int
	. y offset			int
	. sample_time		datetime
	. sample_value		decimal
	. sample_status		int
	
	Sample Status
		0 Success
		1 Value out of bounds
		2 Other Warning
		10 Could not read
		11 Other Fatal
"""
import cnco2
import sys

if __name__ == '__main__':
	cnco2.getAbout()
	
	try:
		batch_access_key = sys.argv[1]
	except IndexError:
		batch_access_key = print("No Batch Access Key Specificed")
		sys.exit()
	
	batch_access_key = sys.argv[1]
	
	batch = cnco2.BatchRuns().getByAccessKey(batch_access_key)

	for sample_set in batch.sampleSets:
		sample_set.initializePlan()

	gantry = cnco2.Gantry()
	gantry.initialize('/dev/ttyUSB0', 115200)
		
	#	Connect to COM for sensor
	o2 = cnco2.O2Sensor()
	o2.initialize('/dev/ttyUSB1', 19200)

	# For each sample set
	for ss in batch.sampleSets:
		for su in ss.execPlan:
			print("Sampling: " + str(su.x) + "," + str(su.y))
			if cnco2.System.isRunning():
				gantry.moveTo(su.x, su.y)
				reading = o2.getReading()
				print("\t"+reading.status)
				cnco2.Storage().write(batch_access_key, su.x, su.y, reading.o2, reading.temp, reading.pressure, reading.status)
				

