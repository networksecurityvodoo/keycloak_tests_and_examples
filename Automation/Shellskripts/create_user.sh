!/bin/bash

#############################
# Add User via Keycloak CLI #
#                           #
#############################
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

#Add USER
echo " * user creation\n"
curl -s -w "\n\n%{http_code}\n -X POST "${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_REALM}/users" \
-H "Content-Type: application/json" -H "Authorization: bearer $TKN" \
--data '{"username":"xyz", "firstName":"xyz","lastName":"xyz", "email":"demo2@email.domain", "enabled":"true"}


## Example Values:

#{"id":"",
#"createdTimestamp":1632411856264,
#"username":"xyz",
#"enabled":true,
#"totp":false,
#"emailVerified":false,
#"firstName":"xyz",
#"lastName":"xyz",
#"email":"demo2@email.domain",
#"disableableCredentialTypes":[],
#"requiredActions":["update_user_locale","CONFIGURE_TOTP","VERIFY_EMAIL","UPDATE_PASSWORD","UPDATE_PROFILE"],
#"notBefore":0,
#"access":{"manageGroupMembership":true,"view":true,"mapRoles":true,"impersonate":true,"manage":true}}
