from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://admin:ZpwHfTeZDM2ACkBM@cluster0.vqrib.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.myFirstDatabase


def get_lecture_hall(lecture_hall, db):
    halls = db["lecture_halls"]

    hall = halls.find({"name": lecture_hall})

    for h in hall:
        print(h["layout"])


def get_module(module, db):
    module_db = db["categories"]

    students = module_db.find({"slug": module})

    for student in students:
        print(student)


def main(module, lecture_hall, filters):
    # get list of students
    client = MongoClient(
        "mongodb+srv://admin:ZpwHfTeZDM2ACkBM@cluster0.vqrib.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.myFirstDatabase

    get_lecture_hall(lecture_hall, db)
    mydb = db["lecture_halls"]

    get_module(module, db)

    return 2

    # TODO:
    """
    Firstly check if the lecture hall has enough capacity(with or without social distancing)
    Then try to allocate based on the filters
    """


if __name__ == '__main__':
    main('rohan-testing', 'ACEX554', 'grades')
