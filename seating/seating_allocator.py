import random


def sort_people(people, factors):
    if 'random' in factors:
        random.shuffle(people)

    if 'nationality' in factors:
        people.sort(key=lambda student: student.get_nationality())

    if 'predicted_grade' in factors:
        people.sort(key=lambda student: student.get_predicted_grade())
        mid = len(people) // 2
        left = people[:mid]
        right = people[mid:]
        people[::2] = left
        people[1::2] = right

    return people


def allocate_seats(layout, people, factors=['random']):
    """
    Sets random occupant for available seats
    :param people: list of people
    :return: list of people that could not be allocated seats
    """
    people = sort_people(people, factors)
    remaining = people

    for subsection in layout.get_subsections():

        remaining = subsection.allocate_seats(remaining)

        if not remaining:
            break

    return remaining
