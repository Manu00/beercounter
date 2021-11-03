from logging import PlaceHolder, shutdown
from flask import Flask, redirect, url_for, request, render_template
import datetime
import os
import sys
import uuid
import db
import event
import json

app = Flask(__name__)

#global sht
result = 0
database = db.db()
events = []

'''
@app.route("/", methods=["POST", "GET"])
def index():
    #this is a test
    print("loading old events")
    loadEvents()
    print(events)
    listOfItems = database.getDistinct("74068922ee0a4fb2873b1607bfc48667")
    items = []
    checked = []
    for item in listOfItems:
        items.append(item[0])
    #tests()
    data = ""
    if request.method == "GET":
        return render_template("index.html", checked=checked, items=items, data = data)
    if request.method == "POST":
        form_data = request.form
        if form_data == "1h":
            pass
        elif form_data == "2h":
            pass
        elif form_data == "4h":
            pass
        elif form_data == "8h":
            pass
        else:
            for i in form_data.values():
                checked.append(i)
        #form_data = database.get_distinct()
        print(form_data)
        print(checked)
        return render_template("index.html", checked=checked, items=items, data = data)
'''

@app.route("/", methods=["POST", "GET"])
def test():
    loadEvents()
    if request.method == "GET":
        return render_template("start.html")
    if request.method == "POST":

        #get formdata
        form_data = request.form
        print(form_data)

        #create new event and add it to the list
        newEvent = event.event(form_data.get("eventName"), True)
        events.append(newEvent)
        print(events)
        return render_template("start.html")
    pass


@app.route("/event/<event_id>", methods=["POST", "GET"])
def hello_user(event_id):
    for event in events:
        if event.getId() == event_id:
            #event.getData()
            print("found this in db: ")
            print(event.getData(48, {"wasser": "wasser", "weizen": "weizen"}))
            
            pass
            #this is a test

            if request.method == "GET":
                return render_template("event.html")
            if request.method == "POST":
                formData = request.form
                result = processRequest(event.getId(), formData)
                
                return render_template("event.html")
        else:
            return render_template("error.html")

@app.route("/api/<action>", methods=["POST", "GET"])
def api(action):
    if action == "post":
        if request.method == "POST":
            event_id = request.json.get("event_id")
            item = request.json.get("name")
            #database.storeItem(datetime.datetime.now(), item, uuid.uuid4())
            for event in events:
                if event.getId() == event_id:
                    event.storeData(datetime.datetime.now(), item, uuid.uuid4())
                    return "ok"
                else:
                    return "error no event with this id"
            #print(item)
            #return "ok"
    #get data from requested event
    if action == "get":
        if request.method == "POST":
            event_id = request.json.get("event_id")
            timescale = int(request.json.get("timescale"))
            items = request.json.get("items")
            print(items)
            for event in events:
                if event.getId() == event_id:
                    result = event.getData(timescale, {"wasser": "wasser", "weizen": "weizen"})
                    print(result)
                    return result
                else:
                    return "error no event with this id"
    #get all public events
    if action == "get-public":
        if request.method == "GET":
            jsonData = {
                "events": [

                ]
            }
            for event in events:
                if event.isPublic:
                    jsonData["events"].append({"event_id": event.getId()})
            result = json.dumps(jsonData, indent = 4)
        return result
    else:
        return "something is very wrong"

#is not needed anymore
def getData(timescale, items):
    jsonData = {
      "items": [

      ]
    }
    startTime = datetime.datetime.now() - datetime.timedelta(0, 0, 0, 0, 0, timescale, 0)
    endTime = datetime.datetime.now()
    for item in items.keys():
        jsonData["items"].append({"name": item, "size": database.getItemcount(item), "timestamps": database.getItem(startTime, endTime, item)})
    result = json.dumps(jsonData, indent = 4)
    return result

def loadEvents():
    dbConn = db.db()
    oldEvents = dbConn.getEventIds()

    for oldEvent in oldEvents:
        oldEventName = dbConn.getEventName(oldEvent[0])
        toAdd = event.event(oldEventName[0], False)
        toAdd.setId(oldEvent[0])
        events.append(toAdd)
    dbConn.closeDb()

#TODOO
def processRequest(event_id, formData):
    pass



def tests():
    #database.storeItem(datetime.time, "Bier", 1)
    getData(48, {"wasser": "wasser", "weizen": "weizen"})
    #database.getItem(datetime.datetime.now() - datetime.timedelta(hours=24), datetime.datetime.now(), "wasser")
    testEvent = event.event()
