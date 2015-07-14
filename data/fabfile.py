#! *-* coding: utf-8 *-*
"""deploy hadoop ecosystem"""

from fabric.api import env
from fabric.operations import run, put
import os

env.hosts = ['node3']
env.user = 'node3'
env.password = 'icssda'

MIRROR = 'http://files.grouplens.org/datasets/movielens/'
CMD_GET = 'wget {0}{1} -P {2}'
CMD_MY = ' mysql -usa -psa sqoop < {0}'
# http://ubuntuforums.org/showthread.php?t=1990780
CMD_MYB = ' mysql -usa -psa sqoop --local-infile < {0}'
FABFILE_DIR = '~/Documents/github/fabric/data'
WORKING_DIR = '~/Downloads/'

def sete(user='hduser'):
    """set user password        => fab sete"""
    env.user = user
    env.password = 'icssda'

def it0(prefix=WORKING_DIR):
    """get ml-latest.zip        => fab it0:prefix"""
    # 1. download test data
    run(CMD_GET.format(MIRROR, 'ml-latest.zip', prefix))

def it1(prefix=WORKING_DIR):
    """unzip ml-latest.zip      => fab it1:prefix"""
    # 2. unzip test data
    file_i = os.path.join(prefix, 'ml-latest.zip')
    run('unzip {0} -d {1}'.format(file_i, prefix))

def it2():
    """create table             => fab it2"""
    file_name = 'create.sql'
    # 1. put file
    file_i = os.path.join(FABFILE_DIR, file_name)
    file_o = os.path.join(WORKING_DIR, file_name)
    put(file_i, file_o)
    # 2. run cmd
    file_i = os.path.join(WORKING_DIR, file_name)
    run(CMD_MY.format(file_i))
    # 3. clean up
    file_i = os.path.join(WORKING_DIR, file_name)
    run('rm {0}'.format(file_i))

def it3():
    """bulk insert              => fab it3"""
    file_name = 'bulk.mysql.sql'
    # 1. put file
    file_i = os.path.join(FABFILE_DIR, file_name)
    file_o = os.path.join(WORKING_DIR, file_name)
    put(file_i, file_o)
    # 2. run cmd
    file_i = os.path.join(WORKING_DIR, file_name)
    run(CMD_MYB.format(file_i))
    # 3. clean up
    file_i = os.path.join(WORKING_DIR, file_name)
    run('rm {0}'.format(file_i))

def it4():
    """drop table               => fab it4"""
    file_name = 'drop.sql'
    # 1. put file
    file_i = os.path.join(FABFILE_DIR, file_name)
    file_o = os.path.join(WORKING_DIR, file_name)
    put(file_i, file_o)
    # 2. run cmd
    file_i = os.path.join(WORKING_DIR, file_name)
    run(CMD_MY.format(file_i))
    # 3. clean up
    file_i = os.path.join(WORKING_DIR, file_name)
    run('rm {0}'.format(file_i))

def my0():
    """mysql list-databases     => fab sete my0"""
    cmd = "sqoop list-databases \
    --connect 'jdbc:mysql://192.168.120.153' \
    --username sa -P"
    run(cmd)

def my1():
    """mysql list-tables        => fab sete my1"""
    cmd = "sqoop list-tables \
    --connect 'jdbc:mysql://192.168.120.153/sqoop' \
    --username sa -P"
    run(cmd)

def my2(table='ratings'):
    """mysql import hdfs        => fab sete my2:table"""
    cmd = "sqoop import \
    --connect 'jdbc:mysql://192.168.120.153/sqoop' \
    --username sa -P --table {0}".format(table)
    run(cmd)

def my3():
    """mysql import all to hdfs => fab sete my3"""
    cmd = "sqoop import-all-tables \
    --connect 'jdbc:mysql://192.168.120.153/sqoop' \
    --username sa -P -m 1"
    run(cmd)

def my4():
    """mysql import to hbase    => fab sete my4"""
    cmd = "sqoop import \
    --connect 'jdbc:sqlserver://192.168.120.151;database=sqoop' \
    --username sa -P --table ratings --hbase-table ratings \
    --column-family info --hbase-row-key user_id,movie_id \
    --hbase-create-table -m 1"
    run(cmd)

def ms0():
    """mssql list-databases     => fab sete ms0"""
    cmd = "sqoop list-databases \
    --connect 'jdbc:sqlserver://192.168.120.151' \
    --username sa -P"
    run(cmd)

def ms1():
    """mssql list-tables        => fab sete ms1"""
    cmd = "sqoop list-tables \
    --connect 'jdbc:sqlserver://192.168.120.151;database=sqoop' \
    --username sa -P"
    run(cmd)

def ms2(table='ratings'):
    """mssql import to hdfs     => fab sete ms2:table"""
    cmd = "sqoop import \
    --connect 'jdbc:sqlserver://192.168.120.151;database=sqoop' \
    --username sa -P --table {0}".format(table)
    run(cmd)

def ms3(database='sqoop'):
    """mssql import all to hdfs => fab sete ms3:database"""
    cmd = "sqoop import-all-tables \
    --connect 'jdbc:sqlserver://192.168.120.151;database={0}' \
    --username sa -P -m 1".format(database)
    run(cmd)

def ms4():
    """mssql import to hbase    => fab sete ms4"""
    cmd = "sqoop import \
    --connect 'jdbc:sqlserver://192.168.120.151;database=sqoop' \
    --username sa -P --table ratings --hbase-table ratings \
    --column-family info --hbase-row-key user_id,movie_id \
    --hbase-create-table -m 1"
    run(cmd)

def hd0(table):
    """hdfs dfs -ls             => fab sete hd0:table"""
    run('hdfs dfs -ls /user/hduser/{0}'.format(table))

def hd1():
    """hdfs dfs -ls -R          => fab sete hd1"""
    run('hdfs dfs -ls -R /user/hduser')

def hd2():
    """hdfs dfs -cat | head     => fab sete hd2"""
    run('hdfs dfs -cat /user/hduser/基础表_贷款业务_额度使用情况信息表/part-m-00000 | head')

def hd3(table):
    """hdfs dfs -rm -r          => fab sete hd3:table"""
    run('hdfs dfs -rm -r /user/hduser/{0}'.format(table))
