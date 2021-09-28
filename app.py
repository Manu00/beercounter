from logging import shutdown
from flask import Flask, redirect, url_for, request, render_template
import datetime, os, sys, uuid
import db
import json

app = Flask(__name__)

#global sht
result = 0
database = db.db()

@app.route("/", methods = ["POST", "GET"])
def index():
    listOfItems = database.get_distinct()
    items = list
    for item in listOfItems:
      items.append(item[0])
    if request.method == "GET":
        return render_template("index.html", len = len(items), items = items)
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
          pass
        #form_data = database.get_distinct()
        print(form_data)
        return render_template("index.html", len = len(items), items = items)

@app.route("/api", methods = ["POST", "GET"])
def api():
    if request.method == "POST":
      item = request.json.get("name")
      database.store_item(datetime.datetime.now(), item, uuid.uuid4())
      print(item)
      return "ok"
    else:
      return "ok"

def tests():
    database.store_item(datetime.time, "Bier", 1)
    database.get_item()