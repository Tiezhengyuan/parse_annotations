#!/usr/bin/python3
"""
create map of references ~ <other annotation terms>
"""
import sys
from utils.commons import Commons

class App(Commons):
    def __init__(self, ref_term:str):
        super(App, self).__init__()
        self.ref_term = ref_term

    def process(self):
        print(self.term)
        pass

if __name__ == '__main__':
    ref_term = sys.argv[1]
    App(ref_term).process()
    print('great!!!!')