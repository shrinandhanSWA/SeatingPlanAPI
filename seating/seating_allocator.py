import random

import itertools
import collections

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


def sort_people(people, factors):
    once = False
    optimal = people
    random.shuffle(people)

    if 'group' in factors:
        people.sort(key=lambda student: student.get_group())
        return people

    if 'wild' in factors:
        optimal = evenly_spaced(group_by(people, 'wild'))
        once = True

    if 'nationality' in factors:
        if once:
            # special function to distribute again
            out = []

            # get size of people, and split into 20
            size = len(people)
            divs = size // 20

            for i in range(divs):
                # partition this shard
                this_shard = optimal[i * 20: (i + 1) * 20]

                # sort this shard
                optimal_shard = evenly_spaced(group_by(this_shard, 'nationality'))

                # add shard in order back to out
                out.extend(optimal_shard)

            # deal with remaining people(rem)
            this_shard = people[divs * 20:]

            # sort this shard
            optimal_shard = evenly_spaced(group_by(this_shard, 'nationality'))

            # add shard in order back to out
            out.extend(optimal_shard)

            return out
        else:
            optimal = evenly_spaced(group_by(people, 'nationality'))
            once = True

    if 'gender' in factors:
        if once:
            # special function to distribute again
            out = []

            # get size of people, and split into 20
            size = len(people)
            divs = size // 20

            for i in range(divs):
                # partition this shard
                this_shard = optimal[i * 20: (i + 1) * 20]

                # sort this shard
                optimal_shard = evenly_spaced(group_by(this_shard, 'gender'))

                # add shard in order back to out
                out.extend(optimal_shard)

            # deal with remaining people(rem)
            this_shard = people[divs * 20:]

            # sort this shard
            optimal_shard = evenly_spaced(group_by(this_shard, 'gender'))

            # add shard in order back to out
            out.extend(optimal_shard)

            return out
        else:
            optimal = evenly_spaced(group_by(people, 'gender'))
            once = True

    return optimal
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


def evaluate_ordering(people, radius=1):
    n = len(people)
    global_avg_predicted_grade = sum(map(lambda p: p.get_predicted_grade(), people)) / n

    global_gender_ratio = len(list(filter(lambda p: p.is_male(), people))) / n
    # print('global_gender_ratio', global_gender_ratio)
    nationalities = collections.Counter(map(lambda p: p.get_predicted_grade(), people))
    global_nationality_ratios = {k: v / n for k, v in nationalities.items()}

    groups = collections.Counter(map(lambda p: p.get_group_name(), people))
    avg_group_size = sum(groups.values()) / len(groups)

    total_score = 0

    for i in range(radius, len(people) - radius):
        section = people[i - radius: i + radius + 1]
        total_score += evaluate_section(section, global_avg_predicted_grade,
                                        global_nationality_ratios, global_gender_ratio,
                                        avg_group_size)

    return 100 + total_score


def evaluate_section(section, global_avg_predicted_grade,
                     global_nationality_ratios, global_gender_ratio,
                     avg_group_size):
    n = len(section)
    score = 0
    avg_predicted_grade = sum(map(lambda p: p.get_predicted_grade(), section)) / n
    score -= (avg_predicted_grade - global_avg_predicted_grade) ** 2

    gender_ratio = len(list(filter(lambda p: p.is_male(), section))) / n
    # print(gender_ratio)
    score -= (global_gender_ratio - gender_ratio) ** 2
    #
    nationalities = collections.Counter(map(lambda p: p.get_predicted_grade(), section))
    nationality_ratios = {k: v / n for k, v in nationalities.items()}
    score -= sum(map(lambda nat: (nationality_ratios[nat] - global_nationality_ratios[nat]) ** 2,
                     nationalities.keys()))
    #
    # groups = collections.Counter(map(lambda p: p.get_group_name(), section))
    # score += max(groups.values()) / n

    return score


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
        for [username, name, group, disability, gender, nationality, wc_acc, wc_py] \
                in rows:

            first_name = name.split(' ')[0]
            last_name = name.split(' ')[0]
            students.append(Student(first_name, last_name, username, gender=gender,
                                    nationality=nationality, disability_exception=disability != '',
                                    wildcard_accountant=wc_acc, wildcard_python=wc_py,
                                    group_name=group))

    return students


if __name__ == "__main__":
    from student import Student
    students = load_sample_data()
    # print(students)
    students1 = [Student('A1', 'A2', 'A', 'Female'),
                Student('B1', 'A2', 'B', 'Male'),
                Student('C1', 'A2', 'C', 'Female'),
                Student('D1', 'A2', 'D', 'Male')]
    #
    for radius in range(1, 10):
        print(f'radius={radius}')
        for factor in 'random', 'gender', 'predicted_grade', 'nationality':
            # print(factor)
            people = sort_people(students, factors=[factor])
            # if factor != 'random':
            #     print(list(map(lambda p: getattr(p, factor), people)))
            # print('sorted', people)
            print(f'{factor} = {evaluate_ordering(people.copy())}')

        print('=' * 10)
    students = load_sample_data('sample_data.csv')
