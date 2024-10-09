"""
Copyright 2024, Hise Scientific Instrumentation, LLC

cnco2_run.py

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

	Excution Element Structure
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

Program Logic:

	ASSUME: Gantry moves are relative, not absolute

	Create execution plan for each sample set
		Build 2 Dimensional array
		Each element has a status structure
		Initialize each element

	For each sample set
	_gantry_home_
		For each row
			For each column
				_gantry_move_x_y (should be 0,0 for first "cell")
				_sensor_sample
				Evaluate sampling response (ok, error, warn)
				record execution element
"""

