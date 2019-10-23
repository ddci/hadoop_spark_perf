__author__ = 'Daniil Nikulin'
__license__ = "Apache License 2.0"
__email__ = "danil.nikulin@gmail.com"
__date__ = "13.10.2019"
__app__ = "hadoop_spark_perf"
__status__ = "Development"
import csv

with open('/Users/danielnikulin/Projects/MasterProject/hadoop_spark_perf/dataset/LARGE_DAT.tsv', 'r') as csvin, open(
        '/Users/danielnikulin/Projects/MasterProject/hadoop_spark_perf/dataset/LARGE_DAT.csv', 'w') as tsvout:
    csvin = csv.reader(csvin)
    tsvout = csv.writer(tsvout, delimiter=',')

    for row in csvin:
        tsvout.writerow(row)
