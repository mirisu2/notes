# Elasticsearch
## Установка [elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/7.7/deb.html#deb-repo)
```
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
sudo apt-get install apt-transport-https
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
sudo apt-get update && sudo apt-get install elasticsearch
```
> elasticsearch не стартует автоматически, его необходимо включить и стартануть
```
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable elasticsearch.service
sudo systemctl start elasticsearch.service
```
### проверяем
```
curl -X GET http://localhost:9200
{
  "name" : "elastic",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "16oUhewqTIa1sE21g_wfJw",
  "version" : {
    "number" : "7.7.0",
    "build_flavor" : "default",
    "build_type" : "deb",
    "build_hash" : "81a1e9eda8e6183f5237786246f6dced26a10eaf",
    "build_date" : "2020-05-12T02:01:37.602180Z",
    "build_snapshot" : false,
    "lucene_version" : "8.5.1",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```
## файл конфигурации [settings](https://www.elastic.co/guide/en/elasticsearch/reference/7.7/settings.html)
```
/etc/elasticsearch/elasticsearch.yml
```
## параметры
```
node.name
```
## права на папку
```
root:elasticsearch
```
> index -> type -> document

> document -> метаполя:
> * _id
> * _type 
> * _index

# Kibana
## Установка [kibana](https://www.elastic.co/downloads/kibana)
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
## файл конфигурации [settings](https://www.elastic.co/guide/en/kibana/7.7/settings.html)
```
/etc/kibana/kibana.yml
```
## параметры
```
server.host: "localhost"
server.host: "0.0.0.0"
```
