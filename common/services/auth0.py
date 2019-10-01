import logging

from django.conf import settings
import requests

logger = logging.getLogger(__name__)

class Auth0Client:
    """A client for the Auth0 Management API V2"""
    def __init__(self):
        self.domain         = settings.AUTH0['domain']
        self.client_id      = settings.AUTH0['client_id']
        self.client_secret  = settings.AUTH0['client_secret']
        self.audience       = settings.AUTH0['audience']
        self.base_url       = f'https://{self.domain}/api/v2'
        self.access_token   = self.get_access_token()

    def get_access_token(self):
        result = requests.post(
            url=f'https://{self.domain}/oauth/token',
            json={
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'audience': self.audience,
            },
        )
        return result.json()['access_token']

    def post(self, path, data):
        """POST to the Auth0 Management API V2

        Args:
        - path (string): The request path (e.g. /users)
        - data (dict): The data in the POST body

        Returns:
        (dict): The result of the request
        """
        data        = dict(data)
        post_url    = f'{self.base_url}{path}'

        logger.debug('Creating a new user')
        logger.debug(f'POST {post_url} -- {str(data)}')

        response = requests.post(
            url=post_url,
            json=data,
            headers={
                'Authorization': f'Bearer {self.access_token}',
            },
        )
        logger.debug(f'Response from POST {post_url} -- {str(response.json())}')
        return response.json()
