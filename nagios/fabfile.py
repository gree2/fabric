#! *-* coding: utf-8 *-*
"""deploy nagios"""

from fabric.api import cd, env, settings
from fabric.operations import put, run, sudo
import os

env.hosts = ['node5']
env.user = 'node5'
env.password = 'icssda'

FABFILE_DIR = '~/Documents/github/fabric/nagios'
WORKING_DIR = '~/Downloads'
DEPLOY_HOME = '/usr/local'
DEPLOY_PLUGIN_HOME = '/usr/lib/nagios/plugins'
APACHE2_CFG_DIR = '/etc/apache2'
APACHE2_SITES_ENABLED = APACHE2_CFG_DIR + '/sites-enabled'
CLIENT_CFG_DIR = '/etc/nagios'

NAGIOS_SERVER = 'node5@node5'
NAGIOS_CLIENT = ["node%d" % c for c in range(int(2), int(5) + 1)]

NAGIOS_VER = '4.0.8'
NAGIOS_PKG = 'nagios-{0}.tar.gz'.format(NAGIOS_VER)
NAGIOS_PLUGINS_VER = '2.0.3'
NAGIOS_PLUGINS_PKG = 'nagios-plugins-{0}.tar.gz'.format(NAGIOS_PLUGINS_VER)
NAGIOSGRAPH_VER = '1.5.2'
NAGIOSGRAPH_PKG = 'nagiosgraph-{0}.tar.gz'.format(NAGIOSGRAPH_VER)


def setec():
    """env: clean up nagios install        => fab setec"""
    with cd(WORKING_DIR):
        # run('ls nagios*')
        sudo('rm -rf nagios*')

def seteh(start='2', stop='5'):
    """env: set env hosts                  => fab seteh"""
    env.hosts = ["node{0}@node{0}".format(i) for i in range(int(start), int(stop) + 1)]
    password = ['icssda'] * (int(stop) - int(start) + 1)
    # http://stackoverflow.com/questions/209840/map-two-lists-into-a-dictionary-in-python
    env.passwords = dict(zip(env.hosts, password))
    print env.passwords

def setep(user='hduser'):
    """env: set env user password          => fab setep"""
    env.user = user
    env.password = 'icssda'

def seter():
    """env: restart apache2 nagios         => fab seter"""
    sudo('service apache2 restart')
    sudo('service nagios restart')

def setc00():
    """client: add epel-release repo       => fab setc00"""
    sudo('yum install epel-release')

def setc01(option='debian'):
    """client: install nrpe nagios-plugins => fab setc01:debian/other"""
    if 'debian' == option:
        sudo('apt-get install nagios-nrpe-server nagios-plugins nagios-nrpe-plugin')
    else:
        sudo('yum install nrpe nagios-plugins-all openssl')

def setc02():
    """client: copy nrpe server conf       => fab setc02"""
    file_i = os.path.join(FABFILE_DIR, 'client/nrpe.cfg')
    file_o = os.path.join(CLIENT_CFG_DIR, 'nrpe.cfg')
    put(file_i, file_o, use_sudo=True)

def setc03(platform='debian'):
    """client: nagios nrpe service restart => fab setc03:centos6/centos7/debian"""
    if 'debian' == platform:
        sudo('/etc/init.d/nagios-nrpe-server restart')
    elif 'centos6' == platform:
        sudo('systemctl start nrpe')
        sudo('chkconfig nrpe on')
    else:
        sudo('service nrpe start')
        sudo('chkconfig nrpe on')

