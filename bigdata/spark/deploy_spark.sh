#! /bin/sh

SPARK_WS=${SPARK_HOME}
MASTER_HOST=http://localhost:8080/
echo "start to master"
cd $SPARK_WS
sbin/shart-spark.sh
# $# 表示提供到shell脚本或者函数的参数总数；
# $1 表示第一个参数
# #? represent last return value
if [ -z $2 ] then
    echo "your are trying to start a slave in local"
    MASTER_HOME=$2
fi

# if [ -z $1 ] then:
# while
./sbin/start-slave.sh $MASTER_HOME


