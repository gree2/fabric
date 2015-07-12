#! *-* coding: utf-8 *-*
"""deploy hadoop ecosystem"""

from fabric.api import env, settings
from fabric.operations import run, put
import os

APP_HOME = '/app'
DEPLOY_HOME = '/opt/bigdata'
CONF_HOME = '~/Documents/github/fabric/cluster'
SOFTWARE_HOME = '~/Downloads'

# hadoop
HADOOP_CFGS = [
    'core-site.xml',
    'hdfs-site.xml',
    'mapred-site.xml',
    'slaves',
    'yarn-site.xml']
HADOOP_NN = 'node5'
HADOOP_PKG = 'hadoop-2.7.0.tar.gz'

# zookeeper
ZOOKEEPER_CFG = 'zoo.cfg'
ZOOKEEPER_PKG = 'zookeeper-3.4.6.tar.gz'

# hbase
HBASE_CFGS = [
    'backup-masters',
    'hbase-env.sh',
    'regionservers',
    'hbase-site.xml']
HBASE_MASTER = 'node5'
HBASE_PKG = 'hbase-1.0.1.1-bin.tar.gz'

# sqoop
SQOOP1_PKG = 'sqoop-1.4.6.bin__hadoop-2.0.4-alpha.tar.gz'
SQOOP2_PKG = 'sqoop-1.99.6-bin-hadoop200.tar.gz'
SQOOP_LIB_MYSQL = 'mysql-connector-java-5.1.35-bin.jar'
SQOOP_LIB_MSSQL = 'sqljdbc4.jar'

# spark
SPARK_MASTER = 'node5'
SPARK_PKG = 'spark-1.4.0-bin-hadoop2.6.tgz'

env.user = 'hduser'
env.password = 'icssda'

def seth(start=2, stop=5):
    """set host            => fab seth:2,5"""
    env.user = 'hduser'
    env.hosts = ["node%d" % i for i in range(int(start), int(stop) + 1)]

def hd0():
    """hadoop uninstall     => fab seth:2,5 hd0"""
    # 0. rm hadoop
    file_i = os.path.join(DEPLOY_HOME, 'hadoop')
    run('rm -rf {0}'.format(file_i))
    file_i = os.path.join(APP_HOME, 'hadoop')
    run('rm -rf {0}'.format(file_i))

def hd1():
    """hadoop install      => fab seth:2,5 hd1"""
    # 1. copy package
    file_i = os.path.join(SOFTWARE_HOME, HADOOP_PKG)
    file_o = os.path.join(DEPLOY_HOME, HADOOP_PKG)
    put(file_i, file_o)

    # 2. unzip
    file_i = os.path.join(DEPLOY_HOME, HADOOP_PKG)
    run('tar -zxf {0} -C {1}'.format(file_i, DEPLOY_HOME))

    # 3. rename
    file_i = os.path.join(DEPLOY_HOME, 'hadoop-2.7.0')
    file_o = os.path.join(DEPLOY_HOME, 'hadoop')
    run('mv {0} {1}'.format(file_i, file_o))

    # 4. copy cfg
    for cfg in HADOOP_CFGS:
        file_i = os.path.join(CONF_HOME, cfg)
        file_o = os.path.join(DEPLOY_HOME, 'etc/hadoop', cfg)
        put(file_i, file_o)

    # 5. clean up
    file_i = os.path.join(DEPLOY_HOME, HADOOP_PKG)
    run('rm {0}'.format(file_i))

def hd2():
    """hadoop nn format    => fab seth:5,5 hd2"""
    file_i = os.path.join(DEPLOY_HOME, 'hadoop/bin/hdfs namenode -format')
    run(file_i)

def hd3(option):
    """hadoop start        => fab seth:5,5 hd3:start/stop"""
    if 'start' == option:
        with settings(host_string=HADOOP_NN):
            file_i = os.path.join(DEPLOY_HOME, 'hadoop/sbin/start-dfs.sh')
            run(file_i)
            file_i = os.path.join(DEPLOY_HOME, 'hadoop/sbin/start-yarn.sh')
            run(file_i)
    elif 'stop' == option:
        with settings(host_string=HADOOP_NN):
            file_i = os.path.join(DEPLOY_HOME, 'hadoop/sbin/stop-yarn.sh')
            run(file_i)
            file_i = os.path.join(DEPLOY_HOME, 'hadoop/sbin/stop-dfs.sh')
            run(file_i)
    else:
        print 'fab seth:5,5 hd3:start/stop'

