#! *-* coding: utf-8 *-*
"""deploy hadoop ecosystem"""

from fabric.api import env
from fabric.operations import run

env.hosts = ['localhost']
env.user = 'node3'
env.password = 'icssda'

MIRROR = 'http://files.grouplens.org/datasets/movielens/'
CMD = 'wget {0}{1} -P {2}'
WORKING_DIR = '~/Downloads/'

FILES = [
    'ml-1m-README.txt',
    'ml-1m.zip',
    'ml-1m.zip.md5',
    'ml-10m-README.html',
    'ml-10m.zip',
    'ml-10m.zip.md5',
    'ml-20m-README.html',
    'ml-20m.zip',
    'ml-20m.zip.md5',
    'ml-100k-README.txt',
    'ml-100k.zip',
    'ml-100k.zip.md5',
    'ml-latest-README.html',
    'ml-latest-small-README.html',
    'ml-latest-small.zip',
    'ml-latest-small.zip.md5',
    'ml-latest.zip',
    'ml-latest.zip.md5'
    ]

def get00(prefix=WORKING_DIR):
    """get ml-1m.zip   => fab get00:prefix"""
    run(CMD.format(MIRROR, 'ml-1m.zip', prefix))
