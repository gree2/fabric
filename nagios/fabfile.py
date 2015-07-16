#! *-* coding: utf-8 *-*
"""deploy nagios"""

from fabric.api import cd, env
from fabric.operations import put, run, sudo
import os

env.hosts = ['node5']
env.user = 'node5'
env.password = 'icssda'

FABFILE_DIR = '~/Documents/github/fabric/nagios'
WORKING_DIR = '~/Downloads'
DEPLOY_HOME = '/usr/local'

NAGIOS_VER = '4.0.8'
NAGIOS_PKG = 'nagios-{0}.tar.gz'.format(NAGIOS_VER)
NAGIOS_PLUGINS_VER = '2.0.3'
NAGIOS_PLUGINS_PKG = 'nagios-plugins-{0}.tar.gz'.format(NAGIOS_PLUGINS_VER)

def sete(user='hduser'):
    """set user password       => fab sete"""
    env.user = user
    env.password = 'icssda'

def setn0():
    """install prerequisites   => fab setn0"""
    sudo('apt-get install build-essential libgd2-xpm-dev apache2-utils')

def setn1():
    """nagios user and group   => fab setn1"""
    sudo('useradd -m nagios')
    sudo('passwd nagios')
    sudo('groupadd nagcmd')
    sudo('usermod -a -G nagcmd nagios')
    sudo('usermod -a -G nagcmd www-data')

def setn2(prefix=WORKING_DIR):
    """nagios downloads        => fab setn2"""
    # download nagios
    base_url = 'http://prdownloads.sourceforge.net/sourceforge/nagios/{0}'
    run('wget {0} -P {1}'.format(base_url.format(NAGIOS_PKG), prefix))
    # download nagios plugins
    base_url = 'http://nagios-plugins.org/download/{0}'
    run('wget {0} -P {1}'.format(base_url.format(NAGIOS_PLUGINS_PKG), prefix))

def setn3():
    """install nagios          => fab setn3"""
    # 1. copy package
    file_i = os.path.join(WORKING_DIR, NAGIOS_PKG)
    file_o = os.path.join(DEPLOY_HOME, NAGIOS_PKG)
    put(file_i, file_o)

    # 2. unzip
    file_i = os.path.join(DEPLOY_HOME, NAGIOS_PKG)
    run('tar -zxf {0} -C {1}'.format(file_i, DEPLOY_HOME))

    # 3. rename
    file_i = os.path.join(DEPLOY_HOME, 'nagios-{0}'.format(NAGIOS_VER))
    file_o = os.path.join(DEPLOY_HOME, 'nagios')
    run('mv {0} {1}'.format(file_i, file_o))

    with cd(file_o):
        # 1. compile and install nagios
        sudo('./configure --with-command-group=nagcmd')
        sudo('make all')
        sudo('make install')
        sudo('make install-init')
        sudo('make install-config')
        sudo('make install-commandmode')
        # 2. install nagios web interface
        # sudo('make install-webconf')
        file_i = 'sample-config/httpd.conf'
        file_o = '/etc/apache2/sites-enabled/nagios.conf'
        sudo('/usr/bin/install -c -m 644 {0} {1}'.format(file_i, file_o))

    # create a `nagiosadmin` account
    # for logging into nagios webui
    sudo('htpasswd -c /usr/local/nagios/etc/htpasswd.users nagiosadmin')
    sudo('service apache2 restart')

def setn4():
    """install nagios plugins  => fab setn4"""
    # 1. copy package
    file_i = os.path.join(WORKING_DIR, NAGIOS_PLUGINS_PKG)
    file_o = os.path.join(DEPLOY_HOME, NAGIOS_PLUGINS_PKG)
    put(file_i, file_o)

    # 2. unzip
    file_i = os.path.join(DEPLOY_HOME, NAGIOS_PLUGINS_PKG)
    run('tar -zxf {0} -C {1}'.format(file_i, DEPLOY_HOME))

    # 3. rename
    file_i = os.path.join(DEPLOY_HOME, 'nagios-plugins-{0}'.format(NAGIOS_PLUGINS_VER))
    with cd(file_i):
        # compile and install
        sudo('./configure --with-nagios-user=nagios --with-nagios-group=nagios')
        sudo('make')
        sudo('make install')
