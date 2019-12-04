import itertools
import logging
import os
from operator import add

os.environ['HADOOP_USER_NAME'] = 'admin'


# cart = l1.cartesian(l1).cache()
# # sc.broadcast(cart)
# sc.broadcast(internal_l1)


def suppress_py4j_logging():
    logger = logging.getLogger('py4j')
    logger.setLevel(logging.WARN)


from pyspark import SparkConf, SparkContext
import datetime
# conf = SparkConf().set('spark.master', 'local[*]') \
file = "/Users/danielnikulin/Projects/MasterProject/hadoop_spark_perf/dataset/LARGE_DAT.csv"
conf = SparkConf().set('spark.master', 'yarn') \
    .setAppName("Му Арр") \
    .set("spark.executor.memory", "512m") \
    .set("spark.driver.memory", "512m") \
    .set('spark.executor.pyspark.memory', '512m')\
    .set('spark.executor.extraJavaOptions', '-XX:+UseCompressedOops')\
    .set('spark.rdd.compress', True)\
    .set('spark.serializer', 'org.apache.spark.serializer.KryoSerializer')\
    .set('spark.driver.maxResultSize', '24m')\
    .set('spark.driver.maxResultSize', '100m')\
    .set('spark.memory.fraction', 0.9)

sc = SparkContext(conf=conf)
transactions = sc.textFile(file)

now = datetime.datetime.now()
print(now)
trx_count = transactions.count()
print(trx_count)
#0.0002118997384
print()
minSupport = 0.0002118997384 * trx_count
print(minSupport)
transaction_items = transactions.map(lambda line: line.split(","))
transaction_items.cache()


def n1(items):
    array = list()
    for item in items:
        array.append((item, 1))
    return array


l1 = transaction_items.flatMap(n1).reduceByKey(add)
l1 = l1.filter(lambda i: int(i[1]) > minSupport)
print(l1.take(10))


internal_l1 = l1.collect()

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


l2 = transaction_items.flatMap(n2)
print(l2.take(50))
l2 = l2.reduceByKey(add)

l2 = l2.filter(lambda i: int(i[1]) > minSupport)
print(l2.collect())
now = datetime.datetime.now()
print(now)
