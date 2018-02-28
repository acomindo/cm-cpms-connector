import requests
from urllib.parse import urlparse, urlencode
from json import JSONDecodeError
from requests.exceptions import HTTPError


def validate_response(response):
    """
    raise exception if error response occurred
    """

    r = response
    try:
        r.raise_for_status()
    except HTTPError as e:
        message = dict(status_code=r.status_code, exception=e)

        try:
            response = r.json()
            message['response'] = response
        except JSONDecodeError as e:
            message['response'] = r.content

        raise HTTPError(message)


class CpmsConnector:
    """The CpmsConnector object allow you communicate through
    cpms between application.
    """

    ORDER_STATUS = ('NEW', 'IN_PROGRESS', 'COMPLETED', 'CANCELED', 'ERROR')

    def __init__(self, config):
        """initialize with config
        config(dict): must supply username, api_key, api_url
        """
        self.username = config['username']
        self.api_key = config['api_key']
        self.api_url = config['api_url']
        self._token = None
        self._set_token()

    @property
    def _fulfillment_url(self):
        netloc = f'fulfillment.{urlparse(self.api_url).netloc}'
        return urlparse(self.api_url)._replace(netloc=netloc).geturl()

    def _update_headers(self, token):
        self.headers = {
            'X-Subject-Token': token
        }

    @property
    def token(self):
        return self._token

    def _set_token(self):
        path = '/identity/token'

        payload = {
            "auth":
                {
                    "apiKeyCredentials":
                    {
                        "username": self.username,
                        "apiKey": self.api_key
                    }
                }
        }

        url = urlparse(self.api_url)._replace(path=path).geturl()
        r = requests.post(url, json=payload)
        validate_response(r)
        token = r.json()['token']['token_id']
        self._update_headers(token)
        self._token = token
