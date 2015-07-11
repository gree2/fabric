#! *-* coding: utf-8 *-*
"""downloading hadoop ecosystem software"""

from fabric.api import env, run

env.hosts = ['localhost']

MIRROR = 'http://mirrors.cnnic.cn/apache/'
CMD = 'wget {0}{1} -P {2}'
WORKING_DIR = '~/Downloads/'

VER_ACCUMULO = '1.7.0'
VER_DRILL = '1.0.0'
VER_FLUME = '1.6.0'
VER_HADOOP = '2.7.0'
VER_HBASE = '1.1.0.1'
VER_HIVE = '1.2.0'
VER_KAFKA = '0.8.2.1'
VER_OOZIE = '4.2.0'
VER_PHOENIX = '4.3.1'
VER_PIG = '0.15.0'
VER_SOLR = '5.2.0'
VER_SPARK = '1.4.0'
VER_SQOOP1 = '1.4.6'
VER_SQOOP2 = '1.99.6'
VER_STORM = '0.9.5'
VER_TEZ = '0.7.0'
VER_ZOOKEEPER = '3.4.6'

PATH_ACCUMULO = 'accumulo/{0}/accumulo-{0}-bin.tar.gz'
PATH_DRILL = 'drill/drill-{0}/apache-drill-{0}.tar.gz'
PATH_FLUME = 'flume/{0}/apache-flume-{0}-bin.tar.gz'
PATH_HADOOP = 'hadoop/common/hadoop-{0}/hadoop-{0}.tar.gz'
PATH_HBASE = 'hbase/{0}/hbase-{0}-bin.tar.gz'
PATH_HIVE = 'hive/hive-{0}/apache-hive-{0}-bin.tar.gz'
PATH_KAFKA = 'kafka/{0}/kafka_2.9.1-{0}.tgz'
PATH_OOZIE = 'oozie/{0}/oozie-{0}.tar.gz'
PATH_PHOENIX = 'phoenix/phoenix-{0}/bin/phoenix-{0}-bin.tar.gz'
PATH_PIG = 'pig/pig-{0}/pig-{0}.tar.gz'
PATH_SOLR = 'lucene/solr/{0}/solr-{0}.tgz'
PATH_SPARK = 'spark/spark-{0}/spark-{0}.tgz'
PATH_SQOOP1 = 'sqoop/{0}/sqoop-{0}.bin__hadoop-2.0.4-alpha.tar.gz'
PATH_SQOOP2 = 'sqoop/{0}/sqoop-{0}-bin-hadoop200.tar.gz'
PATH_STORM = 'storm/apache-storm-{0}/apache-storm-{0}.tar.gz'
PATH_TEZ = 'tez/{0}/apache-tez-{0}-src.tar.gz'
PATH_ZOOKEEPER = 'zookeeper/zookeeper-{0}/zookeeper-{0}.tar.gz'

# CONNECTOR_MY = "curl -L \
# 'http://www.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.35.tar.gz/from/http://mysql.he.net/' \
# > {0}/mysql-connector-java-5.1.35.tar.gz"

# CONNECTOR_MS = "curl -L \
# 'http://download.microsoft.com/download/0/2/A/02AAE597-3865-456C-AE7F-613F99F850A8/sqljdbc_4.0.2206.100_enu.tar.gz' \
# > {0}/sqljdbc_4.0.2206.100_enu.tar.gz"

CONNECTOR_MY = "curl -L \
'http://www.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.35.tar.gz/from/http://mysql.he.net/' \
| tar xz -C {0}"

CONNECTOR_MS = "curl -L \
'http://download.microsoft.com/download/0/2/A/02AAE597-3865-456C-AE7F-613F99F850A8/sqljdbc_4.0.2206.100_enu.tar.gz' \
| tar xz -C {0}"

def get00(version=VER_ACCUMULO, prefix=WORKING_DIR):
    """get accumulo    => fab get00:1.7.0,prefix"""
    run(CMD.format(MIRROR, PATH_ACCUMULO.format(version), prefix))

def get01(version=VER_DRILL, prefix=WORKING_DIR):
    """get drill       => fab get01:1.0.0,prefix"""
    run(CMD.format(MIRROR, PATH_DRILL.format(version), prefix))

def get02(version=VER_FLUME, prefix=WORKING_DIR):
    """get flume       => fab get02:1.6.0,prefix"""
    run(CMD.format(MIRROR, PATH_FLUME.format(version), prefix))

def get03(version=VER_HADOOP, prefix=WORKING_DIR):
    """get hadoop      => fab get03:2.7.0,prefix"""
    run(CMD.format(MIRROR, PATH_HADOOP.format(version), prefix))

def get04(version=VER_HBASE, prefix=WORKING_DIR):
    """get hbase       => fab get04:1.1.0.1,prefix"""
    run(CMD.format(MIRROR, PATH_HBASE.format(version), prefix))

def get05(version=VER_HIVE, prefix=WORKING_DIR):
    """get hive        => fab get05:1.2.0,prefix"""
    run(CMD.format(MIRROR, PATH_HIVE.format(version), prefix))

def get06(version=VER_KAFKA, prefix=WORKING_DIR):
    """get kafka       => fab get06:0.8.2.1,prefix"""
    run(CMD.format(MIRROR, PATH_KAFKA.format(version), prefix))

def get07(version=VER_OOZIE, prefix=WORKING_DIR):
    """get oozie       => fab get07:4.2.0,prefix"""
    run(CMD.format(MIRROR, PATH_OOZIE.format(version), prefix))

def get08(version=VER_PHOENIX, prefix=WORKING_DIR):
    """get phoenix     => fab get08:4.3.1,prefix"""
    run(CMD.format(MIRROR, PATH_PHOENIX.format(version), prefix))

def get09(version=VER_PIG, prefix=WORKING_DIR):
    """get pig         => fab get09:0.15.0,prefix"""
    run(CMD.format(MIRROR, PATH_PIG.format(version), prefix))

def get10(version=VER_SOLR, prefix=WORKING_DIR):
    """get solr        => fab get10:5.2.0,prefix"""
    run(CMD.format(MIRROR, PATH_SOLR.format(version), prefix))

def get11(version=VER_SPARK, prefix=WORKING_DIR):
    """get spark       => fab get11:1.4.0,prefix"""
    run(CMD.format(MIRROR, PATH_SPARK.format(version), prefix))

def get120():
    """get connector   => fab get120"""
    run(CONNECTOR_MS.format(WORKING_DIR))
    run(CONNECTOR_MY.format(WORKING_DIR))

def get121(version=VER_SQOOP1, prefix=WORKING_DIR):
    """get sqoop       => fab get121:1.4.6,prefix"""
    run(CMD.format(MIRROR, PATH_SQOOP1.format(version), prefix))

def get122(version=VER_SQOOP2, prefix=WORKING_DIR):
    """get sqoop       => fab get122:1.99.6,prefix"""
    run(CMD.format(MIRROR, PATH_SQOOP2.format(version), prefix))

def get13(version=VER_STORM, prefix=WORKING_DIR):
    """get storm       => fab get13:0.9.5,prefix"""
    run(CMD.format(MIRROR, PATH_STORM.format(version), prefix))

def get14(version=VER_TEZ, prefix=WORKING_DIR):
    """get tez         => fab get14:0.7.0,prefix"""
    run(CMD.format(MIRROR, PATH_TEZ.format(version), prefix))

def get15(version=VER_ZOOKEEPER, prefix=WORKING_DIR):
    """get zookeeper   => fab get15:3.4.6,prefix"""
    run(CMD.format(MIRROR, PATH_ZOOKEEPER.format(version), prefix))
