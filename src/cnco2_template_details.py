import cnco2
import sys
import sqlite3

if __name__ == '__main__':
	
    cnco2.getAbout()
	
    templates = cnco2.BatchTemplates.getAll()

    print("\nSystem Templates\n")
    
    print(f"{'Name' : <20}{'Access Key' : ^20}{'Description' : ^40}")
    
    for t in templates:
        print(f"{t.name : <20}{t.accessKey : ^20}{t.description : ^40}")
