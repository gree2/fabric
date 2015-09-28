#! *-* coding: utf-8 *-*
"""deploy hadoop ecosystem"""

from fabric.api import env, settings
from fabric.operations import run, put, sudo
import os

env.user = 'node'
env.password = 'node'

APP_HOME = '/opt/app'
DEPLOY_HOME = '/opt'
CONF_HOME = '~/Documents/github/fabric/kafka-storm'
SOFTWARE_HOME = '~/Downloads/software'

# zookeeper
ZOOKEEPER_CFG = 'zoo.cfg'
ZOOKEEPER_PKG = 'zookeeper-3.4.6.tar.gz'

KAFKA_CFG = 'server.properties'
KAFKA_PKG = 'kafka_2.11-0.8.2.1.tgz'

STORM_CFG = 'storm.yaml'
STORM_PKG = 'apache-storm-0.9.5.tar.gz'

def sete(start=1, stop=3):
    """set user hosts      => fab sete:1,3"""
    env.user = 'node'
    env.password = 'node'
    env.hosts = ["node%d" % i for i in range(int(start), int(stop) + 1)]

def setw():
    '''mkdir deploy dir    => fab sete:1,3 setw'''
    sudo('rm -rf %s' % APP_HOME)
    sudo('mkdir -p %s' % APP_HOME)
    sudo('chown node.node -R %s' % DEPLOY_HOME)

def setc(option):
    '''config kafka storm  => sete:1,3 setc:home/work'''
    # 1. config kafka
    with settings(host_string=env.host):
        # copy config
        config = '{0}/server{1}.properties'.format(option, str(env.host)[-1])
        file_i = os.path.join(CONF_HOME, 'kafka/{0}'.format(config))
        file_o = os.path.join(DEPLOY_HOME, 'kafka/config/', KAFKA_CFG)
        put(file_i, file_o)

    # 2. config storm
    config = 'storm/{0}/{1}'.format(option, STORM_CFG)
    file_i = os.path.join(CONF_HOME, config)
    file_o = os.path.join(DEPLOY_HOME, 'storm/conf/', STORM_CFG)
    put(file_i, file_o)

def zk0():
    """zookeeper uninstall => fab sete:1,3 zk0"""
    # 0. rm zookeeper
    file_i = os.path.join(APP_HOME, 'zookeeper')
    run('rm -rf {0}'.format(file_i))
    file_i = os.path.join(DEPLOY_HOME, 'zookeeper')
    run('rm -rf {0}'.format(file_i))

def zk1():
    """zookeeper install   => fab sete:1,3 zk1"""
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
    file_i = os.path.join(CONF_HOME, 'zookeeper', ZOOKEEPER_CFG)
    file_o = os.path.join(DEPLOY_HOME, 'zookeeper/conf', ZOOKEEPER_CFG)
    put(file_i, file_o)

    # 5. mkdir and set `myid`
    file_i = os.path.join(APP_HOME, 'zookeeper')
    run('mkdir -p {0}'.format(file_i))
    with settings(host_string=env.host):
        run('mkdir -p {0}/zookeeper/data'.format(APP_HOME))
        run('echo {0} > {1}/zookeeper/data/myid'.format(str(env.host)[-1], APP_HOME))

    # 6. clean up
    file_i = os.path.join(DEPLOY_HOME, ZOOKEEPER_PKG)
    run('rm {0}'.format(file_i))

def zk2(option):
    """zookeeper service   => fab sete:1,3 zk2:start/stop/status"""
    file_i = os.path.join(DEPLOY_HOME, 'zookeeper/bin/zkServer.sh {0}'.format(option))
    run(file_i)

def zk3():
    """zookeeper status    => fab sete:1,3 zk3"""
    run('echo status | nc {0} 2181'.format(env.host))

def kf0():
    '''kafka uninstall     => fab sete:1,3 kf0'''
    file_i = os.path.join(APP_HOME, 'kafka')
    run('rm -rf {0}'.format(file_i))
    file_i = os.path.join(DEPLOY_HOME, 'kafka')
    run('rm -rf {0}'.format(file_i))

