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

    if 'wild' in factors:
        # print(orderings)
        orderings = list(map(lambda optimal: evenly_spaced(group_by(
            optimal, 'wild')), orderings))
        # print(orderings)

    epochs = 20
    mu = 2
    lambda_ = 10

    return evolution_strategy(orderings, epochs, mu, lambda_)


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
    """
    Calculate the fitness of ordering of list
    :param people: list of Student objects
    :return: int
    """
    score = 0
    for i in range(1, len(people) - 1):
        # Scan over every window of 3 students
        left, curr, right = people[i - 1], people[i], people[i + 1]

        g1, g2, g3 = left.get_gender(), curr.get_gender(), right.get_gender()
        # If student of left is same gender
        if g1 == g2:
            score += 1

        if g2 == g3:
            score += 1

        # if all have the same gender
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
    """
    Mutate list by swapping students at randomly chosen indices
    :param people: list of students
    :return: list of students
    """
    # Swap 10% of indices
    ratio = 0.1
    swaps = int(ratio * len(people))
    n = len(people)

    for _ in range(swaps):
        first = True
        # Only swap if neither are wildcards or both are wildcards
        while (first or
               (people[i].is_wildcard() and not people[j].is_wildcard()
                or not people[i].is_wildcard() and people[j].is_wildcard())):
            i = random.randint(0, n - 1)
            j = random.randint(0, n - 1)
            first = False

        people[i], people[j] = people[j], people[i]

    return people


def evolution_strategy(orderings, epoch, mu, lambda_):
    """

    :param orderings: list of students
    :param epoch: number of iterations of algorithm
    :param mu: number of fittest parents to be chosen from each generation
    :param lambda_: number of children to generate from mu parents
    :return:
    """
    max_fitness_count = 0
    count_threshold = 3
    prev_max_fitness = 0

    for i in range(epoch):
        # Sort based on fitness
        orderings.sort(key=lambda people: fitness(people))

        curr_max_fitness = fitness(orderings[-1])
        if curr_max_fitness == prev_max_fitness:
            max_fitness_count += 1
            # If the fitness has stopped increasing then stop iterations
            if max_fitness_count == count_threshold:
                break

        elif curr_max_fitness > prev_max_fitness:
            # If new max fitness is greater than previous max then reset count
            prev_max_fitness = curr_max_fitness
            max_fitness_count = 1

        # Select mu fittest parents
        parents = orderings[-mu:]

        children = []
        for _ in range(lambda_):
            index = random.randint(0, len(parents) - 1)
            # Mutate random parent to create new child
            children.append(mutate(parents[index].copy()))

        # New population is combination of parents and children
        orderings = parents + children
        # print(f'''epoch {i}: fitness={max(map(lambda people: fitness(people),
        #                                       orderings))}''')

    return max(orderings, key=lambda people: fitness(people))


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

    for factors in ['group'], ['gender'], ['nationality'], ['gender',
                                                            'nationality'], \
                   ['gender',
                    'nationality',
                    'wild']:
        optimal = sort_people(students, factors=factors)
        print(f'{factors} = {fitness(optimal)}')
        print('=' * 10)
