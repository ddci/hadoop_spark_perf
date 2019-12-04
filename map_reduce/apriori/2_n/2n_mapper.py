#!/usr/bin/env python
import itertools
import sys

sys.path.append('.')
N_DIM = 2


def get_2n_items():
    items = set()
    with open("part-00000") as inf:
        for line in inf:
            parts = line.split('\t')
            if len(parts) > 1:
                items.add(parts[0])

    return items


def count_usage_of_2n_items():
    all_items_set = get_2n_items()
    for line in sys.stdin:
        items = line.rstrip("\n").rsplit(",")  # 74743 43355 53554
        exist_in_items = set()
        for item in items:
            if item in all_items_set:
                exist_in_items.add(item)
        for combination in itertools.combinations(exist_in_items, N_DIM):
            combination = sorted(combination)
            print("{el1},{el2}\t{count}".format(el1=combination[0], el2=combination[1], count=1))


if __name__ == "__main__":
    count_usage_of_2n_items()


# MEMORY ERROR
# def count_usage_of_2n_items():
#     all_items_set = get_2n_items()
#     all_items = list(itertools.combinations(all_items_set, N_DIM))
#     for line in sys.stdin:
#         items = line.rstrip("\n").rsplit(",")
#         for candidate_items in all_items:
#             if set(candidate_items).issubset(set(items)):
#                 print("{el1},{el2}\t{count}".format(el1=candidate_items[0], el2=candidate_items[1], count=1))
