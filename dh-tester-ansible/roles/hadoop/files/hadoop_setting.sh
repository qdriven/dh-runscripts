
# Daemon	Environment Variable
# NameNode	HDFS_NAMENODE_OPTS
# DataNode	HDFS_DATANODE_OPTS
# Secondary NameNode	HDFS_SECONDARYNAMENODE_OPTS
# ResourceManager	YARN_RESOURCEMANAGER_OPTS
# NodeManager	YARN_NODEMANAGER_OPTS
# WebAppProxy	YARN_PROXYSERVER_OPTS
# Map Reduce Job History Server	MAPRED_HISTORYSERVER_OPTS

HADOOP_HOME=/Users/patrick/workspace/tools/hadoop-2.8.1
export HADOOP_HOME

# 针对 DataNode 没法启动的解决方法
./sbin/stop-dfs.sh   # 关闭
rm -r ./tmp     # 删除 tmp 文件，注意这会删除 HDFS 中原有的所有数据
./bin/hdfs namenode -format   # 重新格式化 NameNode
./sbin/start-dfs.sh  # 重启

curl http://localhost:50070/dfshealth.html#tab-overview