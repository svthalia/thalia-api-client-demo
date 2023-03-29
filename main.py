import logging
import os

from concrexit.backend import ConcrexitBackendAPIService


def hello_concrexit():
    base_url = os.environ.get("CONCREXIT_BASE_URL", "https://staging.thalia.nu")
    client_id = os.environ.get("CONCREXIT_CLIENT_ID", "123456789")
    client_secret = os.environ.get("CONCREXIT_CLIENT_SECRET", "abcdefghij")
    scope = ["read", "write"]

    concrexit = ConcrexitBackendAPIService(
        base_url=base_url,
        client_id=client_id,
        client_secret=client_secret,
        scope=scope,
    )  # or ConcrexitLegacyAPIService, or ConcrexitWebAPIService, or ConcrexitImplicitAPIService

    response = concrexit.get("/api/v2/members/me/")
    if response.status_code == 200:
        print("I am", response.json())
    elif response.status_code == 403:
        print("Could not authenticate as a user", response.json())
    else:
        print("Something went wrong", response.json())


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger("concrexit").setLevel(logging.DEBUG)
    hello_concrexit()
