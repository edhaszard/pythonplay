import sys
import msal
import requests
import json
import os

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

# function to get details about an AAD group
def getAADgroup(token, endpoint, UPN):
    graph_data = requests.get(  # Use token to call downstream service
        endpoint + '/' + objID, # + '?$select=' + attributes,
        headers={'Authorization': 'Bearer ' + token},).json()
        
    print("Graph API call result: %s" % json.dumps(graph_data, indent=2))

# load parameters from JSON file
with open(os.path.join(sys.path[0], "queryGroup-parameters.json")) as json_file:
    config = json.load(json_file)

    authority = config["authority"]
    client_id = config["client_id"]
    scope = config["scope"]
    secret = config["secret"]
    endpoint = config["endpoint"]
    objID = config["objID"]

# get a Graph API token to use for API calls
token = get_token(client_id, authority, secret, scope,)

# get AAD group info
getAADgroup(token, endpoint, objID)

#print(token)