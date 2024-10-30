"""
Copyright 2024, Hise Scientific Instrumentation, LLC

cnco2_run.py

Purpose:
Execute a batch

Command line parameters:
batch_id

"""
import cnco2
import sys
import time

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

	# Connect to COM for sensor
	o2 = cnco2.O2Sensor()
	o2.initialize('/dev/ttyUSB1', 19200)

	# Connect to gantry controller
	gantry = cnco2.Gantry()
	gantry.initialize('/dev/ttyUSB0', 115200)

	# For each sample set
	for ss in batch.sampleSets:
		for su in ss.execPlan:
			if cnco2.System.isRunning():
				print("\tSampling: " + str(su.x) + "," + str(su.y))
				gantry.moveTo(su.x, su.y)
				reading = o2.getReading()
				print("\t"+reading.status)
				cnco2.Storage().write(batch_access_key, su.x, su.y, su.sampleStatus, reading.o2, reading.temp, reading.pressure, reading.status)

	gantry.goHome()
	cnco2.Logging.write("Job Complete", True)
