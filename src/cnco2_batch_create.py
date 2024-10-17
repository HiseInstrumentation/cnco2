import cnco2
import sys
import sqlite3

cnco2.getAbout()

batch_template_id = sys.argv[1]

new_batch_key = cnco2.BatchRuns.createFromTemplate(batch_template_id)

print("New Batch Key: " + new_batch_key)
