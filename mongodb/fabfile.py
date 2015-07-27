#! *-* coding: utf-8 *-*
"""deploy mongodb"""

from fabric.api import env
from fabric.operations import sudo

env.hosts = ['node4@node4']
env.user = 'node4'
env.password = 'icssda'

FABFILE_DIR = '~/Documents/github/fabric/mongodb'
WORKING_DIR = '~/Downloads'
MONGODB_CFG_FIR = '/etc/mongodb'

def sethp(start='2', stop='5'):
    """env: set hosts             => fab sethp"""
    env.hosts = ["node{0}@node{0}".format(i) for i in range(int(start), int(stop) + 1)]
    password = ['icssda'] * (int(stop) - int(start) + 1)
    # http://stackoverflow.com/questions/209840/map-two-lists-into-a-dictionary-in-python
    env.passwords = dict(zip(env.hosts, password))
    # print env.passwords

def setup(user='hduser'):
    """env: set user password     => fab setup"""
    env.user = user
    env.password = 'icssda'

def set0():
    """switch back to upstart     => fab set0"""
    # http://www.answee.com/8a5a9f9b/mongodb-2-6-does-not-start-on-ubuntu-15-04
    # ubuntu 15.04 advances the default init system
    # from `upstart` to `systemd`
    # starting mongodb 3.0 with systemd not work
    sudo('apt-get install upstart-sysv')

def set1():
    """add key add list reload db => fab set1"""
    # 1. import public key
    sudo('apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10')
    # 2. create a list file for mongodb
    # replace `"$(lsb_release -sc)"` with `trusty`
    sudo('echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list')
    # sudo('echo "deb http://repo.mongodb.org/apt/ubuntu wheezy/mongodb-org/3.0 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list')
    # 3. reload local package database
    sudo('apt-get update')

def set2():
    """install gmetad             => fab set2"""
    sudo('apt-get install -y mongodb-org')
    # sudo('apt-get install --reinstall -y mongodb-org')

def set3(option='restart'):
    """service mongodb            => fab set3:start/stop/restart"""
    if 'start' == option:
        sudo('service mongod {0}'.format(option))
    elif 'stop' == option:
        sudo('service mongod {0}'.format(option))
    elif 'restart' == option:
        sudo('service mongod {0}'.format(option))
    else:
        print 'do nothing'

def set4():
    """rm mongodb                 => fab set4"""
    # http://askubuntu.com/questions/617097/mongodb-2-6-does-not-start-on-ubuntu-15-04
    # 1. stop mongodb
    sudo('service mongod stop')
    # 2. remove package
    sudo('apt-get purge mongodb-org*')
    # 3. remove data directories
    sudo('rm -r /var/log/mongodb')
    sudo('rm -r /var/lib/mongodb')
