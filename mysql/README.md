* **mysqlslap** is a diagnostic program designed to emulate client load for a MariaDB server and to report the timing of each stage. It works as if multiple clients are accessing the server.
* **mysqlshow** client can be used to quickly see which databases exist, their tables, or a table´s columns or indexes.
* **mysqlhotcopy** is a Perl script that was originally written and contributed by Tim Bunce. It uses FLUSH TABLES, LOCK TABLES, and cp or scp to make a database backup. It is a fast way to make a backup of the database or single tables, but it can be run only on the same machine where the database directories are located.  mysqlhotcopy works only for backing up MyISAM and ARCHIVE tables. 
* **mysqlreport** Makes a friendly report of important MySQL status values
* **mysql_secure_installation**
* **mysqldump**
* **mysqlcheck**
```
--analyze, -a
--optimize, -o
--repair, -r
```
* **mysqlanalyze** dbname
* **mysqloptimize
* **mysqlrepair**
#
```
SHOW VARIABLES LIKE 'have_query_cache';
SHOW VARIABLES LIKE 'query_cache_%';

SET profiling = 1;
SELECT * FROM customers;
SHOW PROFILES;
SHOW PROFILE FOR QUERY 1;
```
## MASTER-MASTER
### STEP 1. /etc/mysql/mariadb.conf.d/50-server.cnf
```
[mysqld]
server-id         = 120 #the optimal way to specify the last octet of ip address
log_bin           = /var/log/mysql/mysql-bin.log
log_bin_index     = /var/log/mysql/mysql-bin.log.index
relay_log         = /var/log/mysql/mysql-relay-bin.log
relay_log_index   = /var/log/mysql/mysql-relay-bin.index
expire_logs_days  = 10
max_binlog_size   = 100M
sync_binlog       = 1
log_slave_updates = 1 #it allows us to convert slave server to master
```
### STEP 2. create account on both servers
```
GRANT REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO repl@'192.168.198.%' IDENTIFIED BY 'myPas#d';
```
### STEP 3 on slave
```STOP SLAVE;```
### Move data from master to slave
```
mysqldump -u root -p --triggers --routines --opt --lock-all-tables --master-data --databases mydb | ssh john@192.168.198.120 mysql --user=root --password=myPass4wd mydb
```
### STEP 4 Check MASTER_LOG_FILE and MASTER_LOG_POS on master server:
```SHOW MASTER STATUS\G```
### STEP 5 on slave
```
CHANGE MASTER TO master_host='192.168.198.120', master_port=3306, master_user='repl', master_password='myPas#d', master_log_file='mysql-bin.000053', master_log_pos=31785723;
```
### STEP 6 on slave
```START SLAVE;```

### Monitoring
```
SHOW MASTER LOGS;
SHOW BINLOG EVENTS;
SHOW BINARY LOGS;
SHOW BINLOG EVENTS IN 'mysql-bin.000058' FROM 4186178\G
SHOW PROCESSLIST\G
SHOW МASTER STATUS;
SHOW SLAVE STATUS\G
```
### Troubleshooting
##### One problem I had on slave
```
MariaDB [(none)]> SHOW SLAVE STATUS\G
                Slave_IO_State: Waiting for master to send event
              Slave_IO_Running: **Yes**
             Slave_SQL_Running: **No**
                    Last_Errno: 1396
                    Last_Error: Error 'Operation DROP USER failed for ...
                  Skip_Counter: 0
           Exec_Master_Log_Pos: 92320728
               Relay_Log_Space: 5509915
                 Last_IO_Error:
                Last_SQL_Errno: 1396
                Last_SQL_Error: Error 'Operation DROP USER failed for ...
```
STOP SLAVE;SET GLOBAL SQL_SLAVE_SKIP_COUNTER = 1;START SLAVE;
