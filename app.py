from logging import PlaceHolder, shutdown
from flask import Flask, redirect, url_for, request, render_template, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
import datetime
import os
import sys
import uuid
import db
import event
import json
"""
Api docs
/api/ => POST {eventName: "", items: []}
/api/ => GET (get public events)
/api/<event_id> POST {event_id: "", timescale: "", items: {}} /not final
/api/<event_id> PUT {event_id: "", name: ""} /not final
"""

app = Flask(__name__)
api = Api(app)

#global sht
result = 0
database = db.db()
events = []

@app.before_first_request
def setup():
    pass
    #loadEvents()

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
        newEvent = event.Event(form_data.get("eventName"), True)
        events.append(newEvent)
        print(events)
        return render_template("start.html")
    pass


@app.route("/event/<event_id>", methods=["GET"])
def event_route(event_id):
    for event in events:
        if event.getId() == event_id:
            #event.getData()
            #print("found this in db: ")
            #print(event.getData(48, {"wasser": "wasser", "weizen": "weizen"}))
            
            #pass
            #this is a test
            return render_template("event.html")

            if request.method == "GET":
                return render_template("event.html")
            if request.method == "POST":
                #formData = request.form
                #result = processRequest(event.getId(), formData)
                
                return render_template("event.html")
        else:
            return render_template("error.html")

#todo check to not load same event multiple times
#"""Loads events from database at the program startup"""
def loadEvents():
    dbConn = db.db()
    oldEvents = dbConn.getEventIds()

    for oldEvent in oldEvents:
        oldEventName = dbConn.getEventName(oldEvent[0])
        toAdd = event.Event(oldEventName[0], False)
        toAdd.setId(oldEvent[0])
        events.append(toAdd)
        print(toAdd.getId())
    dbConn.closeDb()

class Get_api(Resource):
  
    # corresponds to the GET request.
    def get(self):
        jsonData = {
                "events": [],
            }
        for event in events:
            if event.isPublic:
                tempData = {"event_id": "", "items": []}
                itemsInEvent = event.getDistinct(event.getId())
                tempData["event_id"] = event.getId()
                tempData["items"] = itemsInEvent.get("items")
                jsonData["events"].append(tempData)
  
        return jsonify(jsonData)
  
    # Corresponds to POST request
    def post(self):
        event_id = request.json.get("event_id")
        timescale = int(request.json.get("timescale"))
        items = request.json.get("items")
        print(event_id)
        for event in events:
            if event.getId() == event_id:
                if items:
                    print("requesting items:")
                    print(items)
                    result = event.getData(timescale, items)
                    #result = event.getData(timescale, {"wasser": "wasser", "weizen": "weizen"})
                    print(result)
                    return jsonify(result)
                else:
                    tempData = {"event_id": event.getId(), "items": []}
                    tempData["items"] = event.getDistinct(event.getId()).get("items")
                    return jsonify(tempData)
            else:
                return jsonify({"message": "error no event with this id", "code": ""})
        return jsonify({"message": "error no event_id specified", "code": "001"})

class Store_api(Resource):
  
    # corresponds to the GET request.
    def get(self):
        pass
  
    # Corresponds to POST request
    def post(self):
        event_id = request.json.get("event_id")
        item = request.json.get("name")
        #database.storeItem(datetime.datetime.now(), item, uuid.uuid4())
        for event in events:
            if event.getId() == event_id:
                event.storeData(datetime.datetime.now(), item, uuid.uuid4())
                return jsonify({"message": "ok", "code": "200"})
            else:
                return jsonify({"message": "error cannot store data", "code": ""})


api.add_resource(Get_api, "/api/get")
api.add_resource(Store_api, "/api/store")

def tests():
    #database.storeItem(datetime.time, "Bier", 1)
    #getData(48, {"wasser": "wasser", "weizen": "weizen"})
    #database.getItem(datetime.datetime.now() - datetime.timedelta(hours=24), datetime.datetime.now(), "wasser")
    testEvent = event.event()

if __name__ == "__app__":
	app.run(debug=True, host='0.0.0.0', port=5050)