#Need to install requests package for python
#easy_install requests
import requests
import json

# Set the request parameters
#url = 'https://dev87552.service-now.com/api/now/table/sc_request?sysparm_limit=1'
#url = 'https://dev87552.service-now.com/api/now/table/sc_req_item'
url = 'https://dev90399.service-now.com/api/sn_sc/servicecatalog/catalogs?sysparm_limit=10'

# Eg. User name="admin", Password="admin" for this code sample.
user = 'admin'
pwd = 'Lgcns2020+'
#pwd = 'Wh9fCOwD2zhZ'

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}

# Do the HTTP request
response = requests.get(url, auth=(user, pwd), headers=headers )

# Check for HTTP codes other than 200
if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()

# Decode the JSON response into a dictionary and use the data
data = response.json()
print(json.dumps(data, indent=4))

