#! coding: utf-8
'''dummy spout'''

from pyleus.storm import Spout


class DummySpout(Spout):
    '''dummy spout'''

    OUTPUT_FIELDS = ['sentence', 'name']

    def next_tuple(self):
        '''next_tuple'''
        self.emit(("This is a sentence.", "spout",))

if __name__ == '__main__':
    DummySpout().run()
