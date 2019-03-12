#! /bin/zsh
echo $HADOOP_HOME

# format namenode
bin/hdfs namenode -format
# start namenode and datanode and check it

bin/hdfs dfs -put etc/hadoop input
bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-2.9.2.jar grep input output 'dfs[a-z.]+'
