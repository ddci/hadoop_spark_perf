#!/usr/bin/env bash

stop-yarn.sh && stop-dfs.sh
mkdir /home/hadoop/algorithms
scp -rp /Users/danielnikulin/Projects/MasterProject/hadoop_spark_perf/map_reduce/ hadoop@ec2-52-57-251-35.eu-central-1.compute.amazonaws.com:/home/hadoop/algorithms/
scp -rp /Users/danielnikulin/Projects/MasterProject/hadoop_spark_perf/regular/ hadoop@ec2-52-57-251-35.eu-central-1.compute.amazonaws.com:/home/hadoop/algorithms/regular/
scp -rp /Users/danielnikulin/Projects/MasterProject/hadoop_spark_perf/dataset/perf_test/ hadoop@ec2-52-57-251-35.eu-central-1.compute.amazonaws.com:/home/hadoop/perf_test/

#######
hdfs namenode -format
start-dfs.sh && start-yarn.sh
hdfs dfs -mkdir -p /user/hadoop
hdfs dfs -mkdir apriori_input
hdfs dfs -put /home/hadoop/perf_test/csv/ apriori_input/


hdfs namenode -format &&
start-dfs.sh && start-yarn.sh &&
hdfs dfs -mkdir -p /user/hadoop &&
hdfs dfs -mkdir apriori_input &&
hdfs dfs -put /home/hadoop/perf_test/csv/ apriori_input/

aws s3 cp s3://hadoopparameters/DAT.csv /home/hadoop/test_data/DAT.csv
aws s3 cp s3://hadoopparameters/DAT.tsv /home/hadoop/test_data/DAT.tsv


hdfs dfs -put /home/hadoop/test_data/DAT.csv apriori_input/DAT.csv

hdfs dfs -rm -r output

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
-D mapred.reduce.tasks=2
-D mapred.map.tasks = 20
# try multiple files books/*
wc -l <filename>
head -n 100000 DAT.csv > DAT100K.csv

for i in {1..4}
do
   cat DAT1M.csv >> DAT4M.csv
   echo "Welcome $i times"
done




yarn logs -applicationId<applicationID>
yarn logs -applicationId application_1570478973576_0002

yarn application -kill application_1572208120423_0003


/Users/danielnikulin/Projects/MasterProject/hadoop_spark_perf/dataset/DAT.tsv -s 0.0002118997384 -c 0 -l 3
python3 /home/hadoop/algorithms/regular_apriori_3_habr.py /home/hadoop/test_data/DAT.tsv -s 0.0002118997384 -c 0 -l 3
