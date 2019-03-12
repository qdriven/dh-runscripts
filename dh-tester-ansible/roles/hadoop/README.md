# Install Hadoop

- Local(standalone) Mode
- Pseudo-Distributed Mode
- Full-Distributed Mode

# Local Mode

```sh
mkdir input
cp etc/hadoop/*.xml input
hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-3.0.0-beta1.jar \
     grep input output 'dfs[a-z.]+'
cat output/*
```

## 1. Cluster Mode Setup

- setup profile.d
- setup hosts
- setup hostname and reboot
- setup JDK
- setup /etc/profile

```shell
export JAVA_HOME=/usr/lib/jvm/jre-1.7.0-openjdk.x86_64
export PATH=$JAVA_HOME/bin:$PATH
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
```

```shell
source /etc/profile
```

- setup firewall
```shell
service iptables status
service iptables stop
```
```
-- 关闭SELINUX
# vim /etc/selinux/config
-- 注释掉
#SELINUX=enforcing
#SELINUXTYPE=targeted
-- 添加
SELINUX=disabled
```

本机无密码登陆：

```
ssh-keygen -t rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ～/.ssh/authorized_keys
ssh hadoop-master
```

hadoop env

```sh
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/bin 
source /etc/profile
```

core-site.xml

```
<configuration>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>file:/usr/local/hadoop/tmp</value>
        <description>Abase for other temporary directories.</description>
    </property>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://hadoop-master:9000</value>
    </property>
</configuration>
```

hdfs-site.xml
```
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>3</value>
    </property>
    <property>
        <name>dfs.name.dir</name>
        <value>/usr/local/hadoop/hdfs/name</value>
    </property>
    <property>
        <name>dfs.data.dir</name>
        <value>/usr/local/hadoop/hdfs/data</value>
    </property>
</configuration>
```

mapred-site.xml

```
<configuration>
  <property>
      <name>mapreduce.framework.name</name>
      <value>yarn</value>
  </property>
   <property>
      <name>mapred.job.tracker</name>
      <value>http://hadoop-master:9001</value>
  </property>
</configuration>
```

yarn-site.xml
```
<configuration>
<!-- Site specific YARN configuration properties -->
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>hadoop-master</value>
    </property>
</configuration>
```

masters/namenode

```
vi /usr/local/hadoop/etc/hadoop/masters
## 内容
hadoop-master
```
salves
```
vi /usr/local/hadoop/etc/hadoop/slaves
## 内容
hadoop-slave1
hadoop-slave2
hadoop-slave3
```

```
rm -rf /usr/local/hadoop/etc/hadoop/slaves
```

## 启动HDFS

```sh
# format
bin/hadoop namenode -format
# start all
sbin/start-all.sh
# JPS master
# 25928 SecondaryNameNode
# 25742 NameNode
# 26387 Jps
# 26078 ResourceManager

# jps slave
# 24002 NodeManager
# 23899 DataNode
# 24179 Jps
```

## hadoop metrics

```sh
hadoop dfsadmin -report
```

## restart hadoop

```
sbin/stop-all.sh
sbin/start-all.sh
```

## setup javahome to hadoop-env.sh



## web namenode move to 
from hadoop 3.0
http://localhost:9870