def zk0():
    """zookeeper uninstall => fab seth:2,4 zk0"""
    # 0. rm zookeeper
    file_i = os.path.join(DEPLOY_HOME, 'zookeeper')
    run('rm -rf {0}'.format(file_i))
    file_i = os.path.join(APP_HOME, 'zookeeper')
    run('rm -rf {0}'.format(file_i))

def zk1():
    """zookeeper install   => fab seth:2,4 zk1"""
    # 1. copy package
    file_i = os.path.join(SOFTWARE_HOME, ZOOKEEPER_PKG)
    file_o = os.path.join(DEPLOY_HOME, ZOOKEEPER_PKG)
    put(file_i, file_o)

    # 2. unzip
    file_i = os.path.join(DEPLOY_HOME, ZOOKEEPER_PKG)
    run('tar -zxf {0} -C {1}'.format(file_i, DEPLOY_HOME))

    # 3. rename
    file_i = os.path.join(DEPLOY_HOME, 'zookeeper-3.4.6')
    file_o = os.path.join(DEPLOY_HOME, 'zookeeper')
    run('mv {0} {1}'.format(file_i, file_o))

    # 4. copy cfg
    file_i = os.path.join(CONF_HOME, ZOOKEEPER_CFG)
    file_o = os.path.join(DEPLOY_HOME, 'zookeeper/conf', ZOOKEEPER_CFG)
    put(file_i, file_o)

    # 5. clean up
    file_i = os.path.join(DEPLOY_HOME, ZOOKEEPER_PKG)
    run('rm {0}'.format(file_i))

def zk3():
    """zookeeper set myid  => fab seth:2,4 zk3"""
    for i in range(2, 5):
        with settings(host_string='node{0}'.format(i)):
            run('mkdir -p /app/zookeeper/data')
            run('echo {0} > /app/zookeeper/data/myid'.format(i))

def zk4(option):
    """zookeeper service   => fab seth:2,4 zk4:start/stop/status"""
    file_i = os.path.join(DEPLOY_HOME, 'zookeeper/bin/zkServer.sh {0}'.format(option))
    run(file_i)

def hb0():
    """hbase uninstall     => fab seth:2,5 hb0"""
    # 0. rm hbase
    file_i = os.path.join(DEPLOY_HOME, 'hbase')
    run('rm -rf {0}'.format(file_i))

def hb1():
    """hbase install       => fab seth:2,5 hb1"""
    # 1. copy package
    file_i = os.path.join(SOFTWARE_HOME, HBASE_PKG)
    file_o = os.path.join(DEPLOY_HOME, HBASE_PKG)
    put(file_i, file_o)

    # 2. unzip
    file_i = os.path.join(DEPLOY_HOME, HBASE_PKG)
    run('tar -zxf {0} -C {1}'.format(file_i, DEPLOY_HOME))

    # 3. rename
    file_i = os.path.join(DEPLOY_HOME, 'hbase-1.0.1.1')
    file_o = os.path.join(DEPLOY_HOME, 'hbase')
    run('mv {0} {1}'.format(file_i, file_o))

    # 4. copy cfg
    for cfg in HBASE_CFGS:
        file_i = os.path.join(CONF_HOME, 'hbase', cfg)
        file_o = os.path.join(DEPLOY_HOME, 'hbase/conf', cfg)
        put(file_i, file_o)

    # 5. clean up
    file_i = os.path.join(DEPLOY_HOME, HBASE_PKG)
    run('rm {0}'.format(file_i))

def hb2(option):
    """hbase server        => fab seth:5,5 hb2:start/stop"""
    with settings(host_string=HBASE_MASTER):
        file_i = os.path.join(DEPLOY_HOME, 'hbase/bin', '{0}-hbase.sh'.format(option))
        run(file_i)

def sq10():
    """sqoop1 uninstall    => fab seth:3,3 sq10"""
    # 0. rm sqoop
    file_i = os.path.join(DEPLOY_HOME, 'sqoop')
    run('rm -rf {0}'.format(file_i))

