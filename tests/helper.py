from copy import deepcopy
from datetime import datetime
import json
import os
import pandas as pd

from ddt import ddt, data, unpack
from unittest import TestCase, mock, skip


from dotenv import load_dotenv
load_dotenv()
env = {
    'DIR_BIN': os.environ.get('DIR_BIN', ''),
    'DIR_CACHE': os.environ.get('DIR_CACHE', ''),
    'DIR_DOWNLOAD': os.environ.get('DIR_DOWNLOAD', ''),
}

# store example data for unit and local testing
DIR_DATA = os.path.join(os.path.dirname(__file__), 'data')