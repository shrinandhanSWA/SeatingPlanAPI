from pymongo import MongoClient
from seating.layout import Layout
from seating.seating_allocator import allocate_seats
from seating.student import Student

client = MongoClient(
    "mongodb+srv://admin:ZpwHfTeZDM2ACkBM@cluster0.vqrib.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.myFirstDatabase


def get_lecture_hall(lecture_hall, db):
    halls = db["lecture_halls"]

    hall = halls.find({"name": lecture_hall})

    for h in hall:
        return h["layout"]


def get_module(module, db):
    module_db = db["categories"]

    students = module_db.find({"slug": module})

    for student in students:
        return student["students"]


def generate_layout(layout, lecture_hall):
    output = []

    for i, subsection in enumerate(lecture_hall):
        sub_output = []

        for j, row in enumerate(subsection):
            row_output = []

            for k, _ in enumerate(row):
                seat = layout.get_subsections()[i].get_rows()[j][k]

                occupant = None
                name = None

                if seat.get_seat_no() != -1:
                    occupant = seat.get_occupant()
                    if occupant == 'empty':
                        name = 'empty'
                    else:
                        name = occupant.get_username()

                row_output.append(name if occupant else "null")

            sub_output.append(row_output)

        output.append(sub_output)

    return output


def main(module, lecture_hall, filters):
    # get list of students
    client = MongoClient(
        "mongodb+srv://admin:ZpwHfTeZDM2ACkBM@cluster0.vqrib.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.myFirstDatabase

    # get lecture hall
    lecture_hall = get_lecture_hall(lecture_hall, db)

    # generate layout from lecture hall
    layout = Layout(lecture_hall)

    # get list of students taking this module
    students = get_module(module, db)

    # turn students into list of people
    people = []

    for student in students:

        person = Student(student["name"], student["last_name"], student["shortcode"])

        if 'grade' in student:
            person.set_predicted_grade(student["grade"])
        if 'nationality' in student:
            person.set_nationality(student["nationality"])

        people.append(person)

    # block alternate seats
    layout.block_alternate_seats()

    # allocate seats
    allocate_seats(layout, people, [filters])

    if len(people) != 0:
        # failed to allocate students
        return None

    # turn layout into list of lists based on input
    output = generate_layout(layout, lecture_hall)

    return output


if __name__ == '__main__':
    main('nandhu-testing', 'ACEX554', 'nationality')
