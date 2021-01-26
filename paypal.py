"""PayPal API Client."""
# -*- coding: utf-8 -*-

import httpx
from pprint import pprint
from types import MappingProxyType


API_SCHEME: str = 'https://'
API_BASE_URL: str = 'api-m.sandbox.paypal.com'
API_VERSION: str = 'v1'

API_PATH_OAUTH: str = 'oauth2/token'
API_PATH_TRANSACTIONS: str = ''

HEADERS: MappingProxyType = MappingProxyType({  # Frozen dictionary
    'Content-Type': 'application/json',
    'Authorization': 'Bearer :accesstoken:',
})


class PayPal(object):
    """PayPal API Client."""

    def __init__(self, client_id: str, secret: str) -> None:
        """Initialize client.

        Arguments:
            client_id {str} -- PayPal client id
            secret {str} -- PayPal secret
        """
        self.client_id = client_id
        self.secret = secret

        self.token = None
        self.token_expires_in = None
        self._authenticate()

    def _authenticate(self) -> None:
        """Generate a bearer access token."""
        url: str = (
            f'{API_SCHEME}{self.client_id}:{self.secret}@{API_BASE_URL}/'
            f'{API_VERSION}/{API_PATH_OAUTH}'
        )
        headers: dict = {
            'Accept': 'application/json',
            'Accept-Language': 'en_US'
        }
        post_data: dict = {'grant_type': 'client_credentials'}

        pprint(url)
        response: httpx._models.Response = httpx.post(  # noqa: WPS437
            url,
            headers=headers,
            data=post_data,
        )

        # Raise error on 4xx and 5xxx
        response.raise_for_status()

        response_data: dict = response.json()

        self.token = response_data.get('access_token')
        self.token_expires_in = response_data.get('expires_in')


        pprint(response.json())


p = PayPal('test', 'test')
