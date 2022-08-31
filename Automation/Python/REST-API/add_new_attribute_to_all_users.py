from operator import eq, index, length_hint
import requests,json
from urllib3.exceptions import InsecureRequestWarning # for suppressing Warning: "InsecureRequestWarning: Unverified HTTPS request is being made to host 'YOUR_HOSTNAME'

## Suppress only for the single warning from urllib3 needed.                                                                            ##
## Adding certificate verification is strongly advised ! See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings ##
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


#############################################################################
#                                                                           #
#  This script retrieves the userid from all users in the realm.            #
#  After that it retrieves all attributes for the current user.             #
#  Adds a new attribute [i18n] and pushes all attributes via API            #
#  into the database.                                                       #
#                                                                           #
#  @Author networksecurityvodoo                                             #
#  @Version: 2.1 - 31.08.2022                                               #
#############################################################################

target_host = "https://192.168.94.33:8443"
login_string = 'username=esbadmin&password=esbadmin&client_id=frontend&client_secret=a73bd556-9449-46b3-8e05-705444a8f39c&grant_type=password'

start_value_pagination = 0
limit = 100



def get_accesstoken():
    """Retreive Accesstoken from target_host/auth/realms/{realm}/protocol/openid-connect/token"""

    url = "https://192.168.94.33:8443/auth/realms/trafineo/protocol/openid-connect/token"
    payload=login_string

    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
   # print(response.text)
    #global token_data  #should be available for other functions
    token_data =json.loads(response.text)
    #print(token_data['access_token'])      # Bearer Token
    return token_data

def get_usercount_in_realm():
    """GET number of users in /{realm}/users"""
    token_data = get_accesstoken()
    url = str(target_host)+"/auth/admin/realms/trafineo/users/count"
    payload='='
    headers = {
      'Authorization': 'Bearer '+token_data['access_token'],
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response_user_count = requests.request("GET", url, headers=headers, data=payload, verify=False)
    print("------------------------------------------------------------------------")
    print ("Total Number of Users in the realm: "+str(response_user_count.text)) 
    print("------------------------------------------------------------------------")



def get_users(start_value_pagination,end_value_pagination):
    """GET /{realm}/users """
    
    token_data = get_accesstoken()
    #global json_arr # retrieved User_Array should be available for other functions

    url2 = str(target_host)+"/auth/admin/realms/trafineo/users?first="+str(start_value_pagination)+"&max="+str(end_value_pagination)+"" 
    payload2='='
    headers2 = {
     'Authorization': 'Bearer '+token_data['access_token'],
     'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    print (url2)
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
    return json_arr


def print_number_of_changed_users(json_arr):
    """ Print the Number of users in the realm selected for change"""
    print("------------------------------------------------------------------------")
    print ("Number of Users in the realm about to be changed in this run: "+str(len(json_arr))) 
    print("------------------------------------------------------------------------")


def add_attribute_to_users(json_arr):
    """ Iterate through users, retrieve existing attributes and add new one """
    
    token_data = get_accesstoken()
    ## for each unique entry in the user dictionary...
    for x in json_arr:
     url3 = str(target_host)+"/auth/admin/realms/trafineo/users/"+str(x['id'])  # prepare URL for GET and PUT
     
     # -- Debug --
     print ("--Changing User-ID (User-URL): --")
     print (url3)
     
     # -- /Debug -- 


    ## Get existing attributes for each user & add new one  
    # ------------------------------------------------------------------------------------
    #print (x) # All Values in the dictionary
    #print(x['attributes'])
    if 'attributes' in x:
        x['attributes']['i18n'] = ['en']
        NewAttributes = x['attributes']
        NewAttributes['i18n'] = ['en']           # add attribute "i18n"
    else:
        x['attributes'] = {}
        NewAttributes = x['attributes']
        NewAttributes['i18n'] = ['en']
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
      'Authorization': 'Bearer '+token_data['access_token'],
        }

    response3 = requests.request("PUT", url3, headers=headers3, data=payload3, verify=False) # write via PUT !
    response3_HTTP_REASON = response3.reason
    response3_HTTP_CODE = response3.status_code

    ## log feedback into console ...
    print("    ")
    print("Last changed User on this run (Username):"+" "+x['username']+" ...")
    print("Attributes retrieved: "+str(x['attributes']))
    print("Attributes changed:   "+ str(NewAttributes))
    print("Last HTTP Response Code:   " +str(response3_HTTP_CODE)+" "+str(response3_HTTP_REASON))
    print("------------------------------------------------------------------------")
    
    return response3_HTTP_CODE, response3_HTTP_REASON, NewAttributes,  x['username'], x['attributes']



## Main ##
get_usercount_in_realm()

start_index =  start_value_pagination 


user_array = get_users(start_index,limit)
while len(user_array) > 0:
  print_number_of_changed_users(user_array)
  add_attribute_to_users(user_array)
  start_index = start_index + limit
  user_array = get_users(start_index,limit)
if len(user_array) < 1 :
  print("Changes complete, please verify !")
else:
  print("Changes not complete, please check !")

