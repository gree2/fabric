#! *-* coding: utf-8 *-*
"""deploy zoomdata"""

from fabric.api import cd, env
from fabric.operations import put, run, sudo
import os

env.hosts = ['node4@node4']
env.user = 'node4'
env.password = 'icssda'

FABFILE_DIR = '~/Documents/github/fabric/zoomdata'
WORKING_DIR = '~/Downloads'

ZOOMDATA_CFG_DIR = '/etc/zoomdata'
ZOOMDATA_PKG = 'zoomdata_1.5.0-sr1_amd64.deb'

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

def set1():
    """add mongo user             => fab set1"""
    run('mongo zoom --eval "db.createUser({user:\'zoomadmin\', pwd:\'icssda\', roles:[\'readWrite\']});"')

def set2():
    """upload deb and install     => fab set2"""
    file_i = os.path.join(WORKING_DIR, ZOOMDATA_PKG)
    file_o = os.path.join(WORKING_DIR, ZOOMDATA_PKG)
    put(file_i, file_o)
    with cd(WORKING_DIR):
        sudo('dpkg -i {0}'.format(ZOOMDATA_PKG))
        run('rm {0}'.format(ZOOMDATA_PKG))

def set3():
    """config zoomdata            => fab set3"""
    file_i = os.path.join(FABFILE_DIR, 'zoomdata.conf')
    file_o = os.path.join(ZOOMDATA_CFG_DIR, 'zoomdata.conf')
    put(file_i, file_o, use_sudo=True)
    # sudo('iptables -I INPUT 1 -i eth0 -p tcp --dport 8443 -j ACCEPT')
    # sudo('iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 443 -j DNAT --to-destination :8443')
    # sudo('service iptables save')
