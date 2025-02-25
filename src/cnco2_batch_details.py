import cnco2
import sys
import sqlite3

if __name__ == '__main__':
	cnco2.getAbout()

	try:
		batch_access_key = sys.argv[1]
	except IndexError:
		batch_access_key = "NA"
		
	if(batch_access_key != "NA"):
		batch = cnco2.BatchRuns().getByAccessKey(batch_access_key)

		print("Batch: ")
		print(batch.name)
		print(batch.description)
		print(batch.created)
		print("")
		print("Sample Sets")
		print(f"{'Name' : <20}{'Home X' : ^10}{'Home Y' : ^10}{'Control X' : ^10}{'Control Y' : ^10}{'Blank X':^10}{'Blank Y':^10}{'Rows':^5}{'Cols':^5}{'Row Spc(mm)':^12}{'Col Spc(mm)': ^12}")
		print("----------------------------------------------------------------------------------------------------------------------")
		for ss in batch.sampleSets:
			print(f"{ss.name : <20}{ss.homeX : ^10}{ss.homeY : ^10}{ss.controlX : ^10}{ss.controlY : ^10}{ss.blankX : ^10}{ss.blankY : ^10}{ss.rowCount:^5}{ss.colCount:^5}{ss.rowSpacing:^12}{ss.colSpacing: ^12}")
			
			ss.initializePlan()
			for ssu in ss.execPlan:
				print("\t\tPOS: " + str(ssu.x) + "," + str(ssu.y) + " Type: " + str(ssu.sampleStatus) )
			
	else:
		print("All Batches")
		batch_list = cnco2.BatchRuns().getAll()
		print(f"{'Name' : <20}{'Access Key' : ^34}{'Description' : ^40}")
		print("----------------------------------------------------------------------------------------------------------------------")
		for batch in batch_list:
		    print(f"{batch.created : <20}{batch.accessKey : ^34}{batch.name : ^40}")
