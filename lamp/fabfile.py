#! *-* coding: utf-8 *-*
"""deploy lamp"""

from fabric.api import env
from fabric.operations import put, sudo
import os

env.hosts = ['node5']
env.user = 'node5'
env.password = 'icssda'

WORKING_DIR = '~/Documents/github/fabric/lamp'
APACHE2_WWW = '/var/www/html'

def sete(user='hduser'):
    """set env          => fab sete"""
    env.user = user
    env.password = 'icssda'

def seta0():
    """apache install   => fab seta0"""
    sudo('apt-get update')
    sudo('apt-get install apache2')

def seta1(option):
    """apache service   => fab seta1:start/stop/restart"""
    sudo('/etc/init.d/apache2 {0}'.format(option))

def seta2(option):
    """apache autostart => fab seta2:y/n"""
    if 'y' == option:
        sudo('update-rc.d -f apache2 remove')
    else:
        sudo('update-rc.d apache2 defaults')

def setm0():
    """mysql install    => fab setm0"""
    sudo('apt-get update')
    sudo('apt-get install mysql-server mysql-client')

def setm1():
    """mysql uninstall  => fab setm1"""
    sudo('systemctl stop mysql')
    sudo('apt-get remove --purge mysql-server mysql-client mysql-common')
    sudo('apt-get autoremove')
    sudo('apt-get autoclean')
    sudo('rm -rf /var/lib/mysql')
    sudo('rm -rf /etc/mysql')

def setm2(options):
    """mysql service    => fab setm2:start/stop/status"""
    sudo('systemctl {0} mysql'.format(options))

def setp0():
    """php install      => fab setp0"""
    sudo('apt-get install php5 php5-mysql libapache2-mod-php5')

def setp1():
    """php test         => fab setp1"""
    file_i = os.path.join(WORKING_DIR, 'php/test.php')
    file_o = os.path.join(APACHE2_WWW, 'test.php')
    put(file_i, file_o, use_sudo=True)
    print 'restarting apache...'
    sudo('service apache2 restart')
    print 'please visit this site => http://{0}/test.php'.format(env.host)
