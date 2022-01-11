from pymongo import MongoClient
from main import main
from utils import get_students, get_module
import math


# testing that no student was accidentally left out
def test_all_students_allocated(db):
    # calling the main function c1234-2 is our test module , the hall does not matter, no allocations are done,
    # no seats are blank, and social distancing is disabled
    final, _ = main('c1234-2', 'LTUG', 'wild,', ',', ',', '0')

    # all the students
    people = get_module('c1234-2', db)["students"]
    students = get_students(people)
    students_string = []

    for student in students:
        students_string.append(student.get_username())

    students = students_string

    # go through the final list and remove students that are found
    for subsection in final:
        for row in subsection:
            for seat in row:
                occupant = seat["username"]
                if occupant in students:
                    students.remove(occupant)

    # no students should be left out
    assert len(students) == 0


def test_blank_seats_left_out():
    # blank seats are 2, 4, 6, 20
    final, _ = main('c1234-2', 'LTUG', 'wild,', ',', '2,4,6,20,', '0')
    i = 0

    for subsection in final:
        for row in subsection:
            for seat in row:
                occupant = seat["username"]
                if i == 1 or i == 3 or i == 5 or i == 19:
                    assert occupant == ''
                i += 1


def test_allocated_students_allocated():
    # Gisela to 3 and Troy to 20
    final, _ = main('c1234-2', 'LTUG', 'wild,', 'Gisela Peters-3,Troy Moran-12,', ',', '0')
    i = 0

    for subsection in final:
        for row in subsection:
            for seat in row:
                occupant = seat["name"]
                if i == 2: # 0 indexed
                    assert occupant == 'Gisela Peters'
                if i == 11:
                    assert occupant == 'Troy Moran'
                if i == 12:
                    break # simple short circuit
                i += 1


if __name__ == '__main__':

    client = MongoClient(
        "mongodb+srv://admin:ZpwHfTeZDM2ACkBM@cluster0.vqrib.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.myFirstDatabase

    test_all_students_allocated(db)
    test_blank_seats_left_out()
    test_allocated_students_allocated()

    print("All tests passed!")