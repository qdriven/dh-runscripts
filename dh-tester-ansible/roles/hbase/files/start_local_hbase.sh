#! /bin/sh

# 1.install jdk
# 2. copy config file allround server
# 3. start hbase 
# 4. running hbase and hadoop in a same server
HBASE_HOME=hbase-2.1.1
echo "copy hbase site files to config"
cp -f hbase-site_local.xml ${HBASE_HOME}/conf/hbase-site.xml
echo "start hbase"
cd ${HBASE_HOME}/bin
sh start-hbase.sh