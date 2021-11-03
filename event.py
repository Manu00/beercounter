import datetime
import json
import uuid
import db

class event:

    #Global Attributes
    event_id = ""
    name = "test"
    entities = []
    isPublic = True

    #Database conn
    database = None

    def __init__(self, name, isNew):
        self.database = db.db()
        self.name = name
        if isNew:
            self.event_id = uuid.uuid4().hex
            self.database.storeEvent(self.event_id, name)
        

    def getId(self):
        return self.event_id

    def setId(self, newId):
        self.event_id = newId

    def setName(self, newName):
        self.name = newName

    def addEntity(self, toAdd):
        for entity in self.entities:
            if entity == toAdd:
                return False
            
        self.entities.append(toAdd)
        return True

    def removeEntity(self, toRemove):
        for entity in self.entities:
            if entity == toRemove:
                self.entities.remove(toRemove)
                return True
        return False

    def setVisibility(self, visible):
        self.isPublic = visible

    def getData(self, timescale, items):
        test = {
            "event_id": self.event_id,
            "items": [

            ]
        }
        startTime = datetime.datetime.now() - datetime.timedelta(0, 0, 0, 0, 0, timescale, 0)
        endTime = datetime.datetime.now()
        #change to items.values
        for item in items.keys():
            test["items"].append({"name": item, "size": self.database.getItemcount(self.event_id, item), "timestamps": self.database.getItem(self.event_id, startTime, endTime, item)})
        result = json.dumps(test, indent = 4)
        print("getData() resonese:")
        print(result)
        return result

    def storeData(self, time, name, id):
        self.database.storeItem(self.event_id, time, name, id)
