import random
import itertools
from seating.student import Student, dummy_student


def group_by(xs, attr):
    """
    Groups objects in the list with same value for an attribute
    :param xs: list of objects
    :param attr: string of name of attribute
    :return: list of list of objects
    """
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
    random.shuffle(optimal)

    if 'random' in factors:
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

    # wildcards with special expertise need to be evenly placed around the
    # lecture theatre
    if 'wild' in factors:
        orderings = list(map(lambda optimal: evenly_spaced(group_by(
            optimal, 'wild')), orderings))

    epochs = 100
    mu = 2
    lambda_ = 5 * mu

    return evolution_strategy(orderings, epochs, mu, lambda_, factors)


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


def fitness(people, factors):
    """
    Calculate the fitness of ordering of list
    :param people: list of Student objects
    :return: int
    """

    def window_score(v1, v2, v3):
        score = 0
        if v1 == v2:
            score += 1

        if v2 == v3:
            score += 1

        # if all have the same gender
        if v1 == v2 == v3:
            score -= 2

        return score

    score = 0
    for i in range(1, len(people) - 1):
        # Scan over every window of 3 students
        left, curr, right = people[i - 1], people[i], people[i + 1]
        if 'gender' in factors:
            g1 = left.get_gender()
            g2 = curr.get_gender()
            g3 = right.get_gender()
            score += window_score(g1, g2, g3)

        if 'nationality' in factors:
            n1 = left.get_nationality()
            n2 = curr.get_nationality()
            n3 = right.get_nationality()
            score += window_score(n1, n2, n3)

    return score


def valid_swap(people, i, j, factors):
    if 'wild' in factors:
        return people[i].is_wildcard() == people[j].is_wildcard()
    return True


def mutate(people, swap_rate, factors):
    """
    Mutate list by swapping students at randomly chosen indices
    :param swap_rate: percentage of seats to swap
    :param people: list of students
    :return: list of students
    """
    swaps = int(swap_rate * len(people))
    n = len(people)
    i = j = 0
    for _ in range(swaps):
        first = True
        # Only swap if neither are wildcards or both are wildcards
        while first or not valid_swap(people, i, j, factors):
            i = random.randint(0, n - 1)
            j = random.randint(0, n - 1)
            first = False

        people[i], people[j] = people[j], people[i]

    return people


def evolution_strategy(orderings, epoch, mu, lambda_, factors):
    """

    :param orderings: list of students
    :param epoch: number of iterations of algorithm
    :param mu: number of fittest parents to be chosen from each generation
    :param lambda_: number of children to generate from mu parents
    :return:
    """
    swap_rate = 0.5
    min_swap_rate = 0.1
    decay_rate = 0.95

    orderings = initialise_population(factors, lambda_, mu, orderings,
                                      swap_rate)

    for i in range(epoch):
        # Sort based on fitness
        orderings.sort(key=lambda people: fitness(people, factors))
        # Select mu fittest parents
        parents = orderings[-mu:]

        children = []
        for _ in range(lambda_):
            index = random.randint(0, len(parents) - 1)
            # Mutate random parent to create new child
            children.append(mutate(parents[index].copy(), swap_rate, factors))

        # New population is combination of parents and children
        orderings = parents + children
        swap_rate = max(decay_rate * swap_rate, min_swap_rate)

    return max(orderings, key=lambda people: fitness(people, factors))


def initialise_population(factors, lambda_, mu, orderings, swap_rate):
    children = []
    for _ in range(len(orderings) - (mu + lambda_)):
        index = random.randint(0, len(orderings) - 1)
        # Mutate random parent to create new child
        children.append(mutate(orderings[index].copy(), swap_rate, factors))
    orderings += children
    return orderings


def load_sample_data(file):
    """
    Load student data from file
    :param file: CSV file path
    :return: list of students
    """
    import csv
    students = []
    with open(file) as sample_data:
        rows = csv.reader(sample_data)
        next(rows)
        for [username, name, group, disability, gender, nationality, wc_acc,
             wc_py] \
                in rows:
            students.append(
                Student(name, username, gender, nationality, group,
                        disability=disability != '',
                        wild=wc_acc == 'Y' or wc_py == 'Y'))

    return students


if __name__ == "__main__":
    students = load_sample_data('sample_data.csv')

    factors = ['gender', 'nationality', 'wild']
    optimal = sort_people(students, factors=factors)
    print(f'{factors} = {fitness(optimal, factors)}')
    print('=' * 10)
