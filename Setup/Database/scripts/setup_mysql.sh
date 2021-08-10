MYSQL_DBPASS=PASSWORD123

cat >/etc/my.cnf.d/mariadb.cnf<<EOF
[mysqld]
bind-address = 0.0.0.0
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
