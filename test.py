from pymongo import MongoClient
from main import get_module
import math

client = MongoClient(
    "mongodb+srv://admin:ZpwHfTeZDM2ACkBM@cluster0.vqrib.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.myFirstDatabase

# get LT3
category = get_module('c1234-2', db)
students = category["students"]

new_hall = {"name": "LTUG"}

for student in students:
    if student["wildCard1"] == '' and student["wildCard2"] == '':
        student["wild"] = 'N'
    else:
        student["wild"] = 'Y'

category["students"] = students

this_db = db["categories"]
this_db.save(category)

if __name__ == '__main__':
    math.ceil(2.5)