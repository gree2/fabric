#! coding: utf-8
'''write word count to redis/log'''

import logging
import redis

from pyleus.storm import SimpleBolt

RDS = redis.Redis('localhost')
LOG = logging.getLogger('log_results')

class LogResultsBolt(SimpleBolt):
    '''write word count to redis/log'''

    def process_tuple(self, tup):
        word, count = tup.values
        RDS.zadd('word_count', word, count)
        LOG.debug("%s: %d", word, count)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='/tmp/word_count_results.log',
        format="%(message)s",
        filemode='a',
    )

    LogResultsBolt().run()
