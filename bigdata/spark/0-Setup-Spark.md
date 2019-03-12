# Setup Spark

- Stardalone

## Installing Spark Standalone to a Cluster

1. First Start Master

```sh
sbin/start-master.sh
```
open http://localhost:8080 to check it or use jps to find out master process is started

```sh
➜  spark-2.4.0-bin-hadoop2.7 jps
5841 Main
6196 RemoteMavenServer
19277 Jps
8461 Master
```

2. Submit Slave if needed

```sh
./sbin/start-slave.sh <master-spark-URL>
```

- sbin/start-master.sh - Starts a master instance on the machine the script is executed on.
- sbin/start-slaves.sh - Starts a slave instance on each machine specified in the conf/slaves file.
- sbin/start-slave.sh - Starts a slave instance on the machine the script is executed on.
- sbin/start-all.sh - Starts both a master and a number of slaves as described above.
- sbin/stop-master.sh - Stops the master that was started via the sbin/start-master.sh script.
- sbin/stop-slaves.sh - Stops all slave instances on the machines specified in the conf/slaves file.
- sbin/stop-all.sh - Stops both the master and the slaves as described above.