def setc04():
    """client: copy nrpe.cfg commands      => fab seteh:2,5 setc04"""
    # 1. copy nrpe.cfg to nrpe daemon => /etc/nagios/nrpe.cfg
    file_i = os.path.join(FABFILE_DIR, 'nrpe/nrpe.cfg')
    file_o = os.path.join(CLIENT_CFG_DIR, 'nrpe.cfg')
    put(file_i, file_o, use_sudo=True)
    # 2. copy plugins => /usr/lib/nagios/plugins
    # 2.1 check_net_transfer
    file_i = os.path.join(FABFILE_DIR, 'plugins/check_net_transfer')
    file_o = os.path.join(DEPLOY_PLUGIN_HOME, 'check_net_transfer')
    put(file_i, file_o, use_sudo=True)
    sudo('chown root:root {0}'.format(file_o))
    sudo('chmod +x {0}'.format(file_o))
    # 2.2 check_bandwidth
    file_i = os.path.join(FABFILE_DIR, 'plugins/check_bandwidth.sh')
    file_o = os.path.join(DEPLOY_PLUGIN_HOME, 'check_bandwidth.sh')
    put(file_i, file_o, use_sudo=True)
    sudo('chown root:root {0}'.format(file_o))
    sudo('chmod +x {0}'.format(file_o))

    # 3. restart nrpe-server on all nodes
    sudo('/etc/init.d/nagios-nrpe-server restart')
    # 4. copy node?.cfg to nagios server => /usr/local/nagios/etc/servers
    with settings(host_string=NAGIOS_SERVER):
        # 1. copy objects => /usr/local/nagios/etc/objects
        file_i = os.path.join(FABFILE_DIR, 'objects/commands.cfg')
        file_o = os.path.join(DEPLOY_HOME, 'nagios/etc/objects/commands.cfg')
        put(file_i, file_o, use_sudo=True)
        sudo('chown root:root {0}'.format(file_o))
        sudo('chmod +x {0}'.format(file_o))

        # 2. copy servers => /usr/local/nagios/etc/servers
        for end in range(2, 6):
            file_i = os.path.join(FABFILE_DIR, 'server/node{0}.cfg'.format(end))
            file_o = os.path.join(DEPLOY_HOME, 'nagios/etc/servers/node{0}.cfg'.format(end))
            put(file_i, file_o, use_sudo=True)

def setg00():
    """nagiosgraph: copy software          => fab setg00"""
    # 1. copy package
    file_i = os.path.join(WORKING_DIR, NAGIOSGRAPH_PKG)
    file_o = os.path.join(WORKING_DIR, NAGIOSGRAPH_PKG)
    put(file_i, file_o)
    # 2. unzip
    file_i = os.path.join(WORKING_DIR, NAGIOSGRAPH_PKG)
    run('tar -zxf {0} -C {1}'.format(file_i, WORKING_DIR))

def setg01():
    """nagiosgraph: prerequisites check    => fab setg01"""
    file_i = os.path.join(WORKING_DIR, 'nagiosgraph-{0}'.format(NAGIOSGRAPH_VER))
    with cd(file_i):
        sudo('./install.pl --check-prereq')

def setg02():
    """nagiosgraph: prerequisites install  => fab setg02"""
    sudo('apt-get install librrds-perl libgd-gd2-perl')
    print 'install Nagios::Config'
    sudo('perl -MCPAN -e shell')

def setg03():
    """nagiosgraph: installation           => fab setg03"""
    file_i = os.path.join(WORKING_DIR, 'nagiosgraph-{0}'.format(NAGIOSGRAPH_VER))
    with cd(file_i):
        print 'Modify the Nagios configuration? [n] y'
        print 'Modify the Apache configuration? [n] y'
        sudo('./install.pl --layout standalone --prefix /usr/local/nagiosgraph')

def setg04():
    """nagiosgraph: copy config, restart   => fab setg04"""
    # 1. copy apache2.conf      => /etc/apache2
    file_i = os.path.join(FABFILE_DIR, 'nagiosgraph/apache2.conf')
    file_o = os.path.join(APACHE2_CFG_DIR, 'apache2.conf')
    put(file_i, file_o)
    # 2. copy common-header.ssi => /usr/local/nagios/share/ssi
    file_i = os.path.join(FABFILE_DIR, 'nagiosgraph/common-header.ssi')
    file_o = os.path.join(DEPLOY_HOME, 'nagios/share/ssi', 'common-header.ssi')
    put(file_i, file_o)
    # 3. copy localhost.cfg     => /usr/local/nagios/etc/objects
    file_i = os.path.join(FABFILE_DIR, 'nagiosgraph/localhost.cfg')
    file_o = os.path.join(DEPLOY_HOME, 'nagios/etc/objects', 'localhost.cfg')
    put(file_i, file_o)
    # 4. copy side.php          => /usr/local/nagios/share
    file_i = os.path.join(FABFILE_DIR, 'nagiosgraph/side.php')
    file_o = os.path.join(DEPLOY_HOME, 'nagios/share', 'side.php')
    put(file_i, file_o)

