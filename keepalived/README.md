Once upon a time I decided to deploy a backup mysql server. And of course I would like to find a solution which will allow me to have failover mechanism. I've read a lot about different technologies which help to resolve this task.
#
We have various solutions:
* [MariaDB MaxScale](https://mariadb.com/kb/en/mariadb-maxscale-24-mariadb-maxscale-installation-guide/)
* [MySQL Router](https://dev.mysql.com/doc/mysql-router/8.0/en/mysql-router-general.html)
* [HAProxy](http://www.haproxy.org/)
* [ProxySQL](https://github.com/sysown/proxysql/)
* pacemaker/corosync
* [keepalived](https://www.keepalived.org/)

And this time I tried **keepalived** service.
I configured two mysql servers. Both servers are master. I know this is a complicated solution. But I decided to use them as active/passive. It allows me to use them safely.
### Instalation:
```
apt-get install keepalived
```
### Configuration file:
```
$ sudo vim /etc/keepalived/keepalived.conf
```
### Monitoring service:
```
$ sudo tail -f /var/log/syslog | grep Keepalived
$ sudo systemctl status keepalived
$ ip addr show | grep VI
```
