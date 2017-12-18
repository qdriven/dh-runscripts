#! /bin/sh

# start/stop/restart server scripts
bin/zkServer.sh <status>

# conencting to ZooKeeper
bin/zkCli.sh -server 127.0.0.1:2181

# cli commands
ls /

# create directory
create /zk_test mydata

get /zk_test
set /zk_test junk
delete /zk_test

# zkClean
sh bin/zkCleanup.sh

#zkCli
bin/zkCli.sh

#zkServer
bin/zkServer.sh

#zkEnv
bin/zkEnv.sh
