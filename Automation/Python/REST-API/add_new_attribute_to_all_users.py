import requests,json
###############################################################
#                                                             #
#  This script retrieves the userid                           #
#  from all users in the realm.                               #
#  After that it retrieves all                                #
#  attributes for each User.                                  #
#  Adds a new attribute and writes                            #
#  all attributes via API into                                #
#  the database.                                              #
#  @Author https://github.com/networksecurityvodoo 01.07.2022 #
#  @Version 1.0                                               #
#  TODO: Please fix new attribute doesn't get added           #
###############################################################

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
  #'Content-Type': 'application/json'
  'Content-Type': 'application/x-www-form-urlencoded'
}


# -- Debug -- 
print ("--Debug: Accesstoken--")
print (headers2)


users = requests.request("GET", url2, headers=headers2, data=payload2, verify=False)
json_arr = users.json()


# -- Debug -- 
print ("--Debug: Users--")
print (users.text)
# -- /Debug -- 

print ("Number of Users to be edited:"+str(len(json_arr))) 
print("-------------------------------------")

counter = 0 # Counting Number of changed Users(Number of Iterations through dictionary)

# ------------------------------------------------------------------------------------
## do stuff for each unique entry in the dictionary
# ------------------------------------------------------------------------------------
for x in json_arr:
     url3 = "http://localhost:8000/auth/admin/realms/Test_Realm/users/"+str(x['id'])  # prepare URL for GET and PUT
     
     # -- Debug -- 
     print ("--Debug: User-URL--")
     print (url3)
     # -- /Debug -- 

# ------------------------------------------------------------------------------------
## Get existing attributes for each user & add new one  
# ------------------------------------------------------------------------------------
    #print (x) # All Values in the dictionary
     # print(x['attributes'])
     NewAttributes = (str(x['attributes'])
     .replace("'", "\"")                         # replace ' with " 
     .replace("[", " ").replace("]", " ")        # remove brackets
     +',{"i18n":"en-GB"}')                       # add attribute "i18n"
    
     # -- Debug -- 
     print ("--Debug: Attribute Values--")
     print (NewAttributes)
     # -- /Debug -- 

# ------------------------------------------------------------------------------------
# write all attributes via PUT 
# ------------------------------------------------------------------------------------
#json.dumps
     payload3 = {
     "attributes": NewAttributes
     }
     # -- Debug -- 
     print ("--Debug: Payload Content--")
     print (payload3)
     # -- /Debug -- 

     headers3 = {
       'Content-Type': 'application/json',
       'Authorization': 'Bearer '+data['access_token'],
     }

     response3 = requests.request("PUT", url3, headers=headers3, data=payload3, verify=False) # write via PUT !
     print("----------------")
     print("Adding attribute to User:"+" "+x['username']+" ...")
     responsecode = response3.status_code
     print("HTTP Code:"+ str(responsecode))
     counter = counter + 1
print ("Number of changed Users:" + str(counter))
