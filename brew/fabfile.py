#! *-* coding: utf-8 *-*
"""reconfig formula after brew upgrade"""

from fabric.api import env
from fabric.operations import put, run
import os


LOCAL_DIR = '/usr/local'
CELLAR_DIR = '/usr/local/Cellar'
SOFTWARE_DIR = '/Users/hqlgree2/Downloads/software'
CONNECTOR_MYSQL = 'mysql-connector-java-5.1.38-bin.jar'

env.hosts = ['localhost']


def check():
    """check /usr/local                => fab check"""
    # ln -s /usr/local/Cellar/apache-drill/version /usr/local/apache-drill
    run('ls -l {}'.format(LOCAL_DIR))

def apache_drill(version):
    """config /usr/local/apache-drill  => fab apache_drill:'1.4.0'"""
    # ln -s /usr/local/Cellar/apache-drill/version /usr/local/apache-drill
    link_from = os.path.join(CELLAR_DIR, 'apache-drill', version)
    link_to = os.path.join(LOCAL_DIR, 'apache-drill')
    run('rm -f {}'.format(link_to))
    run('ln -s {} {}'.format(link_from, link_to))
    # copy config files
    cfg_from = './apache-drill'
    cfg_to = os.path.join(link_to, 'libexec/conf')
    for cfg in os.listdir(cfg_from):
        file_i = os.path.join(cfg_from, cfg)
        file_o = os.path.join(cfg_to, cfg)
        put(file_i, file_o)

def apache_spark(version):
    """config /usr/local/apache-spark  => fab apache_spark:'1.6.0'"""
    # ln -s /usr/local/Cellar/apache-drill/version /usr/local/apache-drill
    link_from = os.path.join(CELLAR_DIR, 'apache-spark', version)
    link_to = os.path.join(LOCAL_DIR, 'apache-spark')
    run('rm -f {}'.format(link_to))
    run('ln -s {} {}'.format(link_from, link_to))
    # copy config files
    cfg_from = './apache-spark'
    cfg_to = os.path.join(link_to, 'libexec/conf')
    for cfg in os.listdir(cfg_from):
        file_i = os.path.join(cfg_from, cfg)
        file_o = os.path.join(cfg_to, cfg)
        put(file_i, file_o)


def hadoop(version, use_yarn):
    """config /usr/local/hadoop        => fab hadoop:'2.7.1',True"""
    # ln -s /usr/local/Cellar/hadoop/version /usr/local/hadoop
    link_from = os.path.join(CELLAR_DIR, 'hadoop', version)
    link_to = os.path.join(LOCAL_DIR, 'hadoop')
    run('rm -f {}'.format(link_to))
    run('ln -s {} {}'.format(link_from, link_to))
    # copy config files
    cfg_from = './hadoop/' + ('yarn' if use_yarn else 'mapred')
    cfg_to = os.path.join(link_to, 'libexec/etc/hadoop')
    for cfg in os.listdir(cfg_from):
        file_i = os.path.join(cfg_from, cfg)
        file_o = os.path.join(cfg_to, cfg)
        put(file_i, file_o)

def hbase(version):
    """config /usr/local/hbase         => fab hbase:'1.1.2'"""
    # ln -s /usr/local/Cellar/hbase/version /usr/local/hbase
    link_from = os.path.join(CELLAR_DIR, 'hbase', version)
    link_to = os.path.join(LOCAL_DIR, 'hbase')
    run('rm -f {}'.format(link_to))
    run('ln -s {} {}'.format(link_from, link_to))
    # copy config files
    cfg_from = './hbase/'
    cfg_to = os.path.join(link_to, 'libexec/conf')
    for cfg in os.listdir(cfg_from):
        file_i = os.path.join(cfg_from, cfg)
        file_o = os.path.join(cfg_to, cfg)
        put(file_i, file_o)

