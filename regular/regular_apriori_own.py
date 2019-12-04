import argparse
import datetime
import itertools
import sys
from collections import defaultdict

end = datetime.datetime.now()

__author__ = 'Daniil Nikulin'
__license__ = "Apache License 2.0"
__email__ = "danil.nikulin@gmail.com"
__date__ = "23.10.2019"
__app__ = "hadoop_spark_perf"
__status__ = "Development"


def data_from_csv(filename):
    f = open(filename)
    for l in f:
        row = list(map(str.strip, l.split(',')))
        yield row


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input',
        help='Input transaction file (default: stdin).',
        type=str)
    parser.add_argument(
        '-s', '--min-support', metavar='float',
        help='Minimum support ratio (must be > 0, default: 0.1).',
        type=float, default=0.1)
    args = parser.parse_args(argv)
    return args


def main():
    """
    Executes Apriori algorithm and print its result.
    """
    args = parse_args(sys.argv[1:])
    file_path = args.input
    with open(file_path) as f:
        count = sum(1 for _ in f)
    print(count)
    support = count * args.min_support
    print(support)
    transaction_generator = data_from_csv(file_path)
    frequent_items_n1 = defaultdict(int)

    for transaction in transaction_generator:
        for item in transaction:
            frequent_items_n1[item] += 1
    # print(frequent_items_n1)
    frequent_items_n1 = {k: v for k, v in frequent_items_n1.items() if v > support}

    transaction_generator = data_from_csv(file_path)

    frequent_items_n2 = defaultdict(int)
    for transaction in transaction_generator:
        exist_in_items = set()
        for item in transaction:
            if item in frequent_items_n1:
                exist_in_items.add(item)
        for combination in itertools.combinations(exist_in_items, 2):
            frequent_items_n2[tuple(sorted(combination))] += 1

    frequent_items_n2 = {k for k, v in frequent_items_n2.items() if v > support}
    # print(frequent_items_n2)
    frequent_items_n2_set = set()
    for k in frequent_items_n2:
        f_item, s_item = k
        frequent_items_n2_set.add(f_item)
        frequent_items_n2_set.add(s_item)

    transaction_generator = data_from_csv(file_path)

    frequent_items_n3 = defaultdict(int)
    for transaction in transaction_generator:
        exist_in_items = set()
        for item in transaction:
            if item in frequent_items_n2_set:
                exist_in_items.add(item)
        for combination in itertools.combinations(exist_in_items, 3):
            frequent_items_n3[tuple(sorted(combination))] += 1
    frequent_items_n3 = {k: v for k, v in frequent_items_n3.items() if v > support}
    # print(frequent_items_n3)


if __name__ == '__main__':
    start = datetime.datetime.now()
    main()
    end = datetime.datetime.now()
    print("Start date and time : ")
    print(start.strftime("%Y-%m-%d %H:%M:%S"))
    print("End date and time : ")
    print(end.strftime("%Y-%m-%d %H:%M:%S"))
