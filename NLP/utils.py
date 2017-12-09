import re
import random

def process(row):
    message = '{0}'.format(' '.join(row[3:]))
    message = message[1:]
    message = message.lower()
    return re.sub(r'([^\s\w]|_)+', '', message)

class MySentences(object):
    def __init__(self, file_path,randomize=False):
        self.file_path = file_path
        self.randomize = randomize
 
    def __iter__(self):
        f = open(self.file_path).readlines()
        if self.randomize:
            random.shuffle(f)

        for line in f:
            to_yield = filter(None,line[:-1].split(' '))
            if(len(to_yield)>1):
                yield to_yield
