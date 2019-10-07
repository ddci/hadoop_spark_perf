#!/usr/bin/env python
__author__ = 'Daniil Nikulin'
__license__ = "Apache License 2.0"
__email__ = "danil.nikulin@gmail.com"
__date__ = "2019-10-06"
__app__ = "hadoop_spark_perf"
__status__ = "Development"

import sys


def do_reduce(word, _values):
    return word, sum(_values)


prev_key = None
values = []

for line in sys.stdin:
    key, value = line.split("\t")
    if key != prev_key and prev_key is not None:
        result_key, result_value = do_reduce(prev_key, values)
        if result_value > 1000:
            print(result_key + "\t" + str(result_value))
        values = []
    prev_key = key
    values.append(int(value))

if prev_key is not None:
    result_key, result_value = do_reduce(prev_key, values)
    if result_value > 1000:
        print(result_key + "\t" + str(result_value))
