import base64
import hashlib
import logging
import secrets

from oauthlib.oauth2 import WebApplicationClient
from requests_oauthlib import OAuth2Session

from concrexit.apiservice import ConcrexitAPIService


class ConcrexitWebAPIService(ConcrexitAPIService):
    """
    This is a service that uses the web application flow to get a token (also known as the authorization code flow).
    It uses PKCE to prevent code interception attacks for a public client with HMAC-SHA256.
    This flow is more secure than the implicit flow, but still requires user interaction.
    If no redirect URL is provided, the default is http://localhost:8080/callback.
    """

    def __init__(self, redirect_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._token = None
        self._redirect_url = redirect_url or "http://localhost:8080/callback"

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

    def _get_token(self):
        logger = logging.getLogger("concrexit")
        logger.info("Getting token")

        client = WebApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(
            client=client, redirect_uri=self._redirect_url, scope=self.scope
        )

        code_verifier = secrets.token_urlsafe(40)
        code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
        code_challenge = code_challenge.replace("=", "")

        authorization_url = client.prepare_request_uri(
            self.authorize_url,
            redirect_uri=self._redirect_url,
            scope=self.scope,
            code_challenge=code_challenge,
            code_challenge_method="S256",
        )
        print(
            f"Please go to the following URL and authorize access: {authorization_url}"
        )
        authorization_response = input("Enter the full callback URL: ")

        self._token = oauth.fetch_token(
            token_url=self.token_url,
            authorization_response=authorization_response,
            client_id=self.client_id,
            client_secret=self.client_secret,
            code_verifier=code_verifier,
        )

        # self.__token = oauth.token_from_fragment(authorization_response)
        logger.debug(f"Got token {self._token}")
