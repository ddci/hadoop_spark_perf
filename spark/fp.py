__author__ = 'Daniil Nikulin'
__license__ = "Apache License 2.0"
__email__ = "danil.nikulin@gmail.com"
__date__ = "22.10.2019"
__app__ = "hadoop_spark_perf"
__status__ = "Development"




from pyspark.mllib.fpm import FPGrowth
from pyspark import SparkConf, SparkContext
conf = SparkConf().setMaster("local").setAppName("Му Арр")
sc = SparkContext(conf=conf)
data = sc.textFile("/Users/danielnikulin/Projects/MasterProject/hadoop_spark_perf/dataset/DAT.csv")
transactions = data.map(lambda line: line.strip().split(','))
print(transactions.take(5))
model = FPGrowth.train(transactions, minSupport=0.000211, numPartitions=10)
result = model.freqItemsets().collect()
for fi in result:
    print(fi)