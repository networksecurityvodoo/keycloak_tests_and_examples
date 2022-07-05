import requests,json
#############################################################################
#                                                                           #
#  This script retrieves the userid from all users in the realm.            #
#  After that it retrieves all attributes for the current user.             #
#  Adds a new attribute [i18n] and pushes all attributes via API            #
#  into the database.                                                       #
#  @Author networksecurityvodoo                                             #
#  @ Version: 1.1 - 05.07.2022                                              #
#############################################################################
# ------------------------------------------------------------------------------------
## Get Token 
# ------------------------------------------------------------------------------------

url = "http://localhost:8000/auth/realms/Test_Realm/protocol/openid-connect/token"

payload='username=python&password=123456&client_id=pytest&client_secret=766716a8-b531-4d6a-a379-1dc4ff37517f&grant_type=password'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}
response = requests.request("POST", url, headers=headers, data=payload, verify=False)
#print(response.text)
data =json.loads(response.text)
#print(data['access_token'])      # Bearer Token

# ------------------------------------------------------------------------------------
## GET /{realm}/users 
# ------------------------------------------------------------------------------------
url2 = "http://localhost:8000/auth/admin/realms/Test_Realm/users"
payload2='='
headers2 = {
  'Authorization': 'Bearer '+data['access_token'],
  'Content-Type': 'application/x-www-form-urlencoded'
}

# -- Debug -- 
#print("-------------------------------------")
#print ("--Debug: Accesstoken--")
#print (headers2)
# -- /Debug --

users = requests.request("GET", url2, headers=headers2, data=payload2, verify=False)
json_arr = users.json()

# -- Debug -- 
#print("-------------------------------------")
#print ("--Debug: Users--")
#print (users.text)
# -- /Debug -- 

print("------------------------------------------------------------------------")
print ("Number of users in the realm about to be changed: "+str(len(json_arr))) 
print("------------------------------------------------------------------------")

counter = 0 # counting number of changed users(number of iterations through the dictionary)

# ------------------------------------------------------------------------------------
## for each unique entry in the dictionary...
# ------------------------------------------------------------------------------------
for x in json_arr:
     url3 = "http://localhost:8000/auth/admin/realms/Test_Realm/users/"+str(x['id'])  # prepare URL for GET and PUT
     
     # -- Debug --
     #print ("--Debug: User-URL--")
     #print (url3)
     
     # -- /Debug -- 

# ------------------------------------------------------------------------------------
## Get existing attributes for each user & add new one  
# ------------------------------------------------------------------------------------
    #print (x) # All Values in the dictionary
     # print(x['attributes'])
     x['attributes']['i18n'] = ['en-GB']
     NewAttributes = x['attributes']
     NewAttributes['i18n'] = ['en-GB']           # add attribute "i18n"
    
     # -- Debug -- 
    # print ("--Debug: Attribute Values--")
    # print (NewAttributes)
     # -- /Debug -- 

# ------------------------------------------------------------------------------------
# write all attributes via PUT 
# ------------------------------------------------------------------------------------

     payload3 = json.dumps({
     "attributes": NewAttributes
     })
     # -- Debug -- 
     #print ("--Debug: Payload Content--")
     #print (payload3)
     # -- /Debug -- 

     headers3 = {
       'Content-Type': 'application/json',
       'Authorization': 'Bearer '+data['access_token'],
     }

     response3 = requests.request("PUT", url3, headers=headers3, data=payload3, verify=False) # write via PUT !
     responsecode = response3.status_code

     ## log feedback into console ...
     print("    ")
     print("Adding attribute to User:"+" "+x['username']+" ...")
     print("Attributes retrieved: "+str(x['attributes']))
     print("Attributes changed:   "+ str(NewAttributes))
     print("Response HTTP Code:   "+ str(responsecode))
     counter = counter + 1
print("------------------------------------------------------------------------")
print ("Number of changed Users:" + str(counter))
