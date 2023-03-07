#!/usr/bin/python3
"""
retrieve data according to terms specifiecd and organize them into data in jtxt format.
"""
import sys
from utils.commons import Commons

class App(Commons):
    def __init__(self, field:str, term:str):
        super(App, self).__init__()
        self.field = field
        self.term = term

    def process(self):
        print(self.field, self.term)
        pass

if __name__ == '__main__':
    field, term = sys.argv[1], sys.argv[2]
    App(field, term).process()
    print(field, term)