"""
Copyright 2024, Hise Scientific Instrumentation, LLC

cnco2_run.py

Purpose:
Export Data

Command line parameters:
batch_key
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

	print("\nExporting to file: "+batch_access_key+".csv\n")
	
	cnco2.Storage().getByAccessKey(batch_access_key)

