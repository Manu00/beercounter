import os
from sqlite3.dbapi2 import Connection
import sys
import sqlite3

from event import event


class db:

    connection = None
    cursor = None

    # check for existing database, create one if necessary
    def __init__(self):
        if os.path.exists("beercounter.db"):
            print("using existing database")
            self.connection = sqlite3.connect("beercounter.db", check_same_thread=False)
            self.cursor = self.connection.cursor()
        else:
            print("creating new database")
            self.connection = sqlite3.connect("beercounter.db", check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute("CREATE TABLE items(event_id TEXT, time TEXT, name TEXT, id TEXT PRIMARY KEY)")
            self.cursor.execute("CREATE TABLE events(event_id TEXT PRIMARY KEY, name TEXT)")
            self.connection.commit()

    def closeDb(self):
        self.connection.commit()
        self.connection.close()

    def storeItem(self, event_id, time, name, id):
        #sql = "INSERT INTO items VALUES(" + "'" + time + "', " + "'" + name + "', " + "'" + id + "')"
        #sql = "INSERT INTO items VALUES({time}, {name}, {id})"
        self.cursor.execute("INSERT INTO items VALUES(?,?,?,?)", (str(event_id), str(time), str(name), str(id)))
        print("Storing new data:")
        print(time, name, id)
        # print(sql)
        # cursor.execute(sql)
        self.connection.commit()

    def getItemOLD(self):
        sql = "SELECT * FROM items"
        self.cursor.execute(sql)
        for dsatz in self.cursor:
            print(dsatz[0], dsatz[1])

    def getItem(self,event_id, startTime, endTime, item):
        self.cursor.execute("SELECT time FROM items WHERE strftime('%Y-%m-%d %H:%M:%S.%f', time) BETWEEN ? AND ? AND name = ? AND event_id = ?", (str(startTime), str(endTime), str(item), str(event_id)))
        rows = self.cursor.fetchall()
        result = []
        for row in rows:
            result.append(row[0])
        return(result)

    def getItemcount(self, event_id, item):
        self.cursor.execute("SELECT count(*) FROM items WHERE name = ? AND name = ? AND event_id = ?", (str(item), str(item), str(event_id)))
        temp = self.cursor.fetchall()
        print("database has ")
        print(temp[0][0])
        print(" of item")
        print(item)
        return(int(temp[0][0]))

    def getDistinct(self, event_id):
        self.cursor.execute("SELECT DISTINCT name FROM items WHERE event_id = ? AND event_id = ?", (str(event_id), str(event_id)))
        return self.cursor.fetchall()

    def getEventIds(self):
        self.cursor.execute("SELECT DISTINCT event_id FROM events")
        return self.cursor.fetchall()

    def getEventName(self, event_id):
        self.cursor.execute("SELECT name FROM events WHERE event_id = ? AND event_id = ?", (str(event_id), str(event_id)))
        return self.cursor.fetchone()
    
    def storeEvent(self, event_id, name):
        self.cursor.execute("INSERT INTO events VALUES(?,?)", (str(event_id), str(name)))
        self.connection.commit()


#connection = sqlite3.connect("beercounter.db", check_same_thread=False)
#cursor = connection.cursor()
