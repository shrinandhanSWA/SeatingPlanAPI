import random
import itertools

from seating.seating_arrangement import SeatingArrangement
from seating.student import Student, DummyStudent
from seating.factors import GENDER, NATIONALITY, GROUP, WILD, RANDOM

from seating.student import Student


def group_by(xs, attr):
    xs = sorted(xs, key=lambda x: getattr(x, attr))
    groups = itertools.groupby(xs, lambda x: getattr(x, attr))
    return [[item for item in data] for (key, data) in groups]


def evenly_spaced(iterables):
    """
    >> evenly_spaced(range(10), list('abc'))
    [0, 1, 'a', 2, 3, 4, 'b', 5, 6, 7, 'c', 8, 9]
    """
    if len(iterables) == 1:
        return iterables[0]

    return [item[1] for item in
            sorted(itertools.chain.from_iterable(
                zip(itertools.count(start=1.0 / (len(seq) + 1),
                                    step=1.0 / (len(seq) + 1)), seq)
                for seq in iterables))]


def sort_students(students, factors, evolution_strategy, reserved_names):
    optimal = students.copy()
    random.shuffle(optimal)

    if RANDOM in factors:
        factors.remove(RANDOM)

    if not factors:
        return optimal

    if GROUP in factors:
        optimal.sort(key=lambda student: student.get_group())
        return optimal

    seating_arrangements = []
    if NATIONALITY in factors:
        seating_arrangements.append(evenly_spaced(group_by(students, NATIONALITY)))

    if GENDER in factors:
        seating_arrangements.append(evenly_spaced(group_by(students, GENDER)))

    # wildcards with special expertise need to be evenly placed around the
    # lecture theatre
    if WILD in factors:
        seating_arrangements = list(map(lambda optimal: evenly_spaced(group_by(
            optimal, WILD)), seating_arrangements))

    seating_arrangements = list(map(lambda students: SeatingArrangement(
        students, factors), seating_arrangements))

    return evolution_strategy.run(seating_arrangements).get_students()


def allocate_seats(layout, people, factors, total_seats, evolution_strategy,
                   reserved_names):
    """
    Sets random occupant for available seats
    :param people: list of students
    :return: list of students that could not be allocated seats
    """
    people = sort_students(people, factors, evolution_strategy, reserved_names)
    n = len(people)
    rem = max(0, (total_seats - n))
    for _ in range(rem):
        people.append(DummyStudent())

    people = evenly_spaced(group_by(people, 'real'))
    remaining = people

    for subsection in layout.get_subsections():

        remaining = subsection.allocate_seats(remaining)

        if not remaining:
            break

    return remaining

def load_sample_data(file):
    """
    Load student data from file
    :param file: CSV file path
    :return: list of students
    """
    import csv
    students = []
    with open('sample_data.csv') as sample_data:
        rows = csv.reader(sample_data)
        next(rows)
        for [username, name, group, disability, gender, nationality, wc_acc,
             wc_py] in rows:

            students.append(Student(name, username, gender,
                                    nationality, group,
                                    disability=disability != '',
                                    wild=wc_py or wc_acc))

    return students


if __name__ == "__main__":
    from student import Student
    students = load_sample_data()
    # print(students)
    students1 = [Student('A1', 'A2', 'A', 'Female'),
                Student('B1', 'A2', 'B', 'Male'),
                Student('C1', 'A2', 'C', 'Female'),
                Student('D1', 'A2', 'D', 'Male')]
    students = load_sample_data('sample_data.csv')
