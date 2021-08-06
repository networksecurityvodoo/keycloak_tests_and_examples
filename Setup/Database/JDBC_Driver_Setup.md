## Steps for deploying of JDBC-Driver
---

Prerequisites:
* You should already have the driver JAR-File for the Databasemanagementsystem you use save to your disk.
In our case this is MariaDB (https://downloads.mariadb.org/connector-java/).

* You should be already logged in into the HAL Management Console (Server-IP:9990)

---

1. Under the Entry 'Deployments' 
   click on the "+" and select "Upload Deployment".

<!-- <img src="A_Upload_Driver.png" alt="" width="50%"/> --> 

 ![Deployment Step1](./images/A_Upload_Driver.png)

2. In the new dialogue choose the JAR-File, which you downloaded before. 

 ![Deployment Step2](./images/00-WildFly-Deploy.png)

3. Choose a name for the Deployment (will be referenced in the Datasource) and set it to enabled.

 ![Deployment Step3](./images/01-WildFly-Deploy.png)

4. Reboot the Server and check the Deployments-Tab, it should look like below.

 ![Deployment Step4](./images/02-WildFly-Deploy.png)


