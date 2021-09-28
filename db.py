import os
import sys
import sqlite3

class db:

    def __init__(self):
        #look for database file
        if os.path.exists("beercounter.db"):
            print("using existing database")
            setup_db()
            connection = sqlite3.connect("beercounter.db", check_same_thread=False)
        else:
            print("creating new database")
            setup_db()
    
    def close_db(self):
        connection.commit()
        connection.close()
    
    def store_item(self, time, name, id):
        #sql = "INSERT INTO items VALUES(" + "'" + time + "', " + "'" + name + "', " + "'" + id + "')"
        #sql = "INSERT INTO items VALUES({time}, {name}, {id})"
        cursor.execute("INSERT INTO items VALUES(?,?,?)", (str(time), str(name), int(id)))
        #print(sql)
        #cursor.execute(sql)
        connection.commit()

    
    def get_item(self):
        sql = "SELECT * FROM items"
        cursor.execute(sql)
        for dsatz in cursor:
            print(dsatz[0], dsatz[1])

        
connection = sqlite3.connect("beercounter.db", check_same_thread=False)
cursor = connection.cursor()

#basic tasks to create db
def setup_db():
    connection = sqlite3.connect("beercounter.db", check_same_thread=False)
    sql = "CREATE TABLE items(" \
      "time TEXT, " \
      "name TEXT, " \
      "id INTEGER PRIMARY KEY)"
    cursor.execute(sql)
    connection.commit()
    connection.close()