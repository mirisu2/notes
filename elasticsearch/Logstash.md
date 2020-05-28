# Logstash
#### Prerequisites
Java 8
#### Установка [Logstash](https://www.elastic.co/downloads/logstash-oss)
```
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
sudo apt-get install apt-transport-https
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
sudo apt-get update && sudo apt-get install logstash
sudo systemctl start logstash.service
```
#### config file
```
/etc/logstash/logstash.yml
```
#### параметры
```
node.name: ls-node-1
path.data: /var/lib/logstash
http.host: "127.0.0.1"
path.logs: /var/log/logstash
```
