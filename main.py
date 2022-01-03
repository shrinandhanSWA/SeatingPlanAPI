from pymongo import MongoClient
from seating.layout import Layout
from seating.seating_allocator import allocate_seats
from seating.student import Student


def get_lecture_hall(lecture_hall, db, module, just=False):
    """

    :param lecture_hall:
    :param db:
    :param module:
    :param just:
    :return:
    """
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
    """

    :param module:
    :param db:
    :return:
    """
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
                    elif occupant is not None and not occupant.get_real():
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
    """

    :param module:
    :param lecture_hall:
    :param db:
    :return:
    """
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
    """

    :param reqs:
    :return:
    """
    req_list = reqs.split(',')
    out = {}

    for req in req_list:
        if req == '':
            continue
        name, seat = req.split('-')
        out[seat] = name

    return out


def get_blanks(blanks):
    """

    :param blanks:
    :return:
    """
    blank_list = blanks.split(',')

    out = set(blank_list)
    out.remove('')

    return out


def main(module, lecture_hall, filters, reqs, blanks):
    """

    :param module:
    :param lecture_hall:
    :param filters:
    :param reqs:
    :param blanks:
    :return:
    """
    client = MongoClient(
        "mongodb+srv://admin:ZpwHfTeZDM2ACkBM@cluster0.vqrib.mongodb.net/"
        "myFirstDatabase?retryWrites=true&w=majority")
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
    people = get_students(students)

    # generate layout from lecture hall
    # takes in list of unavailable seats to blank out beforehand
    # takes in the reqs and student list to put people in place beforehand
    layout = Layout(lecture_hall, reqs, people, blanks)

    if not layout.is_valid():
        return -2  # user entered a bad combo

    names = set(reqs.values())
    people = list(filter(lambda person: person.get_name() not in names,
                         people))
    # remove people who have been dealt with in reqs

    # block alternate seats
    # layout.block_alternate_seats()

    # get number of seats in the lecture hall
    no_seats -= len(reqs)
    no_seats -= len(blanks)

    # allocate seats
    remaining = allocate_seats(layout, people, filters, no_seats)

    if remaining:
        # failed to allocate students
        return None

    # turn layout into list of lists based on input
    output = generate_layout(layout, lecture_hall)

    return output


def get_students(students):
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
    return people


if __name__ == '__main__':
    print(
        main('c1234-2', 'LTUG', 'wild,nationality,', 'Gisela Peters-3,', '1,'))
