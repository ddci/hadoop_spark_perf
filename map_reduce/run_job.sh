#!/usr/bin/env bash

yarn jar ~/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.1.2.jar wordcount "books/*" output

hdfs dfs -mkdir -p /user/hadoop

hdfs dfs -mkdir books

hdfs dfs -mkdir apriori_input

aws s3 cp s3://hadoopparameters/DAT.csv /home/hadoop/test_data/DAT.csv

mkdir test_data

aws s3 cp s3://hadoopparameters/DAT.csv /home/hadoop/test_data/DAT.csv

hdfs dfs -put /home/hadoop/test_data/DAT.csv apriori_input


yarn jar ~/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.1.2.jar wordcount "books/*" output

hdfs dfs -rm -r output

yarn jar ~/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.1.2.jar\
 -input apriori_input/DAT.csv\
 -output output\
 -file mapper.py\
 -file reducer.py\
 -mapper "python mapper.py"\
 -reducer "python reducer.py"

part-r-00000


~/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.1.2.jar