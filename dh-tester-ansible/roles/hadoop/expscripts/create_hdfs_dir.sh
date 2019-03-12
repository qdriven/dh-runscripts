#! /bin/bash

USER_NAME=$1
cd ../files/hadoop-3.1.2

bin/hdfs dfs -mkdir /user
bin/hdfs dfs -mkdir /user/$USER_NAME