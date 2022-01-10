import timeit
from main import main


def benchmark_main():
    repeats = 10
    time = timeit.timeit(lambda: main('c1234-2', 'LTUG', 'wild,nationality,',
                                      'Gisela Peters-3,', '1,'), number=repeats)
    return time / repeats


if __name__ == '__main__':
    print(benchmark_main())