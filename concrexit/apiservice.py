from abc import ABC


class ConcrexitAPIService(ABC):
    """
    This is a service that uses the OAuth2 protocol to authenticate with the Concrexit API and can be used to make requests.
    Note that this class is abstract and should not be used directly. Use one of the subclasses instead, for the different
    OAuth2 flows.
    """

    def __init__(self, base_url, client_id, client_secret, scope=None):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope

        self.authorize_url = f"{base_url}/user/oauth/authorize/"
        self.token_url = f"{base_url}/user/oauth/token/"
        self.refresh_url = f"{base_url}/user/oauth/token/"

    @property
    def _client(self):
        raise NotImplementedError()

    def get(self, path, *args, **kwargs):
        return self._client.get(f"{self.base_url}{path}", *args, **kwargs)

    def post(self, path, data, *args, **kwargs):
        return self._client.post(f"{self.base_url}{path}", data=data, *args, **kwargs)

    def put(self, path, data, *args, **kwargs):
        return self._client.put(f"{self.base_url}{path}", data=data, *args, **kwargs)

    def patch(self, path, data, *args, **kwargs):
        return self._client.patch(f"{self.base_url}{path}", data=data, *args, **kwargs)

    def delete(self, path, *args, **kwargs):
        return self._client.delete(f"{self.base_url}{path}", *args, **kwargs)

    def head(self, path, *args, **kwargs):
        return self._client.head(f"{self.base_url}{path}", *args, **kwargs)

    def options(self, path, *args, **kwargs):
        return self._client.options(f"{self.base_url}{path}", *args, **kwargs)
