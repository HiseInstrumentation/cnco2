# Libraries

# Load configuration
#	x spacing
#	y spacing
#	batch parameters

# Create execution plans for each batch
#	Build 2 Dimensional array
# 	Each element has a status structure
#	Initialize each element

# For each Execution Plan
#	Get Max cols of plan
#	Get Max rows of plan











"""
Excution Element Structure
. x offset			int
. y offset			int
. sample_time		datetime
. sample_value		decimal
. sample_status		int
"""

""" 
Sample Status
0 Success
1 Value out of bounds
2 Other Warning
10 Could not read
11 Other Fatal
"""

"""
Batch Parameters
. Name
. Description
. Enable
. action on failure
"""

""" Batch Log
. event_ts		datetime
. event			created/started/finished
"""
