'''
    Copyright 2024, Hise Scientific Instrumentation, LLC

    cnco2_data.py

    Purpose:
    Database abstraction layer (SQLite3)
'''
import sqlite3

class CNCDataDB:
    def getOne(sql):
        con = sqlite3.connect("cnco2_data.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        
        res = cur.execute(sql).fetchone()
        
        con.close()
        
        return res

    
    def getAll(sql):
        con = sqlite3.connect("cnco2_data.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        
        res = cur.execute(sql).fetchall()
        con.close()
        return res
        
    def execute(sql):
        con = sqlite3.connect("cnco2_data.db")
        cur = con.cursor()
        
        res = cur.execute(sql)
        con.commit()
        con.close()

class CNCSystemDB:
    def getOne(sql):
        con = sqlite3.connect("cnco2.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        
        res = cur.execute(sql).fetchone()
        
        con.close()
        
        return res

    
    def getAll(sql):
        con = sqlite3.connect("cnco2.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        
        res = cur.execute(sql).fetchall()
        con.close()
        return res
        
    def execute(sql):
        con = sqlite3.connect("cnco2.db")
        cur = con.cursor()
        
        res = cur.execute(sql)
        con.commit()
        con.close()
