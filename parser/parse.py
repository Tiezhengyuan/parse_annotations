'''
process gene/DATA
'''
from copy import deepcopy
import itertools
import os
import sys
import json
from typing import Iterable, Callable
import pandas as pd

from utils.commons import Commons
from utils.file import File
from utils.dir import Dir
from utils.utils import Utils
from utils.jtxt import Jtxt
from utils.handle_json import HandleJson

# print(f"{}.", file=sys.stdout)
class Parse(Commons):
    def __init__(self):
        super(Parse, self).__init__()
    
