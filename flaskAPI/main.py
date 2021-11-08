from pymongo import MongoClient

client = MongoClient(
        "mongodb+srv://admin:ZpwHfTeZDM2ACkBM@cluster0.vqrib.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.test
db = db["students"]

def filter_students(module, mydoc):

    students = []

    for student in mydoc:
        modules = student['modules']
        if module in modules:
            students.append(student)

    return students


if __name__ == '__main__':
    # post = {"_id": 3, "name": "nandhu", "score": 5, "nationality": "Indian", "modules": ["c1234", "c2356"]}
    # db.insert_one(post)
    # post = {"_id": 2, "name": "aayush", "score": 5, "nationality": "Indian", "modules": ["c1234", "c2356", "e5693"]}
    # db.insert_one(post)

    mydoc = db.find()

    students = filter_students("e5693", mydoc)

    for x in students:
        print(x)

