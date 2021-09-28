import os
import sys
import sqlite3

class db:

    #check for existing database, create one if necessary
    def __init__(self):
        if os.path.exists("beercounter.db"):
            print("using existing database")
            connection = sqlite3.connect("beercounter.db", check_same_thread=False)
        else:
            print("creating new database")
            connection = sqlite3.connect("beercounter.db", check_same_thread=False)
            sql = "CREATE TABLE items(" \
                "time TEXT, " \
                "name TEXT, " \
                "id TEXT PRIMARY KEY)"
            cursor.execute(sql)
            connection.commit()
    
    def closeDb(self):
        connection.commit()
        connection.close()
    
    def storeItem(self, time, name, id):
        #sql = "INSERT INTO items VALUES(" + "'" + time + "', " + "'" + name + "', " + "'" + id + "')"
        #sql = "INSERT INTO items VALUES({time}, {name}, {id})"
        cursor.execute("INSERT INTO items VALUES(?,?,?)", (str(time), str(name), str(id)))
        print("Storing new data:")
        #print(time, name, id)
        #print(sql)
        #cursor.execute(sql)
        connection.commit()

    
    def getItemOLD(self):
        sql = "SELECT * FROM items"
        cursor.execute(sql)
        for dsatz in cursor:
            print(dsatz[0], dsatz[1])
    
    def getItem(self, startTime, endTime, item):
        cursor.execute("SELECT time FROM items WHERE strftime('%Y-%m-%d %H:%M:%S.%f', time) BETWEEN ? AND ? AND name = ?", (str(startTime), str(endTime), str(item)))
        print(cursor.fetchall())
        
    
    def getDistinct(self):
        sql = "SELECT DISTINCT name FROM items"
        cursor.execute(sql)
        return cursor.fetchall()

        
connection = sqlite3.connect("beercounter.db", check_same_thread=False)
cursor = connection.cursor()
