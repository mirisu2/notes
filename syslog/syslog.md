### [RSYSLOG](https://www.rsyslog.com/doc/v8-stable/configuration/)
vim /etc/rsyslog.conf
```
#################
#### MODULES ####
#################

# provides support for local system logging
module(load="imuxsock")
# provides kernel logging support
module(load="imklog")

# provides UDP syslog reception
module(load="imudp")
input(type="imudp" port="514")

# provides TCP syslog reception
module(load="imtcp")
input(type="imtcp" port="514")

###########################
#### GLOBAL DIRECTIVES ####
###########################

# Include all config files in /etc/rsyslog.d/
$IncludeConfig /etc/rsyslog.d/*.conf

$AllowedSender UDP, 127.0.0.1, 10.0.0.0/8, 172.16.0.0/16, 192.168.198.0/24

###############
#### RULES ####
###############

auth,authpriv.*                        @192.168.198.101
auth,authpriv.*                        /var/log/auth.log
# OR
auth,authpriv.* {
    action(type="omfile" file="/var/log/auth.log")
    action(type="omfwd" target="192.168.198.101" port="514" protocol="udp")
}
```
vim /etc/rsyslog.d/mysql.conf
```
module (load="ommysql")
local6.* action(type="ommysql" server="localhost" db="Syslog" uid="rsyslog" pwd="pass4wd")
& stop

if $fromhost-ip=='192.168.1.1' then action(type="ommysql" server="localhost" db="Syslog" uid="rsyslog" pwd="pass4wd")
& stop

if $fromhost-ip startswith '172.16.15.' then action(type="ommysql" server="localhost" db="Syslog" uid="rsyslog" pwd="pass4wd")
& stop
```
