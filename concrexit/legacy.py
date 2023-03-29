import logging

from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

from concrexit.apiservice import ConcrexitAPIService


class ConcrexitLegacyAPIService(ConcrexitAPIService):
    """
    This is a service that uses the legacy application flow to get a token (also known as the resource owner password credentials flow).
    It does not require user interaction, but instead, username and password, are provided to the client, so this flow can only be used if the client is trusted.
    """

    def __init__(self, username, password, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = None
        self._username = username
        self._password = password

    @property
    def _client(self):
        if self.token is None:
            self._get_token()
        return OAuth2Session(
            self.client_id,
            token=self.token,
        )

    def _get_token(self):
        logger = logging.getLogger("concrexit")
        logger.info("Getting token")

        oauth = OAuth2Session(
            client=LegacyApplicationClient(client_id=self.client_id),
            scope=self.scope,
        )
        self.token = oauth.fetch_token(
            token_url=self.token_url,
            username=self._username,
            password=self._password,
            client_id=self.client_id,
            client_secret=self.client_secret,
            scope=self.scope,
        )
        logger.debug(f"Got token {self.token}")
