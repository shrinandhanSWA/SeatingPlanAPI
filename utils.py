from seating.student import Student
from seating.factors import WILD


def get_students(students):
    people = []

    for student in students:

        person = Student(student["name"], student["shortcode"],
                         student["gender"], student["nationality"],
                         student["group"])

        if 'disability' in student:
            person.set_disability(student["disability"])

        if WILD in student:
            person.set_wild(student["wild"])
        else:
            isWild = student["wildCard1"] != '' or student["wildCard2"] != ''
            person.set_wild(str(isWild))

        people.append(person)
    return people


def check_error(no_seats, people, reqs, blanks, social):
    peeps = len(people)
    social = int(social)

    # first check, literally too many people
    if peeps > no_seats:
        return -7, peeps  # no of students in module
    # second check, too many blanked out seats
    if peeps > no_seats - len(blanks):
        return -2, len(blanks) - (no_seats - peeps)  # no of blanks to be removed
    # check if social distancing would be a problem
    if peeps > no_seats / 2 and social:
        # odd number: will be floored, even is a flat division
        return -3, None
    # check if pure social distancing is fine, but adding the blanked seats add confusion
    # first step is to parse the blanks and find out how many more are needed(so even numbers)
    # reqs: {'3': 'Gisela Peters'}
    extra = 0
    for seat in blanks:
        seat_no = int(seat)
        if seat_no % 2 == 0:
            extra += 1
    if peeps > no_seats / 2 - extra and social:
        # both are there and it causes an issue
        return -4, math.ceil(extra - (no_seats / 2 - peeps))

    # check each requirement
    for seat, person in reqs.items():
        # if seat is an odd number we fail automatically if social distancing is enabled
        seat_no = int(seat)
        if seat_no % 2 != 0 and social:
            return -5, person  # person who is bad

        # go through blanks and check
        for blank in blanks:
            blank_no = int(blank)
            if blank_no == seat_no:
                return -6, person  # person who is bad

    return 0, None


def get_topic(topic):
    client = MongoClient(
        "mongodb+srv://admin:ZpwHfTeZDM2ACkBM@cluster0.vqrib.mongodb.net/"
        "myFirstDatabase?retryWrites=true&w=majority")
    db = client.myFirstDatabase

    topic_db = db["topics"]
    topic_info = topic_db.find({"title": topic})

    for topic in topic_info:
        return topic


def save_topic(topic, seating):
    client = MongoClient(
        "mongodb+srv://admin:ZpwHfTeZDM2ACkBM@cluster0.vqrib.mongodb.net/"
        "myFirstDatabase?retryWrites=true&w=majority")
    db = client.myFirstDatabase

    topic_db = db["topics"]
    topic_info = topic_db.find({"title": topic})

    for topic in topic_info:
        topic_info = topic
        break

    topic_info["content"] = seating

    topic_db.save(topic_info)


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
