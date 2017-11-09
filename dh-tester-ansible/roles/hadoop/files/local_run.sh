# /bin/sh

mkdir input
cp etc/hadoop/*.xml input
hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-3.0.0-beta1.jar \
     grep input output 'dfs[a-z.]+'
cat output/*