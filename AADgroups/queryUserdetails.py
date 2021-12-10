import sys
import msal
import requests
import json
import os

# "Ed Test" App Registration in IHC Azure AD:
#client_id = '352cef7b-9b63-4bb8-a2af-05df03eb37c8'
#tenant_id = '35558aca-3637-44e9-8cc7-393f0482cb28'
#client_secret = '0_D_QnRos~h0wHmo0E1Z6Fwzy_JS.W67O3'

# function to get a graph api auth token
def get_token(client_id, authority, secret,scope):
    app = msal.ConfidentialClientApplication(
        client_id, authority=authority,
        client_credential=secret,
    )
    result = None
    
    result = app.acquire_token_silent(scope, account=None)

    if not result:
        result = app.acquire_token_for_client(scopes=scope)

    return result['access_token']

# function to get details about an AAD user
def getAADuser(token, endpoint, UPN, attributes):
    graph_data = requests.get(  # Use token to call downstream service
        endpoint + '/' + UPN + '?$select=' + attributes,
        headers={'Authorization': 'Bearer ' + token},).json()
        
    print("Graph API call result: %s" % json.dumps(graph_data, indent=2))

# load parameters from JSON file in args
# config = json.load(open(sys.argv[1]))

# load parameters from JSON file
with open(os.path.join(sys.path[0], "msal-parametersEdTestIHC.json")) as json_file:
    config = json.load(json_file)

client_id = config["client_id"]
authority = config["authority"]
secret = config["secret"]
scope = config["scope"]
endpoint = config["endpoint"]
UPN = config["UPN"]
attributes = config["attributes"]

# get a Graph API token to use for API calls
token = get_token(client_id, authority, secret, scope,)

# get user(s)
getAADuser(token, endpoint, UPN, attributes)

#print(token)