import random
import itertools
from seating.student import Student, dummy_student


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
    optimal = people.copy()

    if 'random' in factors:
        optimal = people.copy()
        random.shuffle(optimal)
        factors.remove('random')

    if not factors:
        return optimal

    if 'group' in factors:
        optimal.sort(key=lambda student: student.get_group())
        return optimal

    orderings = []
    if 'nationality' in factors:
        orderings.append(evenly_spaced(group_by(people, 'nationality')))

    if 'gender' in factors:
        orderings.append(evenly_spaced(group_by(people, 'gender')))

    epochs = 10
    mu = 5
    lambda_ = 5
    optimal = evolution_strategy(orderings, epochs, mu, lambda_)

    if 'wild' in factors:
        wildcards = list(filter(lambda person: person.is_wildcard(), optimal))
        for wc in wildcards:
            optimal.remove(wc)

        optimal = evenly_spaced([optimal, wildcards])

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
        left, curr, right = people[i - 1], people[i], people[i + 1]

        g1, g2, g3 = left.get_gender(), curr.get_gender(), right.get_gender()
        if g1 == g2:
            score += 1

        if g2 == g3:
            score += 1

        if g1 == g2 == g3:
            score -= 2

        n1 = left.get_nationality()
        n2 = curr.get_nationality()
        n3 = right.get_nationality()

        if n1 == n2:
            score += 1

        if n2 == n3:
            score += 1

        if n1 == n2 == n3:
            score -= 2

    return score


def mutate(people):
    ratio = random.random()
    swaps = int(ratio * len(people))
    n = len(people)
    for _ in range(swaps):
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        people[i], people[j] = people[j], people[i]

    return people


def evolution_strategy(orderings, epoch, mu, lambda_):
    for i in range(epoch):
        orderings.sort(key=lambda people: fitness(people))
        parents = orderings[-mu:]
        children = []
        for _ in range(lambda_):
            index = random.randint(0, len(parents) - 1)
            children.append(mutate(parents[index].copy()))

        orderings = parents + children
        # print(f'''epoch {i}: fitness={max(map(lambda people: fitness(people),
        #                                       orderings))}''')

    return max(orderings, key=lambda people: fitness(people))


def load_sample_data():
    import csv
    students = []
    with open('sample_data.csv') as sample_data:
        rows = csv.reader(sample_data)
        next(rows)
        for [username, name, group, disability, gender, nationality, wc_acc,
             wc_py] \
                in rows:
            students.append(
                Student(name, username, gender, nationality, group,
                        disability=disability != '',
                        wildcard=wc_acc == 'Y' or wc_py == 'Y'))

    return students


if __name__ == "__main__":
    students = load_sample_data()

    for factors in ['group'], ['gender'], ['nationality'], ['gender',
                                                            'nationality'], \
                   ['gender',
                    'nationality',
                    'wild']:
        optimal = sort_people(students, factors=factors)
        print(f'{factors} = {fitness(optimal)}')
        print('=' * 10)
