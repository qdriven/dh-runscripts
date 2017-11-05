# Hadoop

## Install Hadoop

- pass ssh key to server

```sh
ssh-keygen -t rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys 
chmod 0600 ~/.ssh/authorized_keys 
```

- setup java

```sh
export JAVA_HOME=/usr/local/jdk1.7.0_71 
export PATH=PATH:$JAVA_HOME/bin 
```

- setup hadoop home

```sh
export HADOOP_HOME=/usr/local/hadoop 
```
