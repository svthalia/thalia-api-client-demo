# Hello, concrexit!
This repository contains example code for communicating with the concrexit API. 
The code is written in Python and uses the requests library.
Authentication is done using OAuth2.0 (which is the main feature of this repository).

4 different `ConcrexitAPIService`s are provided, implementing different oauth flows:
- `ConcrexitWebAPIService` uses the authorization code grant flow with PKCE
- `ConcrexitImplicitAPIService` uses the implicit grant flow
- `ConcrexitLegacyAPIService` uses the resource owner password credentials grant flow
- `ConcrexitBackendAPIService` uses the client credentials grant flow

The code in this repository is not meant to be used in production, but rather as an example of how to use the concrexit API.
