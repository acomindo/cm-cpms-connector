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

    def get_order(self, channel_id, order_id):
        """retrieve single order of sales order

        Args:
            url(str): url for retrieval sales order
        """
        path = f'/channel/{channel_id}/order/{order_id}'
        url = urlparse(self._fulfillment_url)._replace(path=path).geturl()
        r = requests.get(url, headers=self.headers)
        validate_response(r)
        return r.json()

    def get_orders_status(self, channel_id=None, partner_id=None, list_id=None,
                          since=None, order_status=None):
        """Get list order status of sales order

        Args:
            channel_id(str): channel_id of cpms
            partner_id(str): merchant/partner id of cpms
            list_id(list): list of order id
            since(str): ISO 8601 format eg. 2015-06-18T10:30:40Z
            order_status(str): (NEW, IN_PROGRESS, COMPLETED, CANCELED, ERROR)

        Returns:
            list: all orders
        """

        if order_status and order_status not in self.ORDER_STATUS:
            raise ValueError(
                'invalid order_status eg. '
                '(NEW, IN_PROGRESS, COMPLETED, CANCELED, ERROR)'
            )

        url = urlparse(self._fulfillment_url)

        # make sure channel_id or partner_id being supply
        if channel_id:
            path = f'/channel/{channel_id}'

        elif partner_id:
            path = f'/partner/{partner_id}'

        else:
            raise ValueError(
                'must supply either channel_id or partner_id args')

        # append sales-order-status path
        path += '/sales-order-status'

        # make sure list_id or since being supply
        if list_id:
            if len(list_id) > 10:
                raise ValueError('list_id can\'t be more than 10 length')
            path += '/id'
            query_string = {'id': list_id}

        elif since:
            query_string = {'id': list_id}
            if order_status in self.ORDER_STATUS:
                query_string.update({'orderStatus': order_status})
        else:
            raise ValueError('must supply either list_id or since args')

        query_string = urlencode(query_string, doseq=True)
        url = url._replace(path=path, query=query_string).geturl()

        r = requests.get(url, headers=self.headers)
        validate_response(r)
        orders = r.json()
        next_url = r.links['next']['url'] if 'next' in r.links else None
        return orders, next_url

    def create_order(self, channel_id, order_id, payload):
        """create order to acommerce (CPMS)

        Args:
            channel_id(str): channel_id of cpms
            order_id(str): order_id of merchant or partner
            payload(dict): order body

        Returns:
            response or exception
        """
        path = f'/channel/{channel_id}/order/{order_id}'
        url = urlparse(self._fulfillment_url)._replace(path=path).geturl()

        r = requests.put(url=url, json=payload, headers=self.headers)
        validate_response(r)

        return {
            'code': r.status_code,
            'message': 'Order has been successfully created'
        }

    def get_stocks(self, channel_id, partner_id, since):
        """Get list stock of partner from specifics channel/marketplace

        Args:
            channel_id(str): channel_id cpms
            partner_id(str): partner/merchant id
            since(str): ISO 8601 format eg. 2015-06-18T10:30:40Z

        Returns (list): list of stock

        """
        path = f'/channel/{channel_id}/allocation/merchant/{partner_id}'
        query_string = urlencode({'since': since})
        url = urlparse(self._fulfillment_url)._replace(
            path=path, query=query_string).geturl()
        r = requests.get(url, headers=self.headers)
        validate_response(r)

        next_link = r.links['next']['url'] if 'next' in r.links else None
        return {'data': r.json(), 'url': url} \
            if next_link else {'data': r.json()}
