"""
Daten aus MongoDB auslesen um den Verbrauch in einem bestimmten interval
zu
"""

import pymongo
from pymongo import MongoClient

cluster = MongoClient(host="35.156.7.227", port=27017, username="admin",
                      password="Asdfgh123456")
cluster.list_database_names()

db = cluster["ocpp16"]

db.list_collection_names()

ChargePointRequest = db["ChargePointRequest"]
MeterValuesSnapshot = db["MeterValuesSnapshot"]
ChargePoint = db["ChargePoint"]

payload = []
results = MeterValuesSnapshot.find({"ChargepointId": "CP009"})
for result in results:
    payload.append(result["Payload"])


payload
