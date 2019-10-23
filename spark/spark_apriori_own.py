import itertools
import logging
import os
from operator import add

os.environ['HADOOP_USER_NAME'] = 'admin'


def suppress_py4j_logging():
    logger = logging.getLogger('py4j')
    logger.setLevel(logging.WARN)


from pyspark import SparkConf, SparkContext
import datetime

conf = SparkConf().setMaster("local").setAppName("Му Арр")
sc = SparkContext(conf=conf)
transactions = sc.textFile("/Users/danielnikulin/Projects/MasterProject/hadoop_spark_perf/dataset/DAT.csv")

now = datetime.datetime.now()
print(now)
minSupport = 0.0002118997384 * transactions.count()
transaction_items = transactions.map(lambda line: line.split(","))
transaction_items.cache()


def n1(items):
    array = list()
    for item in items:
        array.append((item, 1))
    return array


l1 = transaction_items.flatMap(n1).reduceByKey(add)
print(l1.collect())

print(transaction_items.take(5))
l1 = l1.filter(lambda i: int(i[1]) > minSupport)
print(l1.collect())
print(l1.count())

# cart = l1.cartesian(l1).cache()
# # sc.broadcast(cart)
internal_l1 = l1.collect()
# sc.broadcast(internal_l1)
internal_l1set = {x[0] for x in internal_l1}
sc.broadcast(internal_l1set)


def n2(items):
    exist_in_items = set()
    array = list()
    for item in items:
        if item in internal_l1set:
            exist_in_items.add(item)
    for combination in itertools.combinations(exist_in_items, 2):
        array.append((tuple(sorted(combination)), 1))
    return array


l2 = transaction_items.flatMap(n2).reduceByKey(add)
print(l2.take(20))
l2 = l2.filter(lambda i: int(i[1]) > minSupport)
print(l2.collect())
print(l2.count())
now = datetime.datetime.now()
print(now)
