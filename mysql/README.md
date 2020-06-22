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
#### One problem I had on slave
```
MariaDB [(none)]> SHOW SLAVE STATUS\G
                Slave_IO_State: Waiting for master to send event
              Slave_IO_Running: Yes
             Slave_SQL_Running: No
                    Last_Errno: 1396
                    Last_Error: Error 'Operation DROP USER failed for ...
                  Skip_Counter: 0
           Exec_Master_Log_Pos: 92320728
               Relay_Log_Space: 5509915
                 Last_IO_Error:
                Last_SQL_Errno: 1396
                Last_SQL_Error: Error 'Operation DROP USER failed for ...
```
##### One of solution
```
STOP SLAVE;
SET GLOBAL SQL_SLAVE_SKIP_COUNTER = 1;
START SLAVE;
```
#### Next problem I had on slave server when slave server was incorrectly power off
```
MariaDB [(none)]> SHOW SLAVE STATUS\G;
*************************** 1. row ***************************
                Slave_IO_State: 
                   Master_Host: 192.168.198.25
                   Master_User: repl
                   Master_Port: 3306
                 Connect_Retry: 60
               Master_Log_File: mysql-bin.000023
           Read_Master_Log_Pos: 117197
                Relay_Log_File: mysql-relay-bin.000046
                 Relay_Log_Pos: 65285531
         Relay_Master_Log_File: mysql-bin.000019
              Slave_IO_Running: No
             Slave_SQL_Running: No
                    Last_Errno: 1594
                    Last_Error: Relay log read failure: Could not parse relay log event entry. The possible reasons are: the master's binary log is corrupted (you can check this by running 'mysqlbinlog' on the binary log), the slave's relay log is corrupted (you can check this by running 'mysqlbinlog' on the relay log), a network problem, or a bug in the master's or slave's MySQL code. If you want to check the master's binary log or slave's relay log, you will be able to know their names by issuing 'SHOW SLAVE STATUS' on this slave.
                  Skip_Counter: 0
           Exec_Master_Log_Pos: 65285236
               Relay_Log_Space: 223265799
               Until_Condition: None
                Until_Log_File: 
                 Until_Log_Pos: 0
         Seconds_Behind_Master: NULL
                 Last_IO_Errno: 0
                 Last_IO_Error: 
                Last_SQL_Errno: 1594
                Last_SQL_Error: Relay log read failure: Could not parse relay log event entry. The possible reasons are: the master's binary log is corrupted (you can check this by running 'mysqlbinlog' on the binary log), the slave's relay log is corrupted (you can check this by running 'mysqlbinlog' on the relay log), a network problem, or a bug in the master's or slave's MySQL code. If you want to check the master's binary log or slave's relay log, you will be able to know their names by issuing 'SHOW SLAVE STATUS' on this slave.
   Replicate_Ignore_Server_Ids: 
              Master_Server_Id: 25
```
##### One of solution
```
STOP SLAVE;
SHOW SLAVE STATUS;
! record values of Relay_Master_Log_File и Exec_Master_Log_Pos:
RESET SLAVE;
CHANGE MASTER TO MASTER_LOG_FILE='mysql-bin.000019', MASTER_LOG_POS=65285236;
START SLAVE;
```
#### Next problem I had on master server when slave server was incorrectly power off
```
MariaDB [(none)]> SHOW SLAVE STATUS\G
*************************** 1. row ***************************
               Slave_IO_State: 
                  Master_Host: 192.168.198.120
                  Master_User: repl
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mysql-bin.000054
          Read_Master_Log_Pos: 51324205
               Relay_Log_File: mysql-relay-bin.000033
                Relay_Log_Pos: 4
        Relay_Master_Log_File: mysql-bin.000054
             Slave_IO_Running: No
            Slave_SQL_Running: Yes
                   Last_Errno: 0
                   Last_Error: 
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 51324205
              Relay_Log_Space: 249
              Until_Condition: None
               Until_Log_File: 
                Until_Log_Pos: 0
        Seconds_Behind_Master: NULL
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 1236
                Last_IO_Error: Got fatal error 1236 from master when reading data from binary log: 'Client requested master to start replication from impossible position; the first event 'mysql-bin.000054' at 51324205, the last event read from 'mysql-bin.000054' at 4, the last byte read from 'mysql-bin.000054' at 4.'
               Last_SQL_Errno: 0
               Last_SQL_Error: 
                Parallel_Mode: conservative
```
##### One of solution
```
root@db2:/var/log/mysql# mysqlbinlog mysql-bin.000054 | tail -n 10
...
# at 51301104
#200619 13:51:18 server id 25  end_log_pos `51301135` CRC32 0xc29ebfe3 	Xid = 2649595
COMMIT/*!*/;
DELIMITER ;
# End of log file
ROLLBACK /* added by mysqlbinlog */;
/*!50003 SET COMPLETION_TYPE=@OLD_COMPLETION_TYPE*/;
/*!50530 SET @@SESSION.PSEUDO_SLAVE_MODE=0*/;

STOP SLAVE;
CHANGE MASTER TO MASTER_LOG_FILE='mysql-bin.000054', MASTER_LOG_POS=51301135;
START SLAVE;
```
