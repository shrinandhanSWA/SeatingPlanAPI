from pymongo import MongoClient
from seating.layout import Layout
from seating.seating_allocator import allocate_seats
from seating.student import Student

client = MongoClient(
    "mongodb+srv://admin:ZpwHfTeZDM2ACkBM@cluster0.vqrib.mongodb.net/"
    "myFirstDatabase?retryWrites=true&w=majority")
db = client.myFirstDatabase


def get_lecture_hall(lecture_hall, db, module, just=False):
    lecture_halls = get_module(module, db)["lectureHalls"]

    hall = None

    for hal in lecture_halls:
        if hal["name"] == lecture_hall:
            hall = hal
            break

    if not hall:
        # hall not found
        return -1

    if just:
        return hall

    seats = hall["seatLayout"]
    no_seats = hall["seatCount"] - 1

    out = []

    for seat in seats:
        this_subsection_seats = []
        this_subsection = seat["seats"]

        for row in this_subsection:
            this_row = []

            for seat1 in row:
                this_row.append(seat1["seat_no"])

            this_subsection_seats.append(this_row)

        out.append(this_subsection_seats)

    return out, no_seats


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
                    if seat.is_available():
                        name = {"name": occupant, "username": "", "gender": "",
                                "nationality": "", "group": ""}
                    elif occupant is not None and occupant.get_name() == 'fh5':
                        name = {"name": seat.get_seat_no(), "username": "",
                                "gender": "", "nationality": "",
                                "group": ""}
                    else:
                        name = {"name": occupant.get_name(),
                                "username": occupant.get_username(),
                                "gender": occupant.get_gender(),
                                "nationality": occupant.get_nationality(),
                                "group": occupant.get_group(),
                                "wild": occupant.get_wild()}

                row_output.append(name if occupant else "null")

            sub_output.append(row_output)

        output.append(sub_output)

    return output


def get_filters(filters):
    return filters.split(',')


def generate_seat_numbers(module, lecture_hall, db):
    hall = get_lecture_hall(lecture_hall, db, module, True)

    seats = hall["seatLayout"]
    count = 1

    for seat in seats:
        this_subsection = seat["seats"]

        for row in this_subsection:
            for seat in row:
                seat["seat_no"] = count
                count += 1

    category = get_module(module, db)
    halls = category["lectureHalls"]

    for hall in halls:
        if hall["name"] == lecture_hall:
            hall["seatLayout"] = seats
            hall["seatCount"] = count

    this_db = db["categories"]
    this_db.save(category)


def get_reqs(reqs):
    req_list = reqs.split(',')
    out = {}

    for req in req_list:
        if req == '':
            continue
        item = req.split('-')
        out[item[1]] = item[0]

    return out


def get_blanks(blanks):
    blank_list = blanks.split(',')
    out = set(blank_list)

    out.remove('')

    return out


def main(module, lecture_hall, filters, reqs, blanks):
    client = MongoClient(
        "mongodb+srv://admin:ZpwHfTeZDM2ACkBM@cluster0.vqrib.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.myFirstDatabase

    if filters == 'seat':
        # seat number generation
        generate_seat_numbers(module, lecture_hall, db)
        return []

    # parse given filters
    filters = get_filters(filters)

    # parse given blanks
    blanks = get_blanks(blanks)

    # parse given requirements
    reqs = get_reqs(reqs)

    # get lecture hall
    lecture_hall, no_seats = get_lecture_hall(lecture_hall, db, module)

    if lecture_hall == -1:
        return -1

    # get list of students taking this module
    students = get_module(module, db)["students"]

    # turn students into list of people
    people = []

    for student in students:

        person = Student(student["name"], student["shortcode"],
                         student["gender"], student["nationality"],
                         student["group"])
        if 'disability' in student:
            person.set_disability(student["disability"])
        if 'wild' in student:
            person.set_wild(student["wild"])

        people.append(person)

    # generate layout from lecture hall
    # takes in list of unavailable seats to blank out beforehand
    # takes in the reqs and student list to put people in place beforehand
    layout = Layout(lecture_hall, reqs, people, blanks)

    if not layout.is_valid():
        return -2  # user entered a bad combo

    # remove people who have been dealt with in reqs
    for _, value in reqs.items():
        # remove person(value) from list
        for person in people:
            if person.get_name() == value:
                people.remove(person)

    # block alternate seats
    # layout.block_alternate_seats()

    # get number of seats in the lecture hall
    no_seats -= len(reqs)
    no_seats -= len(blanks)

    # allocate seats
    people = allocate_seats(layout, people, filters, no_seats)

    if len(people) != 0:
        # failed to allocate students
        return None

    # turn layout into list of lists based on input
    output = generate_layout(layout, lecture_hall)

    return output


if __name__ == '__main__':
    print(
        main('c1234-2', 'LTUG', 'wild,nationality,', 'Gisela Peters-3,', '1,'))
    # print(get_blanks("1,"))
    # print(main('c1234-2', 'LTUG', 'seat', 'Brianna Morrison-1,Gisela Peters-3,'))
    # client = MongoClient(
    #     "mongodb+srv://admin:ZpwHfTeZDM2ACkBM@cluster0.vqrib.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    # db = client.myFirstDatabase
    # generate_seat_numbers('c1234-2', 'LT3', db)
    # print(get_reqs('aayush-1,nandhu-2'))
    print()
