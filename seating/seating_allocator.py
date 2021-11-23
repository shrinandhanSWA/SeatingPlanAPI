import random

import itertools
import collections


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
    random.shuffle(people)
    if 'random' in factors:
        optimal_random = people
        return optimal_random

    if 'gender' in factors:
        groups = group_by(people, 'gender')
        optimal_gender = evenly_spaced(groups)
        return optimal_gender

    if 'nationality' in factors:
        optimal_nationality = evenly_spaced(group_by(people, 'nationality'))
        return optimal_nationality

    if 'predicted_grade' in factors:
        optimal_grades = evenly_spaced(group_by(people, 'predicted_grade'))
        return optimal_grades

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