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


