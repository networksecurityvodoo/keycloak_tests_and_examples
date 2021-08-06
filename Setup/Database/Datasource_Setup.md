## Steps for Editing the KeyCloak-Datasource
---

Prerequisites:
* You should be already logged in into the HAL Management Console (Server-IP:9990)

*  You should have deployed the the JDBC-Driver.
---

1. Under the Entry 'Configuration ' 
   navigate to the KeyCloakDS Datasource and click on "View".

<img src="A_DS.png" alt="" width="50%"/>


2. In the new dialogue click on "Edit" and ensure to change the Configuration, according to the Screenshots. 


<img src="B_DS.png" alt="" width="50%"/>


<img src="C_DS.png" alt="" width="50%"/>


<img src="E_DS.png" alt="" width="50%"/>

---
Below you find the Field-Values from the Screenshots:

### Attributes-Tab:

* Driver Class: org.mariadb.jdbc.Driver
* Driver Name:  mariadb-java-client-2.7.1.jar
* JNDI Name:    java:/MariaDB

### Connection-Tab:

* Connection URL: jdbc:mariadb://172.21.6.195:3306/db
* JTA:			true
* Use CCM:		true

### Security-Tab:
* User Name: keycloak_srv
* Password   YOUR_PASSWORD
* Allow Multiple Users: false

### Validation-Tab:

* Valid Connection Checker Class Name: org.jboss.jca.adapters.jdbc.extensions.mysql.MySQLValidConnectionChecker
* Validate On Match = ON
* Exception Sorter Class Name : 		 org.jboss.jca.adapters.jdbc.extensions.mysql.MySQLExceptionSorter
