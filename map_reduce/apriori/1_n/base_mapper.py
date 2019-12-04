#!/usr/bin/env python
__author__ = 'Daniil Nikulin'
__license__ = "Apache License 2.0"
__email__ = "danil.nikulin@gmail.com"
__date__ = "2019-10-06"
__app__ = "hadoop_spark_perf"
__status__ = "Development"

import sys


def count_usage():
    for line in sys.stdin:
        elements = line.rstrip("\n").rsplit(",")
        for item in elements:
            print("{item}\t{count}".format(item=item, count=1))


if __name__ == "__main__":
    count_usage()
