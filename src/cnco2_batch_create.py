import cnco2
import sys
import sqlite3

cnco2.getAbout()

batch_template_id = sys.argv[1]

new_batch_key = cnco2.BatchRuns.createFromTemplate(batch_template_id)
cnco2.Logging.write("Creating new batch from template "+batch_template_id+".", True)
cnco2.Logging.write("New Batch Key: " + new_batch_key, True)
