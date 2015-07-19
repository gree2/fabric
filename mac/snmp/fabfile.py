#! *-* coding: utf-8 *-*
"""activate snmp on mac os"""

from fabric.api import env
from fabric.operations import sudo
import os

FABFILE_DIR = '~/Documents/github/fabric/mac/snmp'
DEPLOY_HOME = '/etc/snmp'

env.hosts = ['localhost']

def set0(option='0'):
    """cp snmpd.conf           => fab set0:0/1/2"""
    if '0' == option:
        file_i = os.path.join(FABFILE_DIR, 'snmpd.conf.0')
    elif '1' == option:
        file_i = os.path.join(FABFILE_DIR, 'snmpd.conf.1')
    else:
        file_i = os.path.join(FABFILE_DIR, 'snmpd.conf.2')
    file_o = os.path.join(DEPLOY_HOME, 'snmpd.conf')
    sudo('cp {0} {1}'.format(file_i, file_o))

def set1(option='1'):
    """snmp service            => fab set1:[0-stop]/[1-start]"""
    plist = '/System/Library/LaunchDaemons/org.net-snmp.snmpd.plist'
    if '1' == option:
        sudo('launchctl load -w {0}'.format(plist))
    else:
        sudo('launchctl unload -w {0}'.format(plist))

def set2():
    """snmpconf -g basic_setup => fab set2"""
    # https://www.mikesel.info/snmp-os-x/
    sudo('sudo snmpconf -g basic_setup')

def set3():
    """snmpconf -i             => fab set3"""
    # https://support.apple.com/kb/TA20884?locale=zh_CN&viewlocale=en_US
    sudo('snmpconf -i')
