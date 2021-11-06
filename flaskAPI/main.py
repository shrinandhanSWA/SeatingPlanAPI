import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://mb6118:mb6118@cluster0.jpzpy.mongodb.net/test?retryWrites=true&w=majority")
db = cluster.test
collection = db.test

post = {"_id":0, "name": "tim", "score": 5}
collection.insert_one(post)

if __name__ == '__main__':
    post = {"_id": 0, "name": "tim", "score": 5}
    collection.insert_one(post)
