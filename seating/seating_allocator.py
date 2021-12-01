import random
import itertools
from .student import dummy_student


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
                optimal_shard = evenly_spaced(
                    group_by(this_shard, 'nationality'))

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

    if 'wild' in factors:
        optimal = evenly_spaced(group_by(people, 'wild'))

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
        print(f'''epoch {i}: fitness={max(map(lambda people: fitness(people),
                                              orderings))}''')

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
    from student import Student, dummy_student

    students = load_sample_data()
    orderings = []
    for factor in 'random', 'gender', 'nationality':
        people = sort_people(students, factors=[factor])
        orderings.append(people.copy())
        print(f'{factor} = {fitness(people.copy())}')

    epoch, mu, lambda_ = 5, 3, 5
    optimal = evolution_strategy(orderings, epoch, mu, lambda_)
