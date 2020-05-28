# Kibana
### Установка [kibana](https://www.elastic.co/downloads/kibana)
```
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
sudo apt-get install apt-transport-https
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
sudo apt-get update && sudo apt-get install kibana
```
> kibana не стартует автоматически, его необходимо включить и стартануть
```
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable kibana.service
sudo systemctl start kibana.service
```
### проверяем
```
curl -X GET http://localhost:5601
```
### файл конфигурации [settings](https://www.elastic.co/guide/en/kibana/7.7/settings.html)
```
/etc/kibana/kibana.yml
```
### параметры
```
server.port: 5601
server.host: "0.0.0.0"
server.name: ${HOSTNAME}
elasticsearch.hosts: ["http://192.168.198.99:9200"]
```
