spark-submit --deploy-mode client \
>                --class org.apache.spark.examples.SparkPi \
>               ~/spark_jobs/spark_apriori_own_cluster.py hdfs://hadoop/apriori_input/DAT100K.csv


spark-submit --files ~/spark_jobs/spark_apriori_own_cluster.py\
  --master yarn \
  --deploy-mode cluster ~/spark_jobs/spark_apriori_own_cluster.py\
  hdfs://node-master:9000/user/hadoop/apriori_input/csv/DAT50M.csv 12500


spark-submit --files ~/spark_jobs/spark_apriori_own_cluster.py\
  --master yarn \
  --deploy-mode cluster \
  --num-executors 3  \
  --executor-memory 512mb \
  --executor-cores 1 ~/spark_jobs/spark_apriori_own_cluster.py hdfs://node-master:9000/user/hadoop/apriori_input/csv/DAT200M.csv 50000



PATH=/home/hadoop/spark/bin:$PATH
export HADOOP_CONF_DIR=/home/hadoop/hadoop/etc/hadoop
export SPARK_HOME=/home/hadoop/spark
export LD_LIBRARY_PATH=/home/hadoop/hadoop/lib/native:$LD_LIBRARY_PATH
export PYSPARK_PYTHON=/usr/bin/python3



export PYTHONPATH=${SPARK_HOME}/python:${SPARK_HOME}/python/build:$PYTHONPATH







$SPARK_HOME/conf/spark-defaults.conf