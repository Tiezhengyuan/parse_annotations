'''
Test class 
'''
from unittest import TestCase, mock, skip
from ddt import ddt, data, unpack
import os, sys

from pAnnot.connector.connect_expasy import ConnectExPASy

env = {
    'DIR_CACHE': "H:\\cache",
    'DIR_DOWNLOAD': "H:\\download",
}

@ddt
class TestKEGG(TestCase):

    @mock.patch.dict(os.environ, env)
    def setUp(self):
        self.c = ConnectExPASy()

    @skip
    def test_download_data(self):
        res = self.c.download_data()

