import itertools
import sys
from operator import add

from pyspark import SparkConf, SparkContext


def n1(items):
    array = list()
    for item in items:
        array.append((item, 1))
    return array


def n2(items):
    exist_in_items = set()
    array = list()
    for item in items:
        if item in internal_l1set:
            exist_in_items.add(item)
    for combination in itertools.combinations(exist_in_items, 2):
        array.append((tuple(sorted(combination)), 1))
    return array

def n3(items):
    exist_in_items = set()
    array = list()
    for item in items:
        if item in internal_l2set:
            exist_in_items.add(item)
    for combination in itertools.combinations(exist_in_items, 3):
        array.append((tuple(sorted(combination)), 1))
    return array


# .set("spark.executor.memory", "512m") \
# .set("spark.driver.memory", "512m") \
# .set('spark.executor.pyspark.memory', '512m') \
if __name__ == "__main__":
    path = sys.argv[1]
    supp_count = sys.argv[2]
    conf = SparkConf().set('spark.master', 'yarn') \
        .setAppName("Му Арр") \
        .set("spark.executor.memory", "512m") \
        .set("spark.driver.memory", "512m") \
        .set('spark.executor.pyspark.memory', '512m') \
        .set('spark.executor.extraJavaOptions', '-XX:+UseCompressedOops') \
        .set('spark.rdd.compress', True) \
        .set('spark.serializer', 'org.apache.spark.serializer.KryoSerializer') \
        .set('spark.driver.maxResultSize', '100m') \
        .set('spark.yarn.dist.files',
             'file:/home/hadoop/spark/python/lib/pyspark.zip,file:/home/hadoop/spark/python/lib/py4j-0.10.4-src.zip') \
        .setExecutorEnv('PYTHONPATH', 'pyspark.zip:py4j-0.10.4-src.zip') \
        .set('spark.memory.fraction', 0.1)
    sc = SparkContext(conf=conf)
    transactions = sc.textFile(path)
    minSupportCounts = int(supp_count)
    transaction_items = transactions.map(lambda line: line.split(","))
    l1 = transaction_items.flatMap(n1).reduceByKey(add)
    l1 = l1.filter(lambda i: int(i[1]) > minSupportCounts)
    internal_l1 = l1.collect()
    internal_l1set = {x[0] for x in internal_l1}
    print(internal_l1set)
    sc.broadcast(internal_l1set)

    l2 = transaction_items.flatMap(n2).reduceByKey(add)
    l2 = l2.filter(lambda i: int(i[1]) > minSupportCounts)
    internal_l2 = l2.collect()
    print(internal_l2)

    internal_l2set = set()
    for x in internal_l2:
        for _i in x[0]:
            internal_l2set.add(_i)
    l3 = transaction_items.flatMap(n3).reduceByKey(add)
    l3 = l3.filter(lambda i: int(i[1]) > minSupportCounts)
    internal_l3 = l3.collect()
    print(internal_l3)
    sc.stop()
