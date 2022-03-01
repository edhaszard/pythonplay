import sys
from textwrap import indent
import msal
import requests
import json
import os
import shutil

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
            
#     print("Graph API call result: %s" % json.dumps(graph_data, indent=2))

# load parameters from JSON file
with open(os.path.join(sys.path[0], "createGroup-parametersEdTestIHC.json")) as json_file:
    config = json.load(json_file)
    authority = config["authority"]
    client_id = config["client_id"]
    scope = config["scope"]
    secret = config["secret"]
    endpoint = config["endpoint"]

# copy the generic payload file to work with the current Area
area = "Taranaki"
city = "Taranaki"
originalfile = (os.path.join(sys.path[0], "creategrouppayloadSalesForcegeneric.json"))
newfile = (os.path.join(sys.path[0], "areapayloads/creategrouppayloadSalesForce" + area + ".json"))
shutil.copyfile(originalfile,newfile)

# modify the  JSON payload with the current Area details
with open(os.path.join(sys.path[0], newfile), "r+") as json_file:
    areafile = json.load(json_file)

    open(newfile, 'w').close()
    
    areafile["description"] = areafile["description"].replace('<department/area>', area)
    areafile["displayName"] = areafile["displayName"].replace('<department/area>', area)
    areafile["membershipRule"] = areafile["membershipRule"].replace('<department/area>', area)
    areafile["membershipRule"] = areafile["membershipRule"].replace('<city>', city)
    json_file.seek(0)
    json.dump(areafile, json_file, indent=4)
    
with open(newfile, "r+") as json_file:
    payload = json.load(json_file) 

# get a Graph API token to use for API calls
token = get_token(client_id, authority, secret, scope,)

# create a group
createAADgroup(token, endpoint, payload)

#print(token)