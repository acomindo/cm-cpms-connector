import json
from unittest import mock
from unittest import TestCase

from requests.exceptions import HTTPError

from cpms import CpmsConnector
from . import mock_response


with open('cpms/tests/config.json') as f:
    config = json.load(f)
token = '05fa7a3605074d41b919ad9e10bdbda2'


class TestToken(TestCase):

    @mock.patch('requests.post')
    def test_success(self, mock_post):
        mock_resp = mock_response(
            status_code=200,
            json_data={
                "token": {
                    "username": config['username'],
                    "token_id": "05fa7a3605074d41b919ad9e10bdbda2",
                    "expires_at": "2018-02-27T15:05:36.477914Z"
                }
            }
        )
        mock_post.return_value = mock_resp

        cpmsconn = CpmsConnector(config)
        self.assertIsNotNone(cpmsconn.token)
        self.assertEqual(token, cpmsconn.token)

    @mock.patch('requests.post')
    def test_unauthorize(self, mock_post):
        mock_resp = mock_response(
            status_code=401,
            raise_for_status=HTTPError('Unauthorize access')
        )
        mock_post.return_value = mock_resp

        with self.assertRaises(HTTPError):
            CpmsConnector(config)
