#! /bin/sh

# format file system

hdfs namenode -format

# starting namenode and datanode daemon

sbin/start-dfs.sh

# make HDFS directories required to execute MR Job

hdfs dfs -mkdir /user
hdfs dfs -mkdir /user/<username>

# copy to distributed file system
hdfs dfs -mkdir input
# run job
hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-3.0.0-beta1.jar grep input output 'dfs[a-z.]+'

# copy to local
hdfs dfs -get output output
cat output/*

# checkout the result in distributed file system
hdfs dfs -cat output/*

# stop the dfs
sbin/stop-dfs.sh

# YRAN on Single Node- Running MR job on YARN
# config mapred-site.xml
