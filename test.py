from pymongo import MongoClient
from main import get_module

client = MongoClient(
    "mongodb+srv://admin:ZpwHfTeZDM2ACkBM@cluster0.vqrib.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.myFirstDatabase

# get LT3
category = get_module('c1234-2', db)
halls = category["lectureHalls"]

new_hall = {"name": "LTUG"}

for hall in halls:
  if hall["name"] == 'LT2':
    new_hall["seatLayout"] = hall["seatLayout"]

halls.append(new_hall)

this_db = db["categories"]
this_db.save(category)
