from pymongo import MongoClient
from seating.layout import Layout
from seating.seating_allocator import allocate_seats
from seating.student import Student


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
        else:
            isWild = student["wildCard1"] != '' or student["wildCard2"] != ''
            person.set_wild(str(isWild))

        people.append(person)
    return people


if __name__ == '__main__':
    # print( main('c1234-2', 'LTUG', 'wild,nationality,', 'Gisela Peters-3,', '1,'))
    save_topic("aayush watch thiw", {
  "layout": [
    [
      [
        {
          "gender": "Male",
          "group": "19S Group 9",
          "name": "Laurel Buchanan",
          "nationality": "Sweden",
          "username": "zjf19",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 8",
          "name": "Brianna Morrison",
          "nationality": "United States",
          "username": "nl1119",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 1",
          "name": "Troy Moran",
          "nationality": "Brazil",
          "username": "dr1817",
          "wild": "Y"
        },
        {
          "gender": "Male",
          "group": "19S Group 7",
          "name": "Tana Osborn",
          "nationality": "United Kingdom",
          "username": "ge19",
          "wild": "N"
        },
        {
          "gender": "Female",
          "group": "19S Group 10",
          "name": "Clark Hale",
          "nationality": "Netherlands",
          "username": "ga5318",
          "wild": "N"
        },
        {
          "gender": "Female",
          "group": "19S Group 6",
          "name": "Astra Reynolds",
          "nationality": "South Korea",
          "username": "pt719",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 7",
          "name": "Tatiana Adams",
          "nationality": "Mexico",
          "username": "nd619",
          "wild": "Y"
        },
        {
          "gender": "Female",
          "group": "19S Group 10",
          "name": "Irma Langley",
          "nationality": "Belgium",
          "username": "cc9718",
          "wild": "N"
        },
        {
          "gender": "Female",
          "group": "19S Group 2",
          "name": "Philip Leblanc",
          "nationality": "Peru",
          "username": "am2219",
          "wild": "N"
        }
      ],
      [
        {
          "gender": "Female",
          "group": "19S Group 8",
          "name": "Jocelyn Mcpherson",
          "nationality": "Austria",
          "username": "smw19",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 2",
          "name": "Cruz Wall",
          "nationality": "Turkey",
          "username": "rh1819",
          "wild": "N"
        },
        {
          "gender": "Female",
          "group": "19S Group 8",
          "name": "Tyler Rosario",
          "nationality": "Indonesia",
          "username": "rgm19",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 4",
          "name": "Gabriel Alston",
          "nationality": "China",
          "username": "mjk19",
          "wild": "N"
        },
        {
          "gender": "Female",
          "group": "19S Group 3",
          "name": "Gil Sykes",
          "nationality": "Colombia",
          "username": "jr1519",
          "wild": "N"
        },
        {
          "gender": "Female",
          "group": "19S Group 2",
          "name": "Bree Duke",
          "nationality": "Vietnam",
          "username": "bts19",
          "wild": "Y"
        },
        {
          "gender": "Female",
          "group": "19S Group 5",
          "name": "Troy Anderson",
          "nationality": "Nigeria",
          "username": "ss7319",
          "wild": "N"
        }
      ]
    ],
    [
      [
        {
          "gender": "Male",
          "group": "19S Group 1",
          "name": "Aurora Rowland",
          "nationality": "France",
          "username": "oo1117",
          "wild": "N"
        },
        {
          "gender": "Female",
          "group": "19S Group 5",
          "name": "Aquila Potter",
          "nationality": "United States",
          "username": "nj719",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 9",
          "name": "Ulysses Bernard",
          "nationality": "New Zealand",
          "username": "nak19",
          "wild": "N"
        },
        {
          "gender": "Female",
          "group": "19S Group 3",
          "name": "Alika Winters",
          "nationality": "Sweden",
          "username": "mha13",
          "wild": "Y"
        }
      ]
    ],
    [
      [
        {
          "gender": "Male",
          "group": "19S Group 10",
          "name": "Amery Hernandez",
          "nationality": "India",
          "username": "fcd18",
          "wild": "Y"
        },
        {
          "gender": "Male",
          "group": "19S Group 6",
          "name": "Wade O'connor",
          "nationality": "Netherlands",
          "username": "etg19",
          "wild": "Y"
        },
        {
          "gender": "Male",
          "group": "19S Group 5",
          "name": "Reagan Mathis",
          "nationality": "Costa Rica",
          "username": "co119",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 9",
          "name": "Montana Young",
          "nationality": "United Kingdom",
          "username": "cbl19",
          "wild": "Y"
        },
        {
          "gender": "Male",
          "group": "19S Group 11",
          "name": "Samson Heath",
          "nationality": "Poland",
          "username": "am16918",
          "wild": "N"
        },
        {
          "gender": "",
          "group": "",
          "name": 26,
          "nationality": "",
          "username": ""
        },
        {
          "gender": "Female",
          "group": "19S Group 3",
          "name": "Laurel Saunders",
          "nationality": "South Korea",
          "username": "yt2619",
          "wild": "Y"
        }
      ]
    ],
    [
      [
        {
          "gender": "Male",
          "group": "19S Group 2",
          "name": "Samantha Hernandez",
          "nationality": "Mexico",
          "username": "tv419",
          "wild": "N"
        },
        {
          "gender": "Female",
          "group": "19S Group 11",
          "name": "Constance Madden",
          "nationality": "Peru",
          "username": "fong97",
          "wild": "N"
        },
        {
          "gender": "Female",
          "group": "19S Group 2",
          "name": "Kirby Ball",
          "nationality": "Belgium",
          "username": "aao519",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 8",
          "name": "Berk Caldwell",
          "nationality": "Austria",
          "username": "yz13219",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 7",
          "name": "Neil Simon",
          "nationality": "Netherlands",
          "username": "wrn119",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 6",
          "name": "Addison O'brien",
          "nationality": "Chile",
          "username": "vs1619",
          "wild": "N"
        },
        {
          "gender": "Female",
          "group": "19S Group 3",
          "name": "Katelyn Mercado",
          "nationality": "Brazil",
          "username": "sl7319",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 8",
          "name": "Quemby Anderson",
          "nationality": "Italy",
          "username": "sl5419",
          "wild": "Y"
        }
      ]
    ],
    [
      [
        {
          "gender": "Male",
          "group": "19S Group 9",
          "name": "Kenneth Waters",
          "nationality": "Colombia",
          "username": "sk2919",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 5",
          "name": "Jacqueline Buck",
          "nationality": "Indonesia",
          "username": "sa3819",
          "wild": "N"
        },
        {
          "gender": "Female",
          "group": "19S Group 6",
          "name": "Honorato Kelley",
          "nationality": "United States",
          "username": "mma919",
          "wild": "N"
        },
        {
          "gender": "Female",
          "group": "19S Group 11",
          "name": "Maia Rodgers",
          "nationality": "United Kingdom",
          "username": "koshinye",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 5",
          "name": "Knox Bass",
          "nationality": "Canada",
          "username": "jtn19",
          "wild": "N"
        }
      ]
    ],
    [
      [
        {
          "gender": "Male",
          "group": "19S Group 5",
          "name": "Dustin Humphrey",
          "nationality": "China",
          "username": "jkk19",
          "wild": "Y"
        },
        {
          "gender": "Male",
          "group": "19S Group 8",
          "name": "Richard Gaines",
          "nationality": "Germany",
          "username": "hk1919",
          "wild": "N"
        },
        {
          "gender": "Female",
          "group": "19S Group 1",
          "name": "Gisela Peters",
          "nationality": "Sweden",
          "username": "gm719",
          "wild": "N"
        },
        {
          "gender": "Female",
          "group": "19S Group 10",
          "name": "Quinn Beach",
          "nationality": "Turkey",
          "username": "bpb10",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 7",
          "name": "Levi Travis",
          "nationality": "Russian Federation",
          "username": "bo219",
          "wild": "N"
        },
        {
          "gender": "Female",
          "group": "19S Group 4",
          "name": "Kamal Bell",
          "nationality": "Vietnam",
          "username": "ajc419",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 11",
          "name": "Cara Dillard",
          "nationality": "Pakistan",
          "username": "acg07",
          "wild": "Y"
        },
        {
          "gender": "Male",
          "group": "19S Group 10",
          "name": "Florence Bradley",
          "nationality": "Spain",
          "username": "aao1519",
          "wild": "N"
        }
      ]
    ],
    [
      [
        {
          "gender": "Female",
          "group": "19S Group 10",
          "name": "Cheyenne Holden",
          "nationality": "Mexico",
          "username": "nd1119",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 8",
          "name": "Kieran Rodgers",
          "nationality": "Peru",
          "username": "nak119",
          "wild": "N"
        },
        {
          "gender": "Female",
          "group": "19S Group 7",
          "name": "Sharon Duffy",
          "nationality": "Belgium",
          "username": "gg719",
          "wild": "Y"
        }
      ]
    ],
    [
      [
        {
          "gender": "",
          "group": "",
          "name": 52,
          "nationality": "",
          "username": ""
        },
        {
          "gender": "Female",
          "group": "19S Group 1",
          "name": "Chiquita Pittman",
          "nationality": "South Korea",
          "username": "fk2818",
          "wild": "Y"
        },
        {
          "gender": "Female",
          "group": "19S Group 3",
          "name": "Kennan Morin",
          "nationality": "India",
          "username": "tp519",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 2",
          "name": "Arsenio Curry",
          "nationality": "Sweden",
          "username": "owa19",
          "wild": "Y"
        }
      ]
    ],
    [
      [
        {
          "gender": "Female",
          "group": "19S Group 4",
          "name": "Tiger Davis",
          "nationality": "Poland",
          "username": "orc19",
          "wild": "N"
        },
        {
          "gender": "Female",
          "group": "19S Group 6",
          "name": "Dora Bryan",
          "nationality": "United States",
          "username": "nr1519",
          "wild": "Y"
        },
        {
          "gender": "Female",
          "group": "19S Group 11",
          "name": "Flynn Knox",
          "nationality": "New Zealand",
          "username": "nae19",
          "wild": "N"
        },
        {
          "gender": "Female",
          "group": "19S Group 1",
          "name": "Azalia Dunlap",
          "nationality": "Netherlands",
          "username": "mr1319",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 1",
          "name": "Dennis Meadows",
          "nationality": "Nigeria",
          "username": "kkv19",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 9",
          "name": "Wynne Abbott",
          "nationality": "France",
          "username": "hw2619",
          "wild": "Y"
        },
        {
          "gender": "Female",
          "group": "19S Group 6",
          "name": "Simone Matthews",
          "nationality": "United Kingdom",
          "username": "he219",
          "wild": "N"
        }
      ]
    ],
    [
      [
        {
          "gender": "Female",
          "group": "19S Group 1",
          "name": "Adrienne Peters",
          "nationality": "Costa Rica",
          "username": "dh1818",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 9",
          "name": "Ashton Sanders",
          "nationality": "Vietnam",
          "username": "pp319",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 4",
          "name": "Omar Terrell",
          "nationality": "Indonesia",
          "username": "nft19",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 5",
          "name": "Myles Little",
          "nationality": "Turkey",
          "username": "ks2419",
          "wild": "N"
        },
        {
          "gender": "Female",
          "group": "19S Group 11",
          "name": "Zephania Patrick",
          "nationality": "Austria",
          "username": "hl2019",
          "wild": "Y"
        },
        {
          "gender": "Male",
          "group": "19S Group 11",
          "name": "Griffin Orr",
          "nationality": "Colombia",
          "username": "er19",
          "wild": "Y"
        },
        {
          "gender": "Male",
          "group": "19S Group 3",
          "name": "Gisela Eaton",
          "nationality": "China",
          "username": "awl2518",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 7",
          "name": "Ian Price",
          "nationality": "Belgium",
          "username": "sf1419",
          "wild": "N"
        }
      ]
    ],
    [
      [
        {
          "gender": "Female",
          "group": "19S Group 6",
          "name": "Noelle Slater",
          "nationality": "South Korea",
          "username": "rme19",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 4",
          "name": "Julie Lindsey",
          "nationality": "Mexico",
          "username": "pd219",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 9",
          "name": "Teegan Valenzuela",
          "nationality": "Peru",
          "username": "jml219",
          "wild": "N"
        },
        {
          "gender": "Female",
          "group": "19S Group 10",
          "name": "Inga Osborne",
          "nationality": "Sweden",
          "username": "sai19",
          "wild": "N"
        },
        {
          "gender": "Female",
          "group": "19S Group 7",
          "name": "Petra Schroeder",
          "nationality": "Netherlands",
          "username": "ima00",
          "wild": "Y"
        },
        {
          "gender": "Male",
          "group": "19S Group 4",
          "name": "Xanthus Young",
          "nationality": "United Kingdom",
          "username": "dd619",
          "wild": "N"
        },
        {
          "gender": "Male",
          "group": "19S Group 4",
          "name": "Brendan Dalton",
          "nationality": "United States",
          "username": "aim109",
          "wild": "Y"
        }
      ]
    ]
  ],
  "status": "success"
})
    # print(get_blanks("1,"))
    # print(main('c1234-2', 'LTUG', 'seat', 'Brianna Morrison-1,Gisela Peters-3,'))
    # client = MongoClient(
    #     "mongodb+srv://admin:ZpwHfTeZDM2ACkBM@cluster0.vqrib.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    # db = client.myFirstDatabase
    # generate_seat_numbers('c1234-2', 'LT3', db)
    # print(get_reqs('aayush-1,nandhu-2'))
    print()
