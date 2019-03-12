#! /bin/sh

## setup ssh local
sudo useradd -s /bin/bash -m -p hadoop hadoop
su - hadoop
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys


## setup hadoop home

echo "export HADOOP_HOME=`pwd`/hadoop-3.1.2" >> ~/.bashrc
echo "exort PATH=$HADOOP_HOME/bin:$PATH"
source ~/.bashrc