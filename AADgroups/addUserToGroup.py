import msal
import requests
import json

# "Ed Test" App Registration in IHC Azure AD:
client_id = '352cef7b-9b63-4bb8-a2af-05df03eb37c8'
tenant_id = '35558aca-3637-44e9-8cc7-393f0482cb28'
client_secret = '0_D_QnRos~h0wHmo0E1Z6Fwzy_JS.W67O3'

# function to get graph api token
def get_token(client_id, tenant_id, client_secret):
    scope = ["https://graph.microsoft.com/.default"]
    app = msal.ConfidentialClientApplication(client_id,
                        authority='https://login.microsoftonline.com/{}'.format(tenant_id),
                        client_credential=client_secret
                        )
    result = app.acquire_token_silent(scopes=scope, account=None)
    if not result:
        result = app.acquire_token_for_client(scopes=scope)
    return result['access_token']

# get a Graph API token to use for API calls
token = get_token(client_id, tenant_id, client_secret)