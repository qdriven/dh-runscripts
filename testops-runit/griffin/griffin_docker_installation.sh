#! /bin/sh
# for linux
# sysctl -w vm.max_map_count=262144


docker pull apachegriffin/griffin_spark2:0.3.0
docker pull apachegriffin/elasticsearch
docker pull apachegriffin/kafka
docker pull zookeeper:3.5


## for china
# docker pull registry.docker-cn.com/apachegriffin/griffin_spark2:0.3.0
# docker pull registry.docker-cn.com/apachegriffin/elasticsearch
# docker pull registry.docker-cn.com/apachegriffin/kafka
# docker pull zookeeper:3.5