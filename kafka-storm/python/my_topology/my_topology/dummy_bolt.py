#! coding: utf-8
'''dummy bolt'''

from pyleus.storm import SimpleBolt


class DummyBolt(SimpleBolt):
    '''dummy bolt'''

    OUTPUT_FIELDS = ['sentence']

    def process_tuple(self, tup):
        '''process_tuple'''
        sentence, name = tup.values
        new_sentence = "{0} says, \"{1}\"".format(name, sentence)
        self.emit((new_sentence,), anchors=[tup])


if __name__ == '__main__':
    DummyBolt().run()