def kf1():
    """kafka install       => fab sete:1,3 kf1"""
    # 1. copy package
    file_i = os.path.join(SOFTWARE_HOME, KAFKA_PKG)
    file_o = os.path.join(DEPLOY_HOME, KAFKA_PKG)
    put(file_i, file_o)

    # 2. unzip
    file_i = os.path.join(DEPLOY_HOME, KAFKA_PKG)
    run('tar -zxf {0} -C {1}'.format(file_i, DEPLOY_HOME))

    # 3. rename
    file_i = os.path.join(DEPLOY_HOME, 'kafka_2.11-0.8.2.1')
    file_o = os.path.join(DEPLOY_HOME, 'kafka')
    run('mv {0} {1}'.format(file_i, file_o))

    # 4. mkdir `log` and copy `cfg`
    # for i in range(1, 4):
    with settings(host_string=env.host):
        # mkdir log
        run('mkdir -p {0}/kafka/log{1}'.format(APP_HOME, str(env.host)[-1]))
        # copy cfg
        file_i = os.path.join(CONF_HOME, 'kafka/server{0}.properties'.format(str(env.host)[-1]))
        file_o = os.path.join(DEPLOY_HOME, 'kafka/config/', KAFKA_CFG)
        put(file_i, file_o)

    # 5. clean up
    file_i = os.path.join(DEPLOY_HOME, KAFKA_PKG)
    run('rm {0}'.format(file_i))

def kf2():
    '''kafka service       => fab sete:1,1 kf2 sete:2,2 kf2 sete:3,3 kf2'''
    # on node1-3
    # $ env JMX_PORT=10002 bin/kafka-server-start.sh config/server.properties
    # $ env JMX_PORT=10003 bin/kafka-server-start.sh config/server.properties
    # $ env JMX_PORT=10004 bin/kafka-server-start.sh config/server.properties
    if env.host == 'node1':
        file_env = 'env JMX_PORT=10002'
    elif env.host == 'node2':
        file_env = 'env JMX_PORT=10003'
    else:
        file_env = 'env JMX_PORT=10004'
    file_i1 = os.path.join(DEPLOY_HOME, 'kafka/bin/kafka-server-start.sh')
    file_i2 = os.path.join(DEPLOY_HOME, 'kafka/config/server.properties')
    cmd = 'nohup {} {} {} &> /dev/null &'.format(file_env, file_i1, file_i2)
    run(cmd, pty=False)

def st0():
    '''storm uninstall     => fab sete:1,3 st0'''
    file_i = os.path.join(APP_HOME, 'storm')
    run('rm -rf {0}'.format(file_i))
    file_i = os.path.join(DEPLOY_HOME, 'storm')
    run('rm -rf {0}'.format(file_i))

def st1():
    """storm install       => fab sete:1,3 st1"""
    # 1. copy package
    file_i = os.path.join(SOFTWARE_HOME, STORM_PKG)
    file_o = os.path.join(DEPLOY_HOME, STORM_PKG)
    put(file_i, file_o)

    # 2. unzip
    file_i = os.path.join(DEPLOY_HOME, STORM_PKG)
    run('tar -zxf {0} -C {1}'.format(file_i, DEPLOY_HOME))

    # 3. rename
    file_i = os.path.join(DEPLOY_HOME, 'apache-storm-0.9.5')
    file_o = os.path.join(DEPLOY_HOME, 'storm')
    run('mv {0} {1}'.format(file_i, file_o))

    # 4. mkdir `log` and copy `cfg`
    # mkdir log
    run('mkdir -p {0}/storm/'.format(APP_HOME))
    # copy cfg
    file_i = os.path.join(CONF_HOME, 'storm/storm.yaml')
    file_o = os.path.join(DEPLOY_HOME, 'storm/conf/', STORM_CFG)
    put(file_i, file_o)

    # 5. clean up
    file_i = os.path.join(DEPLOY_HOME, STORM_PKG)
    run('rm {0}'.format(file_i))

def st2(option):
    '''storm nimbus        => fab sete:1,1 st2:nimbus sete:1,3 st2:supervisor sete:1,1 st2:ui'''
    # on node1/node1-3/node1
    # $ bin/storm nimbus     >/dev/null 2>&1 &
    # $ bin/storm supervisor >/dev/null 2>&1 &
    # $ bin/storm ui         >/dev/null 2>&1 &
    file_i = os.path.join(DEPLOY_HOME, 'storm/bin/storm')
    cmd = 'nohup {} {} &> /dev/null &'.format(file_i, option)
    run(cmd, pty=False)

def jps():
    '''jps                 => fab sete:1,3 jps'''
    run('jps')
