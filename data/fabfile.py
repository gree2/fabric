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

def my00(prefix=WORKING_DIR):
    """get ml-latest.zip   => fab my00:prefix"""
    # 1. download test data
    run(CMD_GET.format(MIRROR, 'ml-latest.zip', prefix))

def my01(prefix=WORKING_DIR):
    """unzip ml-latest.zip => fab my01:prefix"""
    # 2. unzip test data
    file_i = os.path.join(prefix, 'ml-latest.zip')
    run('unzip {0} -d {1}'.format(file_i, prefix))

def my02():
    """create table        => fab my02"""
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

def my03():
    """buld insert         => fab my03"""
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

def my04():
    """drop table          => fab my04"""
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
