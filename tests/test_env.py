'''
Test ENV
'''
from tests.helper import *


@ddt
class TestENV(TestCase):

    def setUp(self):
        pass

    @mock.patch.dict(os.environ, env)
    def test_env(self):
        print(os.getenv('DIR_DOWNLOAD'))