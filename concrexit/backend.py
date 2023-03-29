import logging

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from concrexit.apiservice import ConcrexitAPIService


class ConcrexitBackendAPIService(ConcrexitAPIService):
    """
    This is a service that uses the backend application flow (also known as client credentials flow).
    This flow is used when the application is not a user, but a service that needs to access the API.
    Note that not all endpoints are available to this flow because it does not have a user.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._token = None

    def _get_token(self):
        client = BackendApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(client=client, scope=self.scope)

        logger = logging.getLogger("concrexit")
        logger.info("Getting token")
        self._token = oauth.fetch_token(
            token_url=self.token_url,
            client_id=self.client_id,
            client_secret=self.client_secret,
            scope=self.scope,
        )
        logger.debug(f"Got token {self._token}")

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        logger = logging.getLogger("concrexit")
        logger.info(f"Token refreshed: {token}")
        self._token = token

    @property
    def _client(self):
        if self._token is None:
            self._get_token()
        return OAuth2Session(
            self.client_id,
            token=self._token,
            auto_refresh_url=self.refresh_url,
            token_updater=self.token,
        )
