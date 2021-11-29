#!/usr/bin/python3

## Requirements :
## Python Version: Python 3.6.9 and above 

import csv
import moduleSQL 


## GET USER_IDs for USERS
conn = moduleSQL.get_connection()
cursor = conn.cursor()
cursor.execute("""SELECT t1.USER_ID
    --,t1.Name,
    --t1.VALUE AS USERTYPE,
    --t2.REALM_ID,
    --t2.USERNAME,
    --t2.EMAIL,
    --t2.EMAIL_VERIFIED,
    --t2.ENABLED
    --,t3.GROUP_ID
    FROM USER_ATTRIBUTE t1
    INNER JOIN USER_ENTITY t2
    ON t1.USER_ID = t2.ID
    WHERE t1.Name = 'role' AND t1.[VALUE]='Value_of_my_Userdefined_Attribute' AND t2.ENABLED='1'""")


# Write USER-IDs into CSV 
c = csv.writer(open('dbdump01.csv', 'w'))
for x in cursor:
    c.writerow(x)





