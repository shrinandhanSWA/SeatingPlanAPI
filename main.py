from pymongo import MongoClient
import math

from seating.evolution_strategy import EvolutionStrategy
from seating.layout import Layout
from seating.seating_allocator import allocate_seats
from seating.seating_mutator import SeatingMutator
from seating.student import Student
from seating.factors import WILD
from seating.fitness_scorer import FitnessScorer


def check_error(no_seats, people, reqs, blanks, social):

    peeps = len(people)
    social = int(social)

    # first check, literally too many people
    if peeps > no_seats:
        return -7, peeps # no of students in module
    # second check, too many blanked out seats
    if peeps > no_seats - len(blanks):
        return -2, len(blanks) - (no_seats - peeps) # no of blanks to be removed
    # check if social distancing would be a problem
    if peeps > no_seats / 2 and social:
        # odd number: will be floored, even is a flat division
        return -3, None
    # check if pure social distancing is fine, but adding the blanked seats
    # add confusion first step is to parse the blanks and find out how many
    # more are needed(so even numbers) reqs: {'3': 'Gisela Peters'}
    extra = 0
    for seat in blanks:
        seat_no = int(seat)
        if seat_no % 2 == 0:
            extra += 1
    if peeps > no_seats / 2 - extra and social:
        # both are there and it causes an issue
        return -4, math.ceil(extra - (no_seats/2 - peeps))

    # check each requirement
    for seat, person in reqs.items():
        # if seat is an odd number we fail automatically if social distancing
        # is enabled
        seat_no = int(seat)
        if seat_no % 2 != 0 and social:
            return -5, person # person who is bad

        # go through blanks and check
        for blank in blanks:
            blank_no = int(blank)
            if blank_no == seat_no:
                return -6, person # person who is bad

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


def generate_layout(layout, lecture_hall):
    """

    :param layout:
    :param lecture_hall:
    :return:
    """
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


def main(module, lecture_hall, filters, reqs, blanks, social):
    """

    :param module:
    :param lecture_hall: list of list of seat numbers
    :param filters: factors for sorting algorithm
    :param reqs: students already assigned to seats in the frontend
    :param blanks: seats to be left blank
    :return:
    """
    client = MongoClient(
        "mongodb+srv://admin:ZpwHfTeZDM2ACkBM@cluster0.vqrib.mongodb.net/"
        "myFirstDatabase?retryWrites=true&w=majority")
    db = client.myFirstDatabase

    if filters == 'seat':
        # seat number generation
        generate_seat_numbers(module, lecture_hall, db)
        return [], None

    # parse given filters
    filters = get_filters(filters)

    # parse given blanks
    blanks = get_blanks(blanks)

    # parse given requirements
    reqs = get_reqs(reqs)

    # get lecture hall
    lecture_hall, no_seats = get_lecture_hall(lecture_hall, db, module)

    if lecture_hall == -1:
        return -1, None

    # get list of students taking this module
    students = get_module(module, db)["students"]

    # turn students into list of students
    people = get_students(students)

    error, meta = check_error(no_seats, people, reqs, blanks, social)

    # parse error anre print message
    if error != 0:
        return error, meta

    # generate layout from lecture hall
    # takes in list of unavailable seats to blank out beforehand
    # takes in the reserved and student list to put students in place beforehand
    layout = Layout(lecture_hall, reqs, people, blanks)

    names = set(reqs.values())
    people = list(filter(lambda person: person.get_name() not in names,
                         people))
    # remove students who have been dealt with in reserved

    # get number of seats in the lecture hall
    no_seats -= len(reqs)
    no_seats -= len(blanks)

    # allocate seats
    factors = filters
    remaining = allocate_seats(layout, people, filters, no_seats,
                               get_evolutionary_strategy(factors),
                               names)

    if remaining:
        print(remaining)
        # failed to allocate students
        return None

    # turn layout into list of lists based on input
    output = generate_layout(layout, lecture_hall)

    return output, None


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


EPOCHS = 100
MU = 2
LAMBDA = 5 * MU

INITIAL_SWAP_RATE = 0.5
MIN_SWAP_RATE = 0.1
DECAY_RATE = 0.95


def get_evolutionary_strategy(factors):
    fitness_scorer = FitnessScorer(factors)
    seating_mutator = SeatingMutator(swap_rate=INITIAL_SWAP_RATE,
                                     min_swap_rate=MIN_SWAP_RATE)

    evolution_strategy = EvolutionStrategy(mu=MU, lambda_=LAMBDA,
                                           factors=factors,
                                           mutator=seating_mutator,
                                           scorer=fitness_scorer)
    return evolution_strategy


if __name__ == '__main__':
    print(main('c1234-2', 'LTUG', 'gender,', 'Gisela Peters-3,', '1,2,', '0'))