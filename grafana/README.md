#### Install [grafana](https://grafana.com/docs/grafana/latest/installation/debian/) (latest OSS release)
```
sudo apt-get install -y apt-transport-https
sudo apt-get install -y software-properties-common wget
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
sudo apt-get update
sudo apt-get install grafana
sudo systemctl daemon-reload
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
sudo systemctl status grafana-server
```
Installs systemd service: 
```
grafana-server.service
```
Installs configuration file to:
```
/etc/grafana/grafana.ini
```
The default configuration sets the log file at:
```
/var/log/grafana/grafana.log
```
The default configuration specifies an sqlite3 db at:
```
/var/lib/grafana/grafana.db
```
Installs HTML/JS/CSS and other Grafana files at:
```
/usr/share/grafana
```

#### [Configuration](https://grafana.com/docs/grafana/latest/installation/configuration/)
> All options in the configuration file can be overridden using environment variables using the syntax: GF_<SectionName>_<KeyName>
```
# default section
instance_name = ${HOSTNAME}
[security]
admin_user = admin
=
export GF_DEFAULT_INSTANCE_NAME=my-instance
export GF_SECURITY_ADMIN_USER=owner
```

```
[server]
http_port = 3000
http_addr = 192.168.198.98
protocol = http
enable_gzip = true
router_logging = true

[database]
url = mysql://user:secret@host:port/database
type = mysql, postgres or sqlite3
# Only applicable for sqlite3 database. The file path where the database will be stored.
path = /var/lib/grafana/grafana.db 

[remote_cache]

```
