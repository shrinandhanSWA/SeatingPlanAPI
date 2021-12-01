import random

import itertools
import collections

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


def allocate_seats(layout, people, factors, total_seats):
    """
    Sets random occupant for available seats
    :param people: list of people
    :return: list of people that could not be allocated seats
    """
    people = sort_people(people, factors)
    n = len(people)
    rem = max(0, (total_seats - n))

    for _ in range(rem):
        people.append(dummy_student())

    people = evenly_spaced(group_by(people, 'real'))
    remaining = people

    for subsection in layout.get_subsections():

        remaining = subsection.allocate_seats(remaining)

        if not remaining:
            break

    return remaining


def fitness(people):
    score = 0
    for i in range(1, len(people) - 1):
        pass
    return 0


def load_sample_data():
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
    from student import Student, dummy_student

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