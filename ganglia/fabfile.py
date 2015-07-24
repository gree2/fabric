#! *-* coding: utf-8 *-*
"""deploy ganglia"""

from fabric.api import cd, env, settings
from fabric.operations import put, run, sudo
import os

env.hosts = ['node5']
env.user = 'node5'
env.password = 'icssda'

FABFILE_DIR = '~/Documents/github/fabric/ganglia'
WORKING_DIR = '~/Downloads'
GANGLIA_CFG_FIR = '/etc/ganglia'
APACHE2_CFG_DIR = '/etc/apache2'
APACHE2_SITES_ENABLED = APACHE2_CFG_DIR + '/sites-enabled'

GANGLIA_MUTE = 'node5@node5'
GANGLIA_DEAF = ["node{0}@node{0}".format(c) for c in range(int(2), int(4) + 1)]

GANGLIA_VER = '3.7.1'
GANGLIA_PKG = 'ganglia-{0}.tar.gz'.format(GANGLIA_VER)

GANGLIA_WEB_VER = '3.7.0'
GANGLIA_WEB_PKG = 'ganglia-web-{0}.tar.gz'.format(GANGLIA_WEB_VER)

def setc():
    """env: clean up              => fab setc"""
    # 0. clearup working dir
    with cd(WORKING_DIR):
        sudo('rm -rf ganglia*')

def seth(start='2', stop='5'):
    """env: set hosts             => fab seth"""
    env.hosts = ["node{0}@node{0}".format(i) for i in range(int(start), int(stop) + 1)]
    password = ['icssda'] * (int(stop) - int(start) + 1)
    # http://stackoverflow.com/questions/209840/map-two-lists-into-a-dictionary-in-python
    env.passwords = dict(zip(env.hosts, password))
    # print env.passwords

def setp(user='hduser'):
    """env: set user password     => fab setp"""
    env.user = user
    env.password = 'icssda'

def setr():
    """env: service restart       => fab setr"""
    sudo('service apache2 restart')

def set1(option='debian'):
    """install gmond              => fab seth:2,5 set1:debian/rpm-search/rpm-5/rpm-6"""
    if 'debian' == option:
        sudo('apt-get install ganglia-monitor')
    elif 'rpm-search' == option:
        sudo('yum search ganglia-gmond')
    elif 'epel5' == option:
        url = 'http://mirror.ancl.hawaii.edu/linux/epel/5/i386/epel-release-5-4.noarch.rpm'
        sudo('rpm -Uvh {0}'.format(url))
        sudo('yum install ganglia-gmond')
    elif 'epel6' == option:
        url = 'http://mirror.chpc.utah.edu/pub/epel/6/i386/epel-release-6-7.noarch.rpm'
        sudo('rpm -Uvh {0}'.format(url))
        sudo('yum install ganglia-gmond')
    else:
        print 'do nothing'

def set2(option='debian'):
    """install gmetad             => fab seth:2,5 set2:debian/rpm/mac"""
    if 'debian' == option:
        sudo('apt-get install gmetad')
    elif 'rpm' == option:
        sudo('yum install ganglia-gmetad')
    elif 'mac' == option:
        sudo('port install libconfuse pkgconfig pcre apr rrdtool')
        print 'please download extract patch and install manually'
    else:
        print 'do nothing'

def set3(option='debian'):
    """install gweb               => fab set3:debian/rpm"""
    if 'debian' == option:
        sudo('apt-get install apache2 php5 php5-json')
    elif 'rpm' == option:
        sudo('yum install httpd php')
    # 1. copy package
    file_i = os.path.join(WORKING_DIR, GANGLIA_WEB_PKG)
    file_o = os.path.join(WORKING_DIR, GANGLIA_WEB_PKG)
    put(file_i, file_o)
    # 2. unzip
    file_i = os.path.join(WORKING_DIR, GANGLIA_WEB_PKG)
    run('tar -zxf {0} -C {1}'.format(file_i, WORKING_DIR))
    # 3. compile and install
    file_i = os.path.join(WORKING_DIR, 'ganglia-web-{0}'.format(GANGLIA_WEB_VER))
    with cd(file_i):
        file_i = os.path.join(WORKING_DIR, 'gweb/MakeFile')
        file_o = os.path.join(WORKING_DIR, 'ganglia-web-{0}'.format(GANGLIA_WEB_VER), 'MakeFile')
        put(file_i, file_o)
        sudo('make install')

def set4():
    """config ganglia             => fab set4"""
    with settings(host_string=GANGLIA_MUTE):
        pass

def set5(option='master'):
    """install all                => fab seth:5,5 set5 seth:2,4 set5:nodes"""
    common_packages = 'ganglia-monitor ganglia-monitor-python'
    prereq_packages = 'gmetad rrdtool ganglia-webfrontend'
    if 'master' == option:
        sudo('apt-get -y install {0} {1}'.format(common_packages, prereq_packages))
    elif 'nodes' == option:
        sudo('apt-get -y install {0}'.format(common_packages))
    else:
        print 'do nothing'

def set6(option='master'):
    """config ganglia             => fab seth:5,5 set6 seth:2,4 set6:nodes"""
    if 'master' == option:
        # cp => /etc/apache2/sites-enabled/ganglia.conf
        file_i = os.path.join(FABFILE_DIR, 'gweb/ganglia.conf')
        file_o = os.path.join(APACHE2_SITES_ENABLED, 'ganglia.conf')
        put(file_i, file_o, use_sudo=True)
        # cp => /etc/ganglia/gmetad.conf
        file_i = os.path.join(FABFILE_DIR, 'gmetad/gmetad.conf')
        file_o = os.path.join(GANGLIA_CFG_FIR, 'gmetad.conf')
        put(file_i, file_o, use_sudo=True)
        # cp => /etc/ganglia/gmond.conf
        file_i = os.path.join(FABFILE_DIR, 'gmond/master/gmond.conf')
        file_o = os.path.join(GANGLIA_CFG_FIR, 'gmond.conf')
        put(file_i, file_o, use_sudo=True)
    else:
        # cp => /etc/ganglia/gmond.conf
        file_i = os.path.join(FABFILE_DIR, 'gmond/nodes/gmond.conf')
        file_o = os.path.join(GANGLIA_CFG_FIR, 'gmond.conf')
        put(file_i, file_o, use_sudo=True)

def set7(option='master'):
    """service ganglia apache2    => fab seth:5,5 set7 seth:2,4 set7:nodes"""
    if 'master' == option:
        sudo('service ganglia-monitor restart')
        sudo('service gmetad restart')
        sudo('service apache2 restart')
    else:
        sudo('service ganglia-monitor restart')
