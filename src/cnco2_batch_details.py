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
		for ss in batch.sampleSets:
			print("-------------------------------------")
			print("\t"+ss.name)
			print("\tHome X: "+str(ss.homeX))
			print("\tHome Y: "+str(ss.homeY))
			print("\tRows: " + str(ss.rowCount))
			print("\tCols: " + str(ss.colCount))
			print("\tRow Spacing: " + str(ss.rowSpacing))
			print("\tCol Spacing: " + str(ss.colSpacing))
			ss.initializePlan()
			for ssu in ss.execPlan:
				print("\t\tPOS: " + str(ssu.x) + "," + str(ssu.y) )
	else:
		print("All Batches")
		batch_list = cnco2.BatchRuns().getAll()
		for batch in batch_list:
			print(batch.created + ": " + batch.accessKey + " " + batch.name)
