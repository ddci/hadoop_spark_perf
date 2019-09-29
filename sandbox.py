from pyspark import SparkContext

__author__ = 'Daniil Nikulin'
__license__ = "Apache License 2.0"
__email__ = "danil.nikulin@gmail.com"
__date__ = "2019-07-07"
__app__ = "mp_donntu_spark_hdfs"
__status__ = "Development"




import logging

import pyspark.sql.functions as psf
from pyspark.sql import SparkSession
from pyspark.sql.types import DecimalType, StructType, StructField, FloatType, ArrayType, IntegerType, StringType, \
    BooleanType
import os
os.environ['HADOOP_USER_NAME'] = 'admin'

def suppress_py4j_logging():
    logger = logging.getLogger('py4j')
    logger.setLevel(logging.WARN)


sc = SparkContext("spark://localhost:7077", "my-local-testing-pyspark-context")
sc.setLogLevel("WARN")
spark = SparkSession(sc)


# spark = SparkSession.builder\
#             .master('spark://localhost:7077')\
#             .appName('my-local-testing-pyspark-context')\
#             .enableHiveSupport()\
#             .getOrCreate()
df = spark.read.option("delimiter", ";").csv('hdfs://192.168.0.101:8020/fop.xml', header=True)
df.persist()
print(df.count())
df.show(100, False)


# print(df.columns)
# # df = df.select('COLOR').distinct()
# print(sorted(df.groupBy('BRAND').count().collect(), key=lambda x: x['count']))
# # print(df.count())
# # df.show(100, False)
a = 2