def sq11():
    """sqoop1 install      => fab seth:3,3 sq11"""
    # 1. copy package
    file_i = os.path.join(SOFTWARE_HOME, SQOOP1_PKG)
    file_o = os.path.join(DEPLOY_HOME, SQOOP1_PKG)
    put(file_i, file_o)

    # 2. unzip
    file_i = os.path.join(DEPLOY_HOME, SQOOP1_PKG)
    run('tar -zxf {0} -C {1}'.format(file_i, DEPLOY_HOME))

    # 3. rename
    file_i = os.path.join(DEPLOY_HOME, 'sqoop-1.4.6.bin__hadoop-2.0.4-alpha')
    file_o = os.path.join(DEPLOY_HOME, 'sqoop')
    run('mv {0} {1}'.format(file_i, file_o))

    # 4. install dependencies - jar
    file_i = os.path.join(SOFTWARE_HOME, 'sqljdbc_4.0/enu', SQOOP_LIB_MSSQL)
    file_o = os.path.join(DEPLOY_HOME, 'sqoop/lib', SQOOP_LIB_MSSQL)
    put(file_i, file_o)
    file_i = os.path.join(SOFTWARE_HOME, 'mysql-connector-java-5.1.35', SQOOP_LIB_MYSQL)
    file_o = os.path.join(DEPLOY_HOME, 'sqoop/lib', SQOOP_LIB_MYSQL)
    put(file_i, file_o)

    # 5. clean up
    file_i = os.path.join(DEPLOY_HOME, SQOOP1_PKG)
    run('rm {0}'.format(file_i))

def sq20():
    """sqoop2 uninstall    => fab seth:2,3 sq20"""
    # 0. rm sqoop
    file_i = os.path.join(DEPLOY_HOME, 'sqoop')
    run('rm -rf {0}'.format(file_i))

def sq21():
    """sqoop2 install      => fab seth:2,3 sq21"""
    # 1. copy package
    file_i = os.path.join(SOFTWARE_HOME, SQOOP2_PKG)
    file_o = os.path.join(DEPLOY_HOME, SQOOP2_PKG)
    put(file_i, file_o)

    # 2. unzip
    file_i = os.path.join(DEPLOY_HOME, SQOOP2_PKG)
    run('tar -zxf {0} -C {1}'.format(file_i, DEPLOY_HOME))

    # 3. rename
    file_i = os.path.join(DEPLOY_HOME, 'sqoop-1.99.6-bin-hadoop200')
    file_o = os.path.join(DEPLOY_HOME, 'sqoop')
    run('mv {0} {1}'.format(file_i, file_o))

    # 4. install dependencies - jar
    file_i = os.path.join(SOFTWARE_HOME, 'sqljdbc_4.0/enu', SQOOP_LIB_MSSQL)
    file_o = os.path.join(DEPLOY_HOME, 'sqoop/server/lib', SQOOP_LIB_MSSQL)
    put(file_i, file_o)
    file_i = os.path.join(SOFTWARE_HOME, 'mysql-connector-java-5.1.35', SQOOP_LIB_MYSQL)
    file_o = os.path.join(DEPLOY_HOME, 'sqoop/server/lib', SQOOP_LIB_MYSQL)
    put(file_i, file_o)

    # 4. install dependencies - lib
    file_i = os.path.join(DEPLOY_HOME, 'sqoop/server/conf/catalina.properties')
    # common
    replace_i = '/usr/lib/hadoop/\\*.jar'
    replace_o = '/hadoop/share/hadoop/common/\\*.jar'
    run("sed 's@{0}@{1}{2}@' -i {3}".format(replace_i, DEPLOY_HOME, replace_o, file_i))
    replace_i = '/usr/lib/hadoop/lib/\\*.jar'
    replace_o = '/hadoop/share/hadoop/common/lib/\\*.jar'
    run("sed 's@{0}@{1}{2}@' -i {3}".format(replace_i, DEPLOY_HOME, replace_o, file_i))
    # hdfs
    replace_i = '/usr/lib/hadoop-hdfs/\\*.jar'
    replace_o = '/hadoop/share/hadoop/hdfs/\\*.jar'
    run("sed 's@{0}@{1}{2}@' -i {3}".format(replace_i, DEPLOY_HOME, replace_o, file_i))
    replace_i = '/usr/lib/hadoop-hdfs/lib/\\*.jar'
    replace_o = '/hadoop/share/hadoop/hdfs/lib/\\*.jar'
    run("sed 's@{0}@{1}{2}@' -i {3}".format(replace_i, DEPLOY_HOME, replace_o, file_i))
    # mapreduce
    replace_i = '/usr/lib/hadoop-mapreduce/\\*.jar'
    replace_o = '/hadoop/share/hadoop/mapreduce/\\*.jar'
    run("sed 's@{0}@{1}{2}@' -i {3}".format(replace_i, DEPLOY_HOME, replace_o, file_i))
    replace_i = '/usr/lib/hadoop-mapreduce/lib/\\*.jar'
    replace_o = '/hadoop/share/hadoop/mapreduce/lib/\\*.jar'
    run("sed 's@{0}@{1}{2}@' -i {3}".format(replace_i, DEPLOY_HOME, replace_o, file_i))
    # yarn
    replace_i = '/usr/lib/hadoop-yarn/\\*.jar'
    replace_o = '/hadoop/share/hadoop/yarn/\\*.jar'
    run("sed 's@{0}@{1}{2}@' -i {3}".format(replace_i, DEPLOY_HOME, replace_o, file_i))
    replace_i = '/usr/lib/hadoop-yarn/lib/\\*.jar'
    replace_o = '/hadoop/share/hadoop/yarn/lib/\\*.jar'
    run("sed 's@{0}@{1}{2}@' -i {3}".format(replace_i, DEPLOY_HOME, replace_o, file_i))

    # 4. install dependencies - hadoop conf dir
    file_i = os.path.join(DEPLOY_HOME, 'sqoop/server/conf/sqoop.properties')
    replace_i = '/etc/hadoop/conf/'
    replace_o = '/opt/bigdata/hadoop/etc/hadoop/'
    run("sed 's@{0}@{1}@' -i {2}".format(replace_i, replace_o, file_i))

    # 5. clean up
    file_i = os.path.join(DEPLOY_HOME, SQOOP2_PKG)
    run('rm {0}'.format(file_i))

