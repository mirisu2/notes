## [Filebeat](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-overview.html)
#### [Install](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-installation.html) Filebeat
```
aptitude install curl
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.7.0-amd64.deb
sudo dpkg -i filebeat-7.7.0-amd64.deb

OR
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
sudo apt-get install apt-transport-https
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
sudo apt-get update && sudo apt-get install filebeat

root@es-node-1:/etc/filebeat# filebeat version
filebeat version 7.7.0 (amd64), libbeat 7.7.0 [5e69e25b920e3d93bec76a09a31da3ab35a55607 built 2020-05-12 00:53:16 +0000 UTC]
```
#### Filebeat and [systemd](https://www.elastic.co/guide/en/beats/filebeat/current/running-with-systemd.html)
```
systemctl enable filebeat
systemctl disable filebeat
systemctl start filebeat
systemctl stop filebeat
systemctl status filebeat
journalctl -u filebeat.service
systemctl edit filebeat.service
```
#### [Configure](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-configuration.html) Filebeat
> Directory layout
> https://www.elastic.co/guide/en/beats/filebeat/current/directory-layout.html
```
/usr/share/filebeat
/usr/share/filebeat/bin
/etc/filebeat/filebeat.yml
/etc/filebeat/modules.d/
/var/lib/filebeat
/var/log/filebeat
```
#### Load the template manually
```
filebeat setup --index-management -E output.logstash.enabled=false -E 'output.elasticsearch.hosts=["192.168.198.101:9200"]'
```
> Установка дашбордов в кибану. Делал всё по официальной инструкции, получил ошибку.
```
root@es-node-1:/etc/filebeat# /usr/share/filebeat/bin/filebeat setup --dashboards
Loading dashboards (Kibana must be running and reachable)
Skipping loading dashboards, No directory /usr/share/filebeat/bin/kibana/7
```
> Как оказалось, если ставить Filebeat из deb пакета, то нужно запускать wrapper script from /usr/bin/filebeat
```
root@es-node-1:/etc/filebeat# /usr/bin/filebeat setup --dashboards
Loading dashboards (Kibana must be running and reachable)
Loaded dashboards
```
#### To see a list of enabled and disabled modules, run:
```
filebeat modules list
```
#### Enable the modules you want to run:
```
filebeat modules enable nginx mysql
```

## Netflow module
```
ufw allow from <router_ip> to any port 2055
filebeat modules enable netflow
```
#### vim /etc/filebeat/filebeat.yml
```
setup.kibana:
  host: "192.168.198.101:5601"
output.elasticsearch:
  hosts: ["192.168.198.101:9200"]
processors:
  - add_host_metadata: ~
#  - add_cloud_metadata: ~
#  - add_docker_metadata: ~
#  - add_kubernetes_metadata: ~
```
#### vim /etc/filebeat/modules.d/netflow.yml
```
- module: netflow
  log:
    enabled: true
    var:
      netflow_host: 192.168.198.101
      netflow_port: 2055
```
> после старта filebeat, я получил ошибку
```
May 30 19:02:14 es-node-1 filebeat[439]: 2020-05-30T19:02:14.808+0300#011ERROR#011[elasticsearch]#011elasticsearch/client.go:213#
011Failed to perform any bulk index operations:500 Internal Server Error: {"error":{"root_cause":[{"type":"illegal_state_exception",
"reason":"There are no ingest nodes in this cluster, unable to forward request to an ingest node."}],"type":"illegal_state_exception",
"reason":"There are no ingest nodes in this cluster, unable to forward request to an ingest node."},"status":500}
```
> включил в 
```
vim /etc/elasticsearch/elasticsearch.yml
node.ingest: true
node.name: es-node-1
```
> filebeat пишет свои логи в /var/log/syslog. Для дебага включаем
```
vim /etc/filebeat/filebeat.yml
# Sets log level. The default log level is info.
# Available log levels are: error, warning, info, debug
logging.level: debug
```
