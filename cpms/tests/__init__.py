from unittest import mock


def mock_response(
        status_code=200,
        content=None,
        json_data=None,
        raise_for_status=None):
    """
    since we typically test a bunch of different
    requests calls for a service, we are going to do
    a lot of mock responses, so its usually a good idea
    to have a helper function that builds these things
    """

    mock_resp = mock.Mock()
    mock_resp.raise_for_status = mock.Mock()
    if raise_for_status:
        mock_resp.raise_for_status.side_effect = raise_for_status

    mock_resp.status_code = status_code
    mock_resp.content = content
    if json_data:
        mock_resp.json = mock.Mock(
            return_value=json_data
        )
    return mock_resp