def sq22(option):
    """sqoop2 server       => fab seth:2,3 sq22:strat/stop"""
    file_i = os.path.join(DEPLOY_HOME, 'sqoop/bin/sqoop2-server')
    run('{0} {1}'.format(file_i, option))

def sp0():
    """spark uninstall     => fab seth:2,5 sp0"""
    # 0. rm spark
    file_i = os.path.join(DEPLOY_HOME, 'spark')
    run('rm -rf {0}'.format(file_i))

def sp1():
    """spark install       => fab seth:2,5 sp1"""
    # 1. copy package
    file_i = os.path.join(SOFTWARE_HOME, SPARK_PKG)
    file_o = os.path.join(DEPLOY_HOME, SPARK_PKG)
    put(file_i, file_o)

    # 2. unzip
    file_i = os.path.join(DEPLOY_HOME, SPARK_PKG)
    run('tar -zxf {0} -C {1}'.format(file_i, DEPLOY_HOME))

    # 3. rename
    file_i = os.path.join(DEPLOY_HOME, 'spark-1.4.0-bin-hadoop2.6')
    file_o = os.path.join(DEPLOY_HOME, 'spark')
    run('mv {0} {1}'.format(file_i, file_o))

    # 4. clean up
    file_i = os.path.join(DEPLOY_HOME, SPARK_PKG)
    run('rm {0}'.format(file_i))


def sp2(option):
    """spark master        => fab seth:5,5 sp2:start/stop"""
    with settings(host_string='node5'):
        file_i = os.path.join(DEPLOY_HOME, 'spark/sbin/')
        run('{0}{1}-master.sh'.format(file_i, option))

def sp3():
    """spark worker        => fab seth:2,4 sp3"""
    file_i1 = os.path.join(DEPLOY_HOME, 'spark/bin/spark-class')
    file_i2 = 'org.apache.spark.deploy.worker.Worker'
    cmd = 'nohup {0} {1} spark://{2}:7077 >& /dev/null < /dev/null &'
    run(cmd.format(file_i1, file_i2, SPARK_MASTER))

def sp4():
    """spark sparkpi       => fab seth:2,2 sp4"""
    file_i = os.path.join(DEPLOY_HOME, 'spark/bin/spark-submit')
    args = """--class org.apache.spark.examples.SparkPi \
    --master yarn-cluster --num-executors 3 \
    --driver-memory 4g    --executor-memory 2g \
    --executor-cores 1    --queue thequeue {0} \
    10 """.format(os.path.join(DEPLOY_HOME, 'spark/lib/spark-examples-1.4.0-hadoop2.6.0.jar'))
    run('{0} {1}'.format(file_i, args))
