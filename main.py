from pymongo import MongoClient
from seating.layout import Layout
from seating.seating_allocator import allocate_seats
from seating.student import Student

client = MongoClient(
    "mongodb+srv://admin:ZpwHfTeZDM2ACkBM@cluster0.vqrib.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.myFirstDatabase


def get_lecture_hall(lecture_hall, db, module):

    lecture_halls = get_module(module, db)["lectureHalls"]

    hall = None

    for hal in lecture_halls:
        if hal["name"] == lecture_hall:
            hall = hal
            break

    if not hall:
        # hall not found
        return -1

    seats = hall["seatLayout"]

    out = []

    for seat in seats:
        this_subsection_seats = []
        this_subsection = seat["seats"]

        for row in this_subsection:
            this_row = []

            for seat in row:
                this_row.append('empty')

            this_subsection_seats.append(this_row)

        out.append(this_subsection_seats)

    return out


def get_module(module, db):
    module_db = db["categories"]

    students = module_db.find({"slug": module})

    for student in students:
        return student


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


def get_filters(filters):
    return filters.split(',')


def main(module, lecture_hall, filters):
    client = MongoClient(
        "mongodb+srv://admin:ZpwHfTeZDM2ACkBM@cluster0.vqrib.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.myFirstDatabase

    # parse given filters
    filters = get_filters(filters)

    # get lecture hall
    lecture_hall = get_lecture_hall(lecture_hall, db, module)

    if lecture_hall == -1:
        return -1

    # generate layout from lecture hall
    layout = Layout(lecture_hall)

    # get list of students taking this module
    students = get_module(module, db)["students"]

    # turn students into list of people
    people = []

    for student in students:

        person = Student(student["name"], student["shortcode"], student["gender"], student["nationality"], student["group"])

        if 'disability' in student:
            person.set_disability(student["disability"])
        if 'wild1' in student:
            person.set_wild1(student["wild1"])
        if 'wild2' in student:
            person.set_wild1(student["wild2"])

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
    print(main('c1234-2', 'ACEX554', 'nationality'))
