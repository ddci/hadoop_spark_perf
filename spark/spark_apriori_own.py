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

file = "/Users/danielnikulin/Projects/MasterProject/hadoop_spark_perf/dataset/LARGE_DAT.csv"
conf = SparkConf().set('spark.master', 'local[*]') \
    .setAppName("Му Арр") \
    .set("spark.executor.memory", "2g") \
    .set("spark.driver.memory", "2g") \
    .set('spark.executor.pyspark.memory', '2g')\
    .set('spark.executor.extraJavaOptions', '-XX:+UseCompressedOops')\
    .set('spark.rdd.compress', True)\
    .set('spark.serializer', 'org.apache.spark.serializer.KryoSerializer')\
    .set('spark.driver.maxResultSize', '24m')\
    .set('spark.memory.fraction', 0.9)\
    .set('spark.driver.maxResultSize', '100m')


sc = SparkContext(conf=conf)
transactions = sc.textFile(file)

now = datetime.datetime.now()
print(now)
trx_count = transactions.count()
print(trx_count)
#0.0002118997384
print()
minSupport = 0.000211899738 * trx_count
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


l2 = transaction_items.flatMap(n2)
print(l2.take(50))
l2 = l2.reduceByKey(add)

l2 = l2.filter(lambda i: int(i[1]) > minSupport)
print(l2.collect())
now = datetime.datetime.now()
print(now)
