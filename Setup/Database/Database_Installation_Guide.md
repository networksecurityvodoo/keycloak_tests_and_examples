##  Maria-DB installation and configuration
 - Written for CentOS
 
- Install the MariaDB package with the yum package manager (root permissions needed):

yum install mariadb-server
Press y when prompted to proceed with the installation.

2. Edit and run the Skript provided in this Folder:

chmod u+x ./setup_mysql.sh
./setup_mysql.sh 

The Skript will:

- Create a configuration File for your installation
- Bind Maria-DB to an IP-Adress specified by you
- Set the default storage settings as recommended for Keycloak 
- Start the MariaDB Service and set it to be enabled at Boottime
- Run mysql_secure_installation and set a new root Password (specified in the Skript)


Content of setup_mysql.sh:

MYSQL_DBPASS=mysql
cat >/etc/my.cnf.d/openstack.cnf<<EOF
[mysqld]
bind-address = IP_HIER_ÄNDERN !!

default-storage-engine = innodb
innodb_file_per_table
max_connections = 4096
collation-server = utf8_general_ci
character-set-server = utf8
EOF
systemctl enable mariadb.service
systemctl start mariadb.service

/usr/bin/mysql_secure_installation <<EOF

y
$MYSQL_DBPASS
$MYSQL_DBPASS
y
y
y
y
EOF
                                        
To verify that the installation and configuration was successful, check the MariaDB service status by typing:

sudo systemctl status mariadb

The output should show that the service is active and running:

                                       
## Creating a database and a database user for KeyCloak
/usr/bin/mysql -u root -p YOUR_PASSWORD

                                        
```sh
> CREATE DATABASE `db` CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';
> CREATE USER 'keycloak_srv'@'localhost' IDENTIFIED BY 'PASSWORD';
> GRANT USAGE ON *.* TO 'keycloak_srv'@'%' IDENTIFIED BY 'PASSWORD';
> GRANT ALL PRIVILEGES ON keycloak.* TO keycloak_srv@'%';
> FLUSH PRIVILEGES;
> SHOW GRANTS FOR 'keycloak_srv'@'%';
```
 
```sh
> +------------------------------------------------------------------------------------+
> | Grants for keycloak_srv@localhost |
> +------------------------------------------------------------------------------------+
> | GRANT USAGE ON *.* TO 'keycloak_srv'@'%' 
> IDENTIFIED BY PASSWORD '*PASSWORD_HASH' |
> | GRANT ALL PRIVILEGES ON `keycloak`.* TO 'keycloak_srv'@'%'|
> +------------------------------------------------------------------------------------+
```

## If the Database should recieve connections from other hosts


Add Firewall Rule: firewall-cmd --zone=public --add-service=mysql --permanent
