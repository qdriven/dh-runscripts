
# get haddop 
getHadoop(){
    VERSION=3.1.2
    BIGDATA_HOME=/media/patrick/workspace/bigdata
    mkdir -p $BIGDATA_HOME
    cd $BIGDATA_HOME
    wget https://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/current/hadoop-$VERSION.tar.gz 
    wget https://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/current/hadoop-$VERSION-src.tar.gz
}

getHive() {
    HIVE_VERSION=3.1.1
    BIGDATA_HOME=/media/patrick/workspace/bigdata
    mkdir -p $BIGDATA_HOME
    cd $BIGDATA_HOME
    wget https://mirrors.tuna.tsinghua.edu.cn/apache/hive/hive-$HIVE_VERISON/apache-hive-$HIVE_VERSION-bin.tar.gz 
    wget https://mirrors.tuna.tsinghua.edu.cn/apache/hive/hive-$HIVE_VERSION/apache-hive-$HIVE_VERSION-src.tar.gz
}
getHBase() {
    HBASE_VERSION=2.1.3
    BIGDATA_HOME=/media/patrick/workspace/bigdata
    mkdir -p $BIGDATA_HOME
    cd $BIGDATA_HOME
    URL=https://mirrors.tuna.tsinghua.edu.cn/apache/hbase/$HBASE_VERSION/
    wget  $URL/hbase-$HBASE_VERSION-bin.tar.gz 
    wget  $URL/hbase-$HBASE_VERSION-src.tar.gz 
}


getFlink() {
    FLINK_VERSION=1.7.2
    BIGDATA_HOME=/media/patrick/workspace/bigdata
    mkdir -p $BIGDATA_HOME
    cd $BIGDATA_HOME
    URL=https://mirrors.tuna.tsinghua.edu.cn/apache/flink/flink-$FLINK_VERSION
    wget  $URL/flink-$FLINK_VERSION-bin-scala_2.12.tgz
    wget  $URL/flink-$FLINK_VERSION-src.tar.gz
}

getSpark() {
    SPARK_VERSION=2.3.3
    BIGDATA_HOME=/media/patrick/workspace/bigdata
    mkdir -p $BIGDATA_HOME
    cd $BIGDATA_HOME
    URL=https://mirrors.tuna.tsinghua.edu.cn/apache/spark/spark-$SPARK_VERSION
    # wget  $URL/spark-$SPARK_VERSION.tgz  
    # wget $URL/spark-$SPARK_VERSION-bin-without-hadoop.tgz
    wget $URL/pyspark-$SPARK_VERSION.tar.gz 
}



# getHadoop
# getHive
# getHBase
getFlink
# getSpark
cd  /media/patrick/workspace/bigdata
wget https://mirrors.tuna.tsinghua.edu.cn/apache/maven/maven-3/3.6.0/binaries/apache-maven-3.6.0-bin.tar.gz






