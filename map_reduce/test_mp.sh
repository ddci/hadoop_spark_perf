# 1
yarn jar ~/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.1.3.jar\
 -input apriori_input/csv/DAT4M.csv\
 -output output\
 -file /home/hadoop/algorithms/apriori/1_n/base_mapper.py\
 -file /home/hadoop/algorithms/apriori/1_n/1n_reducer.py\
 -file /home/hadoop/algorithms/apriori/1_n/1n_combiner.py\
 -mapper "python3 base_mapper.py"\
 -combiner "python3 1n_combiner.py"\
 -reducer "python3 1n_reducer.py"

 hdfs dfs -rm -r output
 hdfs dfs -cat /user/hadoop/output/part-00000

# SECOND 2n Job
yarn jar ~/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.1.3.jar\
 -files /home/hadoop/algorithms/apriori/2_n/2n_mapper.py,/home/hadoop/algorithms/apriori/2_n/2n_reducer.py,/home/hadoop/algorithms/apriori/2_n/2n_combiner.py,hdfs://node-master:9000/user/hadoop/output/part-00000#part-00000\
 -D mapred.map.tasks=1\
 -input apriori_input/csv/DAT4M.csv\
 -output output_2n\
 -mapper "python3 2n_mapper.py"\
 -combiner "python3 2n_combiner.py"\
 -reducer "python3 2n_reducer.py"

 hdfs dfs -rm -r output_2n
 hdfs dfs -cat /user/hadoop/output_2n/part-00000


# 3
yarn jar ~/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.1.3.jar\
 -files /home/hadoop/algorithms/apriori/3_n/3n_mapper.py,/home/hadoop/algorithms/apriori/3_n/3n_reducer.py,/home/hadoop/algorithms/apriori/3_n/3n_combiner.py,hdfs://node-master:9000/user/hadoop/output_2n/part-00000#part-00000\
 -input apriori_input/csv/DAT4M.csv\
 -output output_3n\
 -mapper "python3 3n_mapper.py"\
 -combiner "python3 3n_reducer.py"\
 -reducer "python3 3n_reducer.py"

 hdfs dfs -rm -r output_3n
 hdfs dfs -cat /user/hadoop/output_3n/part-00000

 hdfs dfs -rm -r output && hdfs dfs -rm -r output_2n && hdfs dfs -rm -r output_3n