def setg05():
    """nagiosgraph: cleanup                => fab setg05"""
    with cd(WORKING_DIR):
        sudo('rm -rf nagiosgraph*')

def sets00():
    """server: install prerequisites       => fab sets00"""
    sudo('apt-get install build-essential libgd2-xpm-dev apache2-utils')

def sets01():
    """server: create user and group       => fab sets01"""
    sudo('useradd -m nagios')
    sudo('passwd nagios')
    sudo('groupadd nagcmd')
    sudo('usermod -a -G nagcmd nagios')
    sudo('usermod -a -G nagcmd www-data')

def sets02():
    """server: install nagios core         => fab sets02"""
    # 1. copy package
    file_i = os.path.join(WORKING_DIR, NAGIOS_PKG)
    file_o = os.path.join(WORKING_DIR, NAGIOS_PKG)
    put(file_i, file_o)
    # 2. unzip
    file_i = os.path.join(WORKING_DIR, NAGIOS_PKG)
    run('tar -zxf {0} -C {1}'.format(file_i, WORKING_DIR))
    # 3. compile and install
    file_i = os.path.join(WORKING_DIR, 'nagioscore-nagios-{0}'.format(NAGIOS_VER))
    with cd(file_i):
        sudo('./configure --with-command-group=nagcmd')
        sudo('make all')
        sudo('make install')
        sudo('make install-init')
        sudo('make install-config')
        sudo('make install-commandmode')

def sets03(option='1'):
    """server: install nagios webui        => fab sets03:0/1"""
    # 1. compile and install
    file_i = os.path.join(WORKING_DIR, 'nagioscore-nagios-{0}'.format(NAGIOS_VER))
    with cd(file_i):
        if '0' == option:
            sudo('make install-webconf')
        else:
            file_i = 'sample-config/httpd.conf'
            file_o = '/etc/apache2/sites-enabled/nagios.conf'
            sudo('/usr/bin/install -c -m 644 {0} {1}'.format(file_i, file_o))

def sets04():
    """server: create webui account        => fab sets04"""
    # create `nagiosadmin` account for logging into nagios webui
    sudo('htpasswd -c /usr/local/nagios/etc/htpasswd.users nagiosadmin')
    sudo('service apache2 restart')

def sets05():
    """server: copy server conf files      => fab sets05"""
    # 1. contacts.cfg
    file_i = os.path.join(FABFILE_DIR, 'server/contacts.cfg')
    file_o = os.path.join(DEPLOY_HOME, 'nagios/etc/objects/contacts.cfg')
    put(file_i, file_o, use_sudo=True)
    # 2. nagios.conf
    file_i = os.path.join(FABFILE_DIR, 'server/nagios.conf')
    file_o = os.path.join(APACHE2_SITES_ENABLED, 'nagios.conf')
    put(file_i, file_o, use_sudo=True)

def sets06():
    """server: install nagios plugins      => fab sets06"""
    # 1. copy package
    file_i = os.path.join(WORKING_DIR, NAGIOS_PLUGINS_PKG)
    file_o = os.path.join(WORKING_DIR, NAGIOS_PLUGINS_PKG)
    put(file_i, file_o)

    # 2. unzip
    file_i = os.path.join(WORKING_DIR, NAGIOS_PLUGINS_PKG)
    run('tar -zxf {0} -C {1}'.format(file_i, WORKING_DIR))
    # 3. compile and install
    file_i = os.path.join(WORKING_DIR, 'nagios-plugins-{0}'.format(NAGIOS_PLUGINS_VER))
    with cd(file_i):
        sudo('./configure --with-nagios-user=nagios --with-nagios-group=nagios --with-openssl')
        sudo('make')
        sudo('make install')

def sets07():
    """server: enable apache modules       => fab sets07"""
    sudo('a2enmod rewrite')
    sudo('a2enmod cgi')
    sudo('service apache2 restart')

def sets08():
    """server: check nagios conf syntax    => fab sets08"""
    sudo('/usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg')

def sets09(option='restart'):
    """server: nagios service              => fab sets09:start/stop/restart"""
    sudo('service nagios {0}'.format(option))

def sets10():
    """server: nagios autostart            => fab sets10"""
    sudo('ln -s /etc/init.d/nagios /etc/rcS.d/S99nagios')
