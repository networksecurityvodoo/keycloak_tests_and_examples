!/bin/bash

#############################
# Disable User via Keycloak CLI #
# Date: 2021-09-23          #
#############################
# Username as Parameter 
# requires https://stedolan.github.io/jq/download/ for JSON-Parsing

# config
KEYCLOAK_URL=http://YOUR-IP/auth
KEYCLOAK_REALM=REALM_NAME

KEYCLOAK_CLIENT_ID=rest-client
USER_NAME=apiuser
USER_PASSWORD=$(echo PASSWORD_IN_BASE64_HERE|base64 -d)   # To Encode Password in Base64 use  echo PASSWORD_HERE | base64


# get_Token
export TKN=$(curl -s -X POST "${KEYCLOAK_URL}/realms/${KEYCLOAK_REALM}/protocol/openid-connect/token" \
 -H "Content-Type: application/x-www-form-urlencoded" \
 -d "username=${USER_NAME}" \
 -d "password=${USER_PASSWORD}" \
 -d 'grant_type=password' \
 -d "client_id=${KEYCLOAK_CLIENT_ID}" | jq -r '.access_token')

## The Token is now stored in $TKN
#echo $TKN

#Get User_ID from USERNAME
JSON=$(curl -s -X GET "${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_REALM}/users/?username=${1}" \
-H "Accept: application/json" \
-H "Authorization: Bearer $TKN")

JSON=$(echo ${JSON:1})        # First Sign recieved is a "[" this stops jq from reading the correct JSON, so this gets removed
JSON=$(echo ${JSON%?})        # Last character recieved is a "]" this stops jq from reading the corect JSON, so this gets removed
USERID=$(echo ${JSON} | jq -r '.id') # ID of the User provided 

#USERID is now stored in USERID
#echo USERID

#Disable USER
curl -v -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer $TKN" --data "{\"enabled\": false}" "${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_REALM}/users/${USERID}"
