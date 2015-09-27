#! *-* coding: utf-8 *-*
"""deploy hadoop ecosystem"""

from fabric.api import env, settings
from fabric.operations import run, put
import os

APP_HOME = '/opt/app'
DEPLOY_HOME = '/opt'
CONF_HOME = 'E:\\hobby\\github\\fabric\\kafka-storm'
SOFTWARE_HOME = 'E:\\Downloads\\apache'

# zookeeper
ZOOKEEPER_CFG = 'zoo.cfg'
ZOOKEEPER_PKG = 'zookeeper-3.4.6.tar.gz'

env.user = 'node'
env.password = 'node'

def sete(start=1, stop=3):
    """set user hosts      => fab sete:1,3"""
    env.user = 'node'
    env.hosts = ["node%d" % i for i in range(int(start), int(stop) + 1)]

def zk0():
    """zookeeper uninstall => fab sete:2,4 zk0"""
    # 0. rm zookeeper
    file_i = os.path.join(DEPLOY_HOME, 'zookeeper')
    run('rm -rf {0}'.format(file_i))
    file_i = os.path.join(APP_HOME, 'zookeeper')
    run('rm -rf {0}'.format(file_i))

def zk1():
    """zookeeper install   => fab sete:2,4 zk1"""
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
    for i in range(2, 5):
        with settings(host_string='node{0}'.format(i)):
            run('mkdir -p {0}/zookeeper/data'.format(APP_HOME))
            run('echo {0} > {1}/zookeeper/data/myid'.format(i, APP_HOME))

    # 6. clean up
    file_i = os.path.join(DEPLOY_HOME, ZOOKEEPER_PKG)
    run('rm {0}'.format(file_i))

def zk2(option):
    """zookeeper service   => fab sete:2,4 zk2:start/stop/status"""
    file_i = os.path.join(DEPLOY_HOME, 'zookeeper/bin/zkServer.sh {0}'.format(option))
    run(file_i)

def zk3():
    """zookeeper status    => fab sete:2,4 zk3"""
    run('echo status | nc {0} 2181'.format(env.host))
