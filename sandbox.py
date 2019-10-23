import itertools
from operator import add
import logging
import os

os.environ['HADOOP_USER_NAME'] = 'admin'


def suppress_py4j_logging():
    logger = logging.getLogger('py4j')
    logger.setLevel(logging.WARN)


# sc = SparkContext("spark://localhost:7077", "my-local-testing-pyspark-context")
# # sc = SparkContext("spark://localhost:7077", "my-local-testing-pyspark-context")
# # sc.setLogLevel("WARN")
# # spark = SparkSession(sc)


# from pyspark.sql import SparkSession
# from pyspark.sql import functions as F
# spark = SparkSession\
#         .builder.master("local[*]").config("spark.driver.cores", 1).appName("understanding_sparksession").getOrCreate()

# spark = SparkSession.builder\
#             .master('spark://localhost:7077')\
#             .appName('my-local-testing-pyspark-context')\
#             .enableHiveSupport()\
#             .getOrCreate()
# df = spark.read.option("delimiter", ",").csv('/Users/danielnikulin/Projects/MasterProject/hadoop_spark_perf/dataset/DAT.csv', header=True)
# df = spark.read.csv('/Users/danielnikulin/Projects/MasterProject/hadoop_spark_perf/dataset/DAT.csv')
# df.persist()
# print(df.count())

# df.show(1000, False)


from pyspark import SparkConf, SparkContext
import datetime
conf = SparkConf().setMaster("local[4]").setAppName("Му Арр")
sc = SparkContext(conf=conf)
transactions = sc.textFile("/Users/danielnikulin/Projects/MasterProject/hadoop_spark_perf/dataset/DAT.csv")

now = datetime.datetime.now()
print(now)
minSupport = 0.0002118997384 * transactions.count()
items = transactions.flatMap(lambda line: line.split("\n"))


# print(items.collect())


def n1(item_set):
    array = list()
    for item in item_set.split(","):
        array.append((item, 1))
    return array


itemCount = items.flatMap(n1).reduceByKey(add)
print(itemCount.collect())

print(itemCount.take(5))
l1 = itemCount.filter(lambda i: int(i[1]) > minSupport)
print(l1.collect())
print(l1.count())

# cart = l1.cartesian(l1).cache()
# # sc.broadcast(cart)
internal_l1 = l1.collect()
sc.broadcast(internal_l1)


def n2(item_set):
    exist_in_items = set()
    array = list()
    for item in item_set.split(","):
        exist_in_items.update([it[0] for it in internal_l1 if it[0] == item])
        for combination in itertools.combinations(exist_in_items, 2):
            array.append((sorted(combination), 1))
    return array


l2 = items.flatMap(n2).reduceByKey(add)
l2 = l2.filter(lambda i: int(i[1]) > minSupport)
print(l2.collect())
now = datetime.datetime.now()
print(now)
# print(l2.collect())
# print(l2.count())


# def n2(trx):
#     print(trx)
#
#
# itemCount = items.map(n2)
#
# print(itemCount.collect())

# print(df.columns)
# # df = df.select('COLOR').distinct()
# print(sorted(df.groupBy('BRAND').count().collect(), key=lambda x: x['count']))
# # print(df.count())
# # df.show(100, False)
a = 2
