from logging import shutdown
from flask import Flask, redirect, url_for, request, render_template
import datetime, os, sys
import db

app = Flask(__name__)

#global sht
result = 0
database = db.db()

@app.route("/")
def index():
    tests()
    return render_template("index.html")

@app.route("/api", methods = ['POST', 'GET'])
def api():
    if request.method == 'POST':
      result = request.get_json()
    else:
      return "<p>result</p>"

def tests():
    database.store_item(datetime.time, "Bier", 1)
    database.get_item()