from logging import PlaceHolder, shutdown
from flask import Flask, redirect, url_for, request, render_template
import datetime
import os
import sys
import uuid
import db
import json

app = Flask(__name__)

#global sht
result = 0
database = db.db()


@app.route("/", methods=["POST", "GET"])
def index():
    listOfItems = database.getDistinct()
    items = []
    checked = []
    for item in listOfItems:
        items.append(item[0])
    #tests()
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


@app.route("/api", methods=["POST", "GET"])
def api():
    if request.method == "POST":
        item = request.json.get("name")
        database.storeItem(datetime.datetime.now(), item, uuid.uuid4())
        print(item)
        return "ok"
    else:
        return "ok"


def getData(timescale, items):
    test = {
      "items": [

      ]
    }
    startTime = datetime.datetime.now() - datetime.timedelta(0, 0, 0, 0, 0, timescale, 0)
    endTime = datetime.datetime.now()
    for item in items.keys():
        test["items"].append({"name": item, "size": database.getItemcount(item), "timestamps": database.getItem(startTime, endTime, item)})
    result = json.dumps(test, indent = 4)
    return result


def tests():
    #database.storeItem(datetime.time, "Bier", 1)
    getData(48, {"wasser": "wasser", "weizen": "weizen"})
    #database.getItem(datetime.datetime.now() - datetime.timedelta(hours=24), datetime.datetime.now(), "wasser")


class itemCollection:
  size = 0
  name = ""
  timestamps = []

  def __init__(self, size, name, timestamps) -> None:
      size = size
      name = name
      timestamps = timestamps
