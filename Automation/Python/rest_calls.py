#!/usr/bin/python3


import requests
from requests.packages import urllib3
import json


#### Retrieve Access_Token from KEYCLOAK

url = "https://URL:PORT/auth/realms/REALM/protocol/openid-connect/token"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # Suppress Certificate Warning from requests that SSL Peer Check is disabled (only for DEVELOPMENT, can lead to MITM) 

payload='username=YOUR_USERNAME&password=YOUR_PASSWORD&client_id=YOUR_ID&client_secret=YOUR_SECRET&grant_type=password'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)
resp_data = response.text # Convert response.text into String

#print(data)        ## Debug

resp_dict = json.loads(resp_data)  ## Parse response as JSON and put into Dictionary (ease of access)

#print (resp_dict) ## Debug

#Check if Response contains access_token and refresh_token
# if true -> store in Variable, else abort with Userfriendly Error 

if 'access_token' in resp_dict:
    var_accestoken = resp_dict.get('access_token')
   # print (var_accestoken)     ##Debug
   
    
    ## Get GroupID by name ##
    var_GroupSearchKeyWord="AttributeNAME"
    url = f"https://URL:PORT/auth/admin/realms/REALM/groups?search={var_GroupSearchKeyWord}"
    payload={}
    headers = {
    'Authorization': "Bearer %s"%var_accestoken
    }
    response = requests.request("GET", url, headers=headers, data=payload , verify=False)
    #print(response.text)

    resp_data = response.text # Convert response.text into String
    #print(resp_data)        ## Debug
    #print (resp_data[1:-1])  
    resp_dict = json.loads(resp_data[1:-1]) ##Remove Leading [ and Trailing ] in Response & Load to Dictionary
    #print (resp_dict)        ##Debug

    if 'id' in resp_dict: 
        var_groupID = resp_dict.get('id')
        #print (var_groupID) ##Debug

        ## Get current Users of the Group requested... ##

        url = f"https://URL:PORT/auth/admin/realms/REALM/groups/{var_groupID}/members" 
        payload={}
        headers = {
        'Authorization': "Bearer %s"%var_accestoken
        }
        response = requests.request("GET", url, headers=headers, data=payload , verify=False)
        resp_data = response.text # Convert response.text into String
            
        ## Write current Group Members to File ##
        f = open("members_of_group.json", "w")
        f.write(resp_data[1:-1])
        f.close()

        
        ## Add Users to Group... ##
        var_UserID="EXAMPE_ID"  #Example with one User
        url = f"https://URL:PORT/auth/admin/realms/REALM/users/{var_UserID}/groups/{var_groupID}" 

        payload={}
        headers = {
        'Authorization': "Bearer %s"%var_accestoken,
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)
        resp_data = response.text # Convert response.text into String
        
        print(resp_data)
       ############

      

    else:
        print("Error! - GroupID not found !")


else:
    print("Error! - Accesstoken missing in Response !")
    
