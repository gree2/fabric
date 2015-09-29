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
    '''config kafka storm  => fab sete:1,3 setc:home/work'''
    # 1 config kafka
    with settings(host_string=env.host):
        # 1.1 config kafka
        config = '{0}/server{1}.properties'.format(option, str(env.host)[-1])
        file_i = os.path.join(CONF_HOME, 'kafka/{0}'.format(config))
        file_o = os.path.join(DEPLOY_HOME, 'kafka/config/', KAFKA_CFG)
        put(file_i, file_o)
        # 1.2 kafka log dir
        run('rm -rf {0}/kafka/'.format(APP_HOME))
        run('mkdir -p {0}/kafka/log{1}'.format(APP_HOME, str(env.host)[-1]))

    # 2.1 config storm
    config = 'storm/{0}/{1}'.format(option, STORM_CFG)
    file_i = os.path.join(CONF_HOME, config)
    file_o = os.path.join(DEPLOY_HOME, 'storm/conf/', STORM_CFG)
    put(file_i, file_o)

    # 2.2 storm data dir
    run('rm -rf {0}/storm/'.format(APP_HOME))
    run('mkdir -p {0}/storm/'.format(APP_HOME))

    # 3.1 config zookeeper
    config = 'zookeeper/{0}/{1}'.format(option, ZOOKEEPER_CFG)
    file_i = os.path.join(CONF_HOME, config)
    file_o = os.path.join(DEPLOY_HOME, 'zookeeper/conf', ZOOKEEPER_CFG)
    put(file_i, file_o)

    # 3.2 zookeeper data dir
    with settings(host_string=env.host):
        run('rm -rf {0}/zookeeper/'.format(APP_HOME))
        run('mkdir -p {0}/zookeeper/data/'.format(APP_HOME))
        run('mkdir -p {0}/zookeeper/log/'.format(APP_HOME))
        run('echo {0} > {1}/zookeeper/data/myid'.format(str(env.host)[-1], APP_HOME))

def jps():
    '''jps                 => fab sete:1,3 jps'''
    run('jps')

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
        run('mkdir -p {0}/zookeeper/log'.format(APP_HOME))
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

def kf2(option):
    '''kafka service       => fab sete:1,3 kf2:start/stop'''
    if option == 'start':
        with settings(host_string=env.host):
            file_env = 'env JMX_PORT=1000{0}'.format(int(str(env.host)[-1]) + 1)
            file_i1 = os.path.join(DEPLOY_HOME, 'kafka/bin/kafka-server-start.sh')
            file_i2 = os.path.join(DEPLOY_HOME, 'kafka/config/server.properties')
            cmd = 'nohup {} {} {} &> /dev/null &'.format(file_env, file_i1, file_i2)
            run(cmd, pty=False)
    else:
        # kill `jps | grep "Kafka" | cut -d " " -f 1`
        run('kill -9 `jps | grep "Kafka" | cut -d " " -f 1`')
        run('jps')

def kf3(option):
    '''kafka topic         => fab sete:1,1 kf3:create/list/describe'''
    # bin/kafka-topics.sh --zookeeper 192.168.1.151:2181 --list
    # bin/kafka-topics.sh --zookeeper 192.168.1.151:2181 --describe --topic topic1
    file_i1 = os.path.join(DEPLOY_HOME, 'kafka/bin/kafka-topics.sh')
    file_i2 = '--zookeeper 192.168.1.151:2181'
    if option == 'create':
        file_i3 = '--create --topic topic1 --partitions 3 --replication-factor 2'
    elif option == 'describe':
        file_i3 = '--describe --topic topic1'
    else:
        file_i3 = '--list'
    cmd = '{} {} {}'.format(file_i1, file_i2, file_i3)
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

    # 4. mkdir `data` and copy `cfg`
    # mkdir data
    run('mkdir -p {0}/storm/'.format(APP_HOME))
    # copy cfg
    file_i = os.path.join(CONF_HOME, 'storm/storm.yaml')
    file_o = os.path.join(DEPLOY_HOME, 'storm/conf/', STORM_CFG)
    put(file_i, file_o)

    # 5. clean up
    file_i = os.path.join(DEPLOY_HOME, STORM_PKG)
    run('rm {0}'.format(file_i))

def st2(option):
    '''storm service       => fab sete:1,3 st2:start/stop'''
    file_i = os.path.join(DEPLOY_HOME, 'storm/bin/storm')
    cmd = 'nohup {} {} &> /dev/null &'
    if option == 'start':
        # node1: nimbus+ui
        if 'node1' == env.host:
            run(cmd.format(file_i, 'nimbus'), pty=False)
            run(cmd.format(file_i, 'ui'), pty=False)
        # node1-3: supervisor
        run(cmd.format(file_i, 'supervisor'), pty=False)
    else:
        # node1: nimbus+ui
        if 'node1' == env.host:
            run('kill -9 `jps | grep "core" | cut -d " " -f 1`')
            run('kill -9 `jps | grep "nimbus" | cut -d " " -f 1`')
        # node1-3: supervisor
        run('kill -9 `jps | grep "supervisor" | cut -d " " -f 1`')

def sv0():
    '''start all service   => fab sete:1,3 zk2:start kf2:start st2:start'''
    pass

def sv1():
    '''stop  all service   => fab sete:1,3 st2:stop kf2:stop zk2:stop'''
    pass