def hive(version):
    """config /usr/local/hive          => fab hive:'1.2.1'"""
    # ln -s /usr/local/Cellar/hive/version /usr/local/hive
    link_from = os.path.join(CELLAR_DIR, 'hive', version)
    link_to = os.path.join(LOCAL_DIR, 'hive')
    run('rm -f {}'.format(link_to))
    run('ln -s {} {}'.format(link_from, link_to))
    # copy config files
    cfg_from = './hive/'
    cfg_to = os.path.join(link_to, 'libexec/conf')
    for cfg in os.listdir(cfg_from):
        file_i = os.path.join(cfg_from, cfg)
        file_o = os.path.join(cfg_to, cfg)
        put(file_i, file_o)
    # copy connector(mysql)
    copy_to = os.path.join(link_to, 'libexec/lib', 'mysql.*.jar')
    run('rm -f {}'.format(copy_to))
    copy_form = os.path.join(SOFTWARE_DIR, CONNECTOR_MYSQL)
    copy_to = os.path.join(link_to, 'libexec/lib', CONNECTOR_MYSQL)
    put(copy_form, copy_to)

def kafka(version):
    """config /usr/local/kafka         => fab kafka:'0.8.2.2'"""
    # ln -s /usr/local/Cellar/kafka/version /usr/local/kafka
    link_from = os.path.join(CELLAR_DIR, 'kafka', version)
    link_to = os.path.join(LOCAL_DIR, 'kafka')
    run('rm -f {}'.format(link_to))
    run('ln -s {} {}'.format(link_from, link_to))
    # copy config files
    cfg_from = './kafka/'
    cfg_to = os.path.join(link_to, 'libexec/conf')
    for cfg in os.listdir(cfg_from):
        file_i = os.path.join(cfg_from, cfg)
        file_o = os.path.join(cfg_to, cfg)
        put(file_i, file_o)

def solr(version):
    """config /usr/local/solr          => fab solr:'5.4.0'"""
    # ln -s /usr/local/Cellar/solr/version /usr/local/solr
    link_from = os.path.join(CELLAR_DIR, 'solr', version)
    link_to = os.path.join(LOCAL_DIR, 'solr')
    run('rm -f {}'.format(link_to))
    run('ln -s {} {}'.format(link_from, link_to))

def sqoop(version):
    """config /usr/local/sqoop         => fab sqoop:'1.4.6'"""
    # ln -s /usr/local/Cellar/sqoop/version /usr/local/sqoop
    link_from = os.path.join(CELLAR_DIR, 'sqoop', version)
    link_to = os.path.join(LOCAL_DIR, 'sqoop')
    run('rm -f {}'.format(link_to))
    run('ln -s {} {}'.format(link_from, link_to))

def tomcat(version):
    """config /usr/local/tomcat        => fab tomcat:'8.0.30'"""
    # ln -s /usr/local/Cellar/tomcat/version /usr/local/tomcat
    link_from = os.path.join(CELLAR_DIR, 'tomcat', version)
    link_to = os.path.join(LOCAL_DIR, 'tomcat')
    run('rm -f {}'.format(link_to))
    run('ln -s {} {}'.format(link_from, link_to))

def zookeeper(version):
    """config /usr/local/zookeeper     => fab zookeeper:'3.4.7'"""
    # ln -s /usr/local/Cellar/zookeeper/version /usr/local/zookeeper
    link_from = os.path.join(CELLAR_DIR, 'zookeeper', version)
    link_to = os.path.join(LOCAL_DIR, 'zookeeper')
    run('rm -f {}'.format(link_to))
    run('ln -s {} {}'.format(link_from, link_to))
    # copy config files
    cfg_from = './zookeeper/'
    cfg_to = os.path.join(LOCAL_DIR, 'etc/zookeeper')
    for cfg in os.listdir(cfg_from):
        file_i = os.path.join(cfg_from, cfg)
        file_o = os.path.join(cfg_to, cfg)
        put(file_i, file_o)
