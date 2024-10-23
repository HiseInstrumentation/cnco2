import cnco2
import sys
import sqlite3

cnco2.getAbout()

batch_access_key = sys.argv[1]


batch = cnco2.BatchRuns().getByAccessKey(batch_access_key)

print("Batch: ")
print(batch.name)
print(batch.description)
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
	
