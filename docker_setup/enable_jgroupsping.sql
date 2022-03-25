/* Run once against Database to enable High-Availability,
otherwise remove KC2 from Compose File*/

IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='JGROUPSPING' AND xtype='U') CREATE TABLE JGROUPSPING (own_addr varchar(200) NOT NULL, cluster_name varchar(200) NOT NULL, created datetime DEFAULT CURRENT_TIMESTAMP, ping_data varbinary(5000) DEFAULT NULL, PRIMARY KEY (own_addr, cluster_name) )

SELECT * FROM JGROUPSPING
