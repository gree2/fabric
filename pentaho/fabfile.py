#! *-* coding: utf-8 *-*
'''deploy pentaho ecosystem'''

from fabric.api import env
from fabric.operations import run, put
import os

env.hosts = ['pentaho']
env.user = 'node'
env.password = 'node'
env.shell = '/bin/sh -c'

APP_HOME = '/opt/app'
DEPLOY_HOME = '/home/node'
CONF_HOME = '~/Documents/github/fabric/pentaho'
SOFTWARE_HOME = '~/Downloads/software'

# deploy 5.4
# PBI_PKG = 'biserver-ce-5.4.0.1-130.zip'
# PBI_DIR = 'biserver-ce-5.4'

# deploy 6.0
PBI_PKG = 'biserver-ce-6.0.0.0-353.zip'
PBI_DIR = 'biserver-ce-6.0'

CONNECTOR_MYSQL = 'mysql-connector-java-5.1.35-bin.jar'

def pbi0():
    '''biserver uninstall  => fab pbi0'''
    file_i = os.path.join(DEPLOY_HOME, PBI_DIR)
    run('rm -rf {0}'.format(file_i))

def pbi1():
    '''biserver install    => fab pbi1'''
    # 1. copy package
    file_i = os.path.join(SOFTWARE_HOME, 'pentaho', PBI_PKG)
    file_o = os.path.join(DEPLOY_HOME, PBI_PKG)
    put(file_i, file_o)

    # 2. unzip
    file_i = os.path.join(DEPLOY_HOME, PBI_PKG)
    run('unzip -q {0}'.format(file_i))

    # 3. rename
    file_i = os.path.join(DEPLOY_HOME, 'biserver-ce')
    file_o = os.path.join(DEPLOY_HOME, PBI_DIR)
    run('mv {0} {1}'.format(file_i, file_o))

    # 4. copy connector
    file_i = os.path.join(SOFTWARE_HOME, CONNECTOR_MYSQL)
    file_o = os.path.join(DEPLOY_HOME, PBI_DIR, 'tomcat/lib', CONNECTOR_MYSQL)
    put(file_i, file_o)

    # 5. clean up
    file_i = os.path.join(DEPLOY_HOME, PBI_PKG)
    run('rm {0}'.format(file_i))

def pbi2(option):
    '''biserver service    => fab pbi2:start/stop'''
    file_i = os.path.join(DEPLOY_HOME, PBI_DIR, '{0}-pentaho.sh'.format(option))
    # with cd(file_i):
    run(file_i)

def pbi3():
    '''netstat -antp       => fab pbi3'''
    run('netstat -antp')
