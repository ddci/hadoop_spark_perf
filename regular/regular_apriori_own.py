import datetime
import itertools
from collections import defaultdict

now = datetime.datetime.now()

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


def main(**kwargs):
    """
    Executes Apriori algorithm and print its result.
    """
    with open('/Users/danielnikulin/Projects/MasterProject/hadoop_spark_perf/dataset/LARGE_DAT.csv') as f:
        count = sum(1 for _ in f)

    support = 0.0002118997384

    print(count)
    transaction_generator = data_from_csv(
        '/Users/danielnikulin/Projects/MasterProject/hadoop_spark_perf/dataset/LARGE_DAT.csv')
    frequent_items_n1 = defaultdict(int)

    for transaction in transaction_generator:
        for item in transaction:
            frequent_items_n1[item] += 1
    frequent_items_n1 = {k for k, v in frequent_items_n1.items() if v / count > support}
    print(frequent_items_n1)
    transaction_generator = data_from_csv(
         '/Users/danielnikulin/Projects/MasterProject/hadoop_spark_perf/dataset/LARGE_DAT.csv')

    frequent_items_n2 = defaultdict(int)
    for transaction in transaction_generator:
        exist_in_items = set()
        for item in transaction:
            if item in frequent_items_n1:
                exist_in_items.add(item)
        for combination in itertools.combinations(exist_in_items, 2):
            frequent_items_n2[tuple(sorted(combination))] += 1

    frequent_items_n2 = {k:v for k, v in frequent_items_n2.items() if v / count > support}
    print(frequent_items_n2)


if __name__ == '__main__':
    print("Current date and time : ")
    print(now.strftime("%Y-%m-%d %H:%M:%S"))

    main()
    import datetime

    now = datetime.datetime.now()
    print("Current date and time : ")
    print(now.strftime("%Y-%m-%d %H:%M:%S"))
