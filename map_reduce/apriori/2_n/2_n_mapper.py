#!/usr/bin/env python
import itertools

__author__ = 'Daniil Nikulin'
__license__ = "Apache License 2.0"
__email__ = "danil.nikulin@gmail.com"
__date__ = "2019-10-06"
__app__ = "hadoop_spark_perf"
__status__ = "Development"

import sys

ONE_ITEM_FREQUENCY_RESULT_PATH = "/user/hadoop/output/part-r-00000"
N_DIM = 2


def get_2n_items_list(file_path):
    items = set()
    with open(file_path) as inf:
        for line in inf:
            parts = line.split('\t')
            if len(parts) > 1:
                items.add(parts[0])
    items_combinations = itertools.combinations(items, N_DIM)

    return list(items_combinations)


def count_usage_of_2n_items():
    # [('a', 'b'), ('a', 'c'), ('b', 'c')]
    # a,b,d
    # b,c,c
    # b,a
    # c,a
    n2_candidates = get_2n_items_list(ONE_ITEM_FREQUENCY_RESULT_PATH)
    for line in sys.stdin:
        items = line.rstrip("\n").rsplit(",")
        for candidate_items in n2_candidates:
            if set(candidate_items).issubset(set(items)):
                print("{el1},{el2}\t{count}".format(el1=candidate_items[0], el2=candidate_items[0], count=1))


if __name__ == "__main__":
    count_usage_of_2n_items()
