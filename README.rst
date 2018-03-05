CpmsConnector
=============
CpmsConnector is connector to aCommerce (CPMS) Public Api


Installing
----------
install using pip or put it to your requirements file

.. code-block:: bash

    $ pip install git+ssh://git@github.com:acomindo/cm-cpms-connector.git



A Simple Example
----------------
This is example guide how to use this library to fetch single order from acommerce (CPMS)

.. code-block:: python

    >>> from cpms import CpmsConnector
    
    >>> config = {
    ...     "username": "somechanel",
    ...     "api_key": "jZW8YjrMZeSaMQG6",
    ...     "api_url": "https://api.acommercedev.com/"
    ... }
    >>> cpmsconn = CpmsConnector(config)
    >>> cpmsconn.token
    'yourtokenkey'

    >>> order_id = 'XYZ10193819'
    >>> channel_id = 'somechannel'

    >>> cpmsconn.get_order(channel_id, order_id)
    'response body of order'
