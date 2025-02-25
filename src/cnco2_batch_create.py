import cnco2
import sys
import sqlite3

if __name__ == '__main__':
	cnco2.getAbout()
	
	try:
		batch_template_id = sys.argv[1]
	except IndexError:
		batch_access_key = print("\nNo Batch Template Specified\n")
		sys.exit()

	t_new_name = ""
    
	if len(sys.argv) == 3:
		t_new_name = sys.argv[2]

	cnco2.Logging.write("\nCreating new batch from template "+batch_template_id+".\n", True)		
	new_batch_key = cnco2.BatchRuns.createFromTemplate(batch_template_id, t_new_name)
	cnco2.Logging.write("\nNew Batch Key: " + new_batch_key + "\n", True)
