#! *-* coding: utf-8 *-*
"""sqoop import data"""

from fabric.api import env
from fabric.operations import run, put
import os

env.hosts = ['node3']
env.user = 'hduser'
env.password = 'icssda'

MIRROR = 'http://files.grouplens.org/datasets/movielens/'
CMD_GET = 'wget {0}{1} -P {2}'
CMD_MY = ' mysql -usa -psa sqoop < {0}'
# http://ubuntuforums.org/showthread.php?t=1990780
CMD_MYB = ' mysql -usa -psa sqoop --local-infile < {0}'
FABFILE_DIR = '~/Documents/github/fabric/data'
WORKING_DIR = '~/Downloads/'

def setup(user='node3'):
    """set user password        => fab setup"""
    env.user = user
    env.password = 'icssda'

def init0(prefix=WORKING_DIR):
    """get ml-latest.zip        => fab setup init0:prefix"""
    # 1. download test data
    run(CMD_GET.format(MIRROR, 'ml-latest.zip', prefix))

def init1(prefix=WORKING_DIR):
    """unzip ml-latest.zip      => fab setup init1:prefix"""
    # 2. unzip test data
    file_i = os.path.join(prefix, 'ml-latest.zip')
    run('unzip {0} -d {1}'.format(file_i, prefix))

def init2():
    """create table             => fab setup init2"""
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

def init3():
    """bulk insert              => fab setup init3"""
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

def init4():
    """drop table               => fab setup init4"""
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

def myim0():
    """mysql list-databases     => fab myim0"""
    cmd = "sqoop list-databases \
    --connect 'jdbc:mysql://192.168.120.153' \
    --username sa -P"
    run(cmd)

def myim1(database='sqoop'):
    """mysql list-tables        => fab myim1:database"""
    cmd = "sqoop list-tables \
    --connect 'jdbc:mysql://192.168.120.153/{0}' \
    --username sa -P".format(database)
    run(cmd)

def myim2(database='sqoop', table='ratings'):
    """mysql import hdfs        => fab myim2:database,table"""
    cmd = "sqoop import \
    --connect 'jdbc:mysql://192.168.120.153/{0}' \
    --username sa -P --table {1}".format(database, table)
    run(cmd)

def myim3(database='sqoop'):
    """mysql import all to hdfs => fab myim3:database"""
    cmd = "sqoop import-all-tables \
    --connect 'jdbc:mysql://192.168.120.153/{0}' \
    --username sa -P -m 1".format(database)
    run(cmd)

def myim4():
    """mysql import to hbase    => fab myim4"""
    cmd = "sqoop import \
    --connect 'jdbc:sqlserver://192.168.120.151;database=sqoop' \
    --username sa -P --table ratings --hbase-table ratings \
    --column-family info --hbase-row-key user_id,movie_id \
    --hbase-create-table -m 1"
    run(cmd)

def msim0():
    """mssql list-databases     => fab msim0"""
    cmd = "sqoop list-databases \
    --connect 'jdbc:sqlserver://192.168.120.151' \
    --username sa -P"
    run(cmd)

def msim1(database='sqoop'):
    """mssql list-tables        => fab msim1:database"""
    cmd = "sqoop list-tables \
    --connect 'jdbc:sqlserver://192.168.120.151;database={0}' \
    --username sa -P".format(database)
    run(cmd)

def msim2(database='sqoop', table='ratings'):
    """mssql import to hdfs     => fab msim2:database,table"""
    cmd = "sqoop import \
    --connect 'jdbc:sqlserver://192.168.120.151;database={0}' \
    --username sa -P --table {1}".format(database, table)
    run(cmd)

def msim3(database='sqoop'):
    """mssql import all to hdfs => fab msim3:database"""
    cmd = "sqoop import-all-tables \
    --connect 'jdbc:sqlserver://192.168.120.151;database={0}' \
    --username sa -P -m 1".format(database)
    run(cmd)

def msim4():
    """mssql import to hbase    => fab msim4"""
    cmd = "sqoop import \
    --connect 'jdbc:sqlserver://192.168.120.151;database=sqoop' \
    --username sa -P --table ratings --hbase-table ratings \
    --column-family info --hbase-row-key user_id,movie_id \
    --hbase-create-table -m 1"
    run(cmd)

def hdfs0(path='/user/hduser'):
    """hdfs dfs -ls             => fab hdfs0:path"""
    run('hdfs dfs -ls {0}'.format(path))

def hdfs1(path='/user/hduser'):
    """hdfs dfs -ls -R          => fab hdfs1:path"""
    run('hdfs dfs -ls -R {0}'.format(path))

def hdfs3(path='/user/hduser'):
    """hdfs dfs -rm -r          => fab hdfs3:path"""
    run('hdfs dfs -rm -r {0}'.format(path))

def hdfs4():
    """hdfs mv import to fbig   => fab hdfs4"""
    run('hdfs dfs -mkdir fbig')
    run('hdfs dfs -mv /user/hduser/中* fbig')
    run('hdfs dfs -mv /user/hduser/代* fbig')
    run('hdfs dfs -mv /user/hduser/分* fbig')
    run('hdfs dfs -mv /user/hduser/基* fbig')
    run('hdfs dfs -mv /user/hduser/备* fbig')
    run('hdfs dfs -mv /user/hduser/日* fbig')

def hdfs5():
    """hdfs dfs -rm import      => fab hdfs5"""
    run('hdfs dfs -rm -r /user/hduser/中*')
    run('hdfs dfs -rm -r /user/hduser/代*')
    run('hdfs dfs -rm -r /user/hduser/分*')
    run('hdfs dfs -rm -r /user/hduser/基*')
    run('hdfs dfs -rm -r /user/hduser/备*')
    run('hdfs dfs -rm -r /user/hduser/日*')
