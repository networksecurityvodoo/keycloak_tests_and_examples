SELECT ID,USER_ID,Name,[VALUE] FROM USER_ATTRIBUTE order by ID DESC        -- Nutzerattribute (ID,USER_ID,Name,VALUE)

SELECT USER_ID,ROLE_ID FROM USER_ROLE_MAPPING                              -- Nutzer 2 Rolle (ROLE_ID, USER_ID)



SELECT * FROM KEYCLOAK_GROUP
WHERE ID='5b2289aa-0db5-4702-baaa-ae4a05805aa1'                                              -- Gruppen Informationen (ID, NAME, PARENT_GROUP, REALM_ID)

SELECT * FROM GROUP_ATTRIBUTE                                             -- Gruppenattribute (ID, NAME, VALUE, GROUP_ID)

SELECT * FROM GROUP_ROLE_MAPPING                                          -- Rolle 2 Gruppe  (ROLE_ID, GROUP_ID)


SELECT * FROM USER_GROUP_MEMBERSHIP                                         -- Nutzer 2 Gruppe






SELECT * FROM KEYCLOAK_ROLE                                                -- Rolleninformationen (ID,CLIENT_REALM_CONSTRAINT,CLIENT_ROLE [0=Nein, 1= JA], DESCRIPTION, NAME, REALM_ID,CLIENT,REALM)
WHERE REALM_ID IN('master') AND CLIENT_ROLE = '0'
ORDER BY NAME,REALM_ID DESC  


SELECT * FROM REALM_DEFAULT_ROLES          -- Standard Rollen (REALM_ID, ROLE_ID)
SELECT * FROM REALM_DEFAULT_GROUPS         -- Standard Gruppen (REALM_ID, GROUP_ID)





SELECT * FROM REALM_SMTP_CONFIG             -- eMail Konfiguration (Passwort im Klartext !)

SELECT * FROM REALM_SUPPORTED_LOCALES      -- Welche Sprachen wurden für das Realm in Keycloak aktiviert ...
