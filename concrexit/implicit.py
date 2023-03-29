import logging

from oauthlib.oauth2 import MobileApplicationClient
from requests_oauthlib import OAuth2Session

from concrexit.apiservice import ConcrexitAPIService


class ConcrexitImplicitAPIService(ConcrexitAPIService):
    """
    This is a service that uses the implicit grant flow.
    This flow is used when the application is a user and needs to access the API.
    Codes can be obtained by going to the authorize URL and logging in, then copying the code from the URL, so this flow
    does require user interaction.
    Also note that authorization codes are transfered in the URL, so this flow is not very secure and users must reauthenticate
    every time the code expires.
    If no redirect URL is provided, the default is http://localhost:8080/callback.
    """

    def __init__(self, redirect_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = None
        self._redirect_url = redirect_url or "http://localhost:8080/callback"

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
            client=MobileApplicationClient(client_id=self.client_id),
            redirect_uri=self._redirect_url,
            scope=self.scope,
        )
        authorization_url, state = oauth.authorization_url(self.authorize_url)
        print(
            f"Please go to the following URL and authorize access: {authorization_url}"
        )
        authorization_response = input("Enter the full callback URL: ")

        self.token = oauth.token_from_fragment(authorization_response)
        logger.debug(f"Got token {self.token}")
