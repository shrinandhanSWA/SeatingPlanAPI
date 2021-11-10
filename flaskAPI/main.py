from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://admin:ZpwHfTeZDM2ACkBM@cluster0.vqrib.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.myFirstDatabase

def get_lecture_hall(lecture_hall):
    hall = db[lecture_hall]

    for h in hall:
        print(h)


def main(module, lecture_hall, filters):
    # get list of students
    client = MongoClient(
        "mongodb+srv://admin:ZpwHfTeZDM2ACkBM@cluster0.vqrib.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.myFirstDatabase
    db = db["lecture_halls"]

    mydoc = db.find({ "name": lecture_hall })

    for x in mydoc:
        return x["layout"]

    # TODO:
    """
    Firstly check if the lecture hall has enough capacity(with or without social distancing)
    Then try to allocate based on the filters
    """


if __name__ == '__main__':
    # post = {"_id": 3, "name": "nandhu", "score": 5, "nationality": "Indian", "modules": ["c1234", "c2356"]}
    # db.insert_one(post)
    # post = {"_id": 2, "name": "aayush", "score": 5, "nationality": "Indian", "modules": ["c1234", "c2356", "e5693"]}
    # db.insert_one(post)
    # print(get_lecture_hall('ACEX554'))
    main('c1234', 'ACEX554', 2)