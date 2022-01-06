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

# function to create an AAD group
def createAADgroup(token, endpoint, payload):
    graph_data = requests.post(  # Use token to call downstream service
        endpoint,
        json=payload,
        headers={'Authorization': 'Bearer ' + token, 'Content-type': 'application/json'},).json(),
            
    print("Graph API call result: %s" % json.dumps(graph_data, indent=2))

# load parameters from JSON file
with open(os.path.join(sys.path[0], "createGroup-parametersEdTestHaszbro.json")) as json_file:
    config = json.load(json_file)

authority = config["authority"]
client_id = config["client_id"]
scope = config["scope"]
secret = config["secret"]
endpoint = config["endpoint"]

# get the JSON payload
with open(os.path.join(sys.path[0], "creategrouppayloadHaszbro.json")) as json_file:
    payload = json.load(json_file)
    #payloadstr = str(payload)

# get a Graph API token to use for API calls
token = get_token(client_id, authority, secret, scope,)

# create a group
createAADgroup(token, endpoint, payload)

#print(payload)