#!/bin/bash

##############################################
# DELETE Keycloak User via REST-API from CLI #
#                                            #
##############################################


##################################################################################################
# How-To use:	#										                                                               #
#												                                                                         #
# The Username is read from the first Parameter provided to this Skript.                         #
# Example ./get_user.sh admin                                                                    #
#                                                                                                #
#												                                                                         #
# Please Note:#                                                       							             #
#												                                                                         #
# 1.) This Skript authenticates via Username and Passwort to recieve a Bearer_Token.		         #
#     With this Bearer_Token you have the possibility to Authenticate each request you make.     #
#     As this is a fire and forget shell script there is no usage of the Refresh_Token.          # 
#												                                                                         #
# 2.) This Skript requires https://stedolan.github.io/jq/download/ for JSON-Parsing  		         #
#     Under Debian like systems just use: apt-install jq -y to install it via CLI		             #
#												                                                                         #
# 3. With DEBUG="1" you can echo the Points in which errors tend to occur mostly.                #
#    DEFAULT is DEBUG="", which remains the script silent.                                       #
##################################################################################################

## Check if parameter "Username" is provided ##
if [[ $#<1 ]]
  then
    echo "Error: No Username supplied as Parameter !"
    exit 1
elif [[ $#>1 ]]
	then echo "Error: Only one Parameter (Username) allowed ! "
	exit 1
fi

## Parameter Configuration ##
Param1_Username=$1

KEYCLOAK_URL=http://YOUR-IP/auth
KEYCLOAK_REALM=REALM_NAME

KEYCLOAK_CLIENT_ID=rest-client
USER_NAME=apiuser
USER_PASSWORD=$(echo PASSWORD_IN_BASE64_HERE|base64 -d)   # To Encode Password in Base64 use  echo PASSWORD_HERE | base64

# Fill in anything as value for DEBUG to enable the function.
DEBUG=""

## This Function is only build for enabling/disabling Debug-Mode
function debugecho {
    if [ ! -z "$DEBUG" ]
    then
        echo "$*"
    fi
}

## DEBUG_POINT - SHOW $Param1_Username
debugecho Username:
debugecho $Param1_Username
debugecho ""

## RECIEVE Token and store in $ACCS_TKN
export ACCS_TKN=$(curl -s -X POST "${KEYCLOAK_URL}/realms/${KEYCLOAK_TARGET_REALM}/protocol/openid-connect/token" \
 -H "Content-Type: application/x-www-form-urlencoded" \
 -d "username=${KEYCLOAK_USER_NAME}" \
 -d "password=${KEYCLOAK_USER_PASSWORD}" \
 -d 'grant_type=password' \
 -d "client_id=${KEYCLOAK_CLIENT_ID}" | jq -r '.access_token')

## DEBUG_POINT - SHOW $ACCS_TKN
debugecho BEARER_TOKEN:
debugecho $ACCS_TKN
debugecho ""

## RETRIEVE User_ID from USERNAME
JSON=$(curl -s -X GET "${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_TARGET_REALM}/users/?username=${1}" \
-H "Accept: application/json" \
-H "Authorization: Bearer $ACCS_TKN")

# TRIM the RESPONSE recieved to the JSON Standard
JSON=$(echo ${JSON:1})        # First Sign recieved is a "[" this stops jq from reading the correct JSON, so this gets removed
JSON=$(echo ${JSON%?})        # Last character recieved is a "]" this stops jq from reading the corect JSON, so this gets removed

# STORE the ID of the USER provided as PARAMETER in $USERID
USERID=$(echo ${JSON} | jq -r '.id') 

## DEBUG_POINT - SHOW USERID
debugecho USER_ID:
debugecho $USERID
debugecho " "

##DELETE USER
http_code=$(curl -s  -X DELETE "${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_TARGET_REALM}/users/${USERID}" -H "Authorization: Bearer $ACCS_TKN")
#NOTE: HTTP 204 = Success | HTTP 405= Most likely User doesn't exist.

if [ ! -z "$http_code" ]
 then
   echo "Deleting the User failed !"
   echo "$http_code"
   echo "Hint: You can set the Debugparameter in this Skript if you have trouble locating the issue." 
exit 1
else
echo "User successfully deleted !"
fi
exit 0
