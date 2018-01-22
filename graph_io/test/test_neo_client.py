from graph_io import SimpleNodeClient, NodeClient
from unittest.mock import patch, MagicMock, MagicProxy
from unittest import TestCase

from graph_io.test import MODE, INTEGRATION
from graph_io.test.helpers import clever_patch_method


class Tests(TestCase):
    def test_instantiation(self):
        with clever_patch_method(NodeClient, 'get_client') as mock_get, \
                clever_patch_method(NodeClient, 'close_client') as mock_close:
            print('bar')
            with SimpleNodeClient() as c:
                print(c)
                assert c
            mock_get.assert_called_once()
            mock_close.assert_called_once()

    def test_call_cypher(self):
        # TODO: implement me
        pass