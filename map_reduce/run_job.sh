#!/usr/bin/env bash
hdfs namenode -format
start-dfs.sh
start-yarn.sh
stop-yarn.sh
stop-dfs.sh
hdfs dfs -ls books

hdfs dfs -ls /tmp
/tmp/logs/hadoop/logs/application_1570478973576_0001/node1_33603
/tmp/logs/hadoop/logs/application_1570478973576_0001/node2_41397
hdfs dfs -cat books/alice.txt
#######
hdfs dfs -mkdir -p /user/hadoop


mkdir /home/hadoop/algorithms
scp -rp /Users/danielnikulin/Projects/MasterProject/hadoop_spark_perf/map_reduce/ hadoop@ec2-52-59-241-77.eu-central-1.compute.amazonaws.com:/home/hadoop/algorithms/

yarn jar ~/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.1.2.jar wordcount "books/*" output

hdfs dfs -mkdir -p /user/hadoop

hdfs dfs -mkdir books

hdfs dfs -mkdir apriori_input


aws s3 cp s3://hadoopparameters/DAT.csv /home/hadoop/test_data/DAT.csv

hdfs dfs -put /home/hadoop/test_data/DAT.csv apriori_input/DAT.csv


yarn jar ~/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.1.2.jar wordcount "books/*" output

hdfs dfs -rm -r output
# First 1n Job
yarn jar ~/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.1.2.jar\
 -input apriori_input/DAT.csv\
 -output output\
 -file /home/hadoop/algorithms/map_reduce/apriori/1_n/base_mapper.py\
 -file /home/hadoop/algorithms/map_reduce/apriori/1_n/reducer_habr.py\
 -mapper "python3 base_mapper.py"\
 -reducer "python3 reducer_habr.py"
# SECOND 2n Job
 yarn jar ~/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.1.2.jar\
 -files /home/hadoop/algorithms/map_reduce/apriori/2_n/2n_mapper.py,/home/hadoop/algorithms/map_reduce/apriori/2_n/2n_reducer.py,hdfs://node-master:9000/user/hadoop/output/part-00000#part-00000\
 -input apriori_input/DAT.csv\
 -output output_2n\
 -mapper "python3 2n_mapper.py"\
 -reducer "python3 2n_reducer.py"

# Third 3n Job

 yarn jar ~/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.1.2.jar\
 -files /home/hadoop/algorithms/map_reduce/apriori/3_n/3n_mapper.py,/home/hadoop/algorithms/map_reduce/apriori/3_n/3n_reducer.py,hdfs://node-master:9000/user/hadoop/output_2n/part-00000#part-00000\
 -input apriori_input/DAT.csv\
 -output output_3n\
 -mapper "python3 3n_mapper.py"\
 -reducer "python3 3n_reducer.py"

part-r-00000
 -cacheFile 'hdfs://node-master:9000/user/hadoop/output/part-00000#part-00000'\
 -file /home/hadoop/algorithms/map_reduce/apriori/2_n/2_n_mapper.py\
 -file /home/hadoop/algorithms/map_reduce/apriori/2_n/2n_reducer.py\

~/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.1.2.jar

hdfs dfs -copyToLocal hdfs://node-master:9000/user/hadoop/output/part-00000 part-00000

 yarn jar ~/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.1.2.jar\
 -files /home/hadoop/algorithms/map_reduce/apriori/3_n/3n_mapper.py,/home/hadoop/algorithms/map_reduce/apriori/3_n/3n_reducer.py,hdfs://node-master:9000/user/hadoop/output_2n/part-00000#part-00000\
 -input apriori_input/*\
 -output output_3n\
 -mapper "python3 3n_mapper.py"\
 -reducer "python3 3n_reducer.py"

 # SIGNIFICANT
-D mapred.map.tasks = 20
# try multiple files books/*