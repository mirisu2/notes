# Elasticsearch
### Установка [elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/7.7/deb.html#deb-repo)
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
### файл конфигурации [settings](https://www.elastic.co/guide/en/elasticsearch/reference/7.7/settings.html)
```
/etc/elasticsearch/elasticsearch.yml
```
### параметры
> the introduction of a feature called **ingest node** in Elasticsearch 5.x onward provided a lightweight solution for preprocessing 
> and enriching documents within Elasticsearch itself before they are indexed.
```
node.name
cluster.name
node.ingest: false
```
### права на папку
```
root:elasticsearch
```
> index -> type -> document

> document -> метаполя:
> * _id
> * _type 
> * _index

> Индексы могут создаваться на "лету" при вставке, либо определены заранее через index template
```
PUT /o_systems/_doc/1
{
    "family": "debian",
    "codename": "stretch",
    "version": 9
}
GET /o_systems/_doc/1
{
  "_index" : "o_systems",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 5,
  "_seq_no" : 7,
  "_primary_term" : 1,
  "found" : true,
  "_source" : {
    "family" : "debian",
    "codename" : "stretch",
    "version" : 9
  }
}
GET /o_systems/_search/
GET /o_systems/_mapping
```
> A *pipeline* defines a series of processors. *Each* processor transforms the document in some way. *Each* processor is executed in
> the order in which it is defined in the pipeline. A pipeline *consists of two main fields*: a description and a list of processors.
```
{
  "description" : "...",
  "processors" : [ ... ]
}
```
#### Ingest APIs *_ingest*
* Put pipeline API *(define a new pipeline)*
```
curl -X PUT http://localhost:9200/_ingest/pipeline/my_pipeline -H 'content-type: application/json' 
-d '{
      "description" : "uppercase the incoming value in the message field", 
      "processors" : [
          {
            "uppercase" : { "field": "message" }
          }
       ]
    }'
```
> When creating a pipeline, multiple processors can be defined, and the order of the execution depends on the order in which it is 
> defined in the definition.
* Get pipeline API
to find the definition of all the pipelines is as follows:
```
curl -X GET http://localhost:9200/_ingest/pipeline -H 'content-type: application/json'
```
To find the definition of an existing pipeline, pass the pipeline ID to the pipeline API:
```
curl -X GET http://localhost:9200/_ingest/pipeline/my_pipeline  -H 'content-type: application/json'
```
* Delete pipeline API
The delete pipeline API deletes pipelines by ID or wildcard match:
```
curl -X DELETE http://localhost:9200/_ingest/pipeline/my_pipeline  -H 'content-type: application/json'
```
* Simulate pipeline API
This pipeline can be used to simulate the execution of a pipeline against the set of documents provided in the body of the request.
```
curl -X POST  http://localhost:9200/_ingest/pipeline/firstpipeline/_simulate -H 'content-type: application/json' 
-d '{
  "docs" : [
    { "_source": {"message":"first document"} },
    { "_source": {"message":"second document"} }
    
  ]
}'
```
or
```
curl -X POST http://localhost:9200/_ingest/pipeline/_simulate -H 'content-type: application/json' 
-d '{
  "pipeline" : {
    "processors":[
      {
         "join": {
          "field": "message",
          "separator": "-"
        }
      }]
  },
  "docs" : [
    { "_source": {"message":["first","document"]} }  
  ]
}'
```
### Шарды
> Шарды помогают распределить индекс по кластеру. Процесс разделения данных по шардам называется шардированием.

> По умолчанию каждый индекс настроен так, чтобы иметь пять шардов в Elasticsearch. В момент создания индекса можно
> обозначить количество шардов, на которые будут разделены данные вашего индекса. После того как индекс создан,
> количество шардов невозможно изменить.

> Каждый шард индекса может быть настроен таким образом, чтобы у него было некоторое количество копий или не было ни одной.
> Реплики шардов — это дополнительные копии оригинального или первичного шарда для обеспечения высокого уровня доступности данных.

### CRUD operations
#### Index API
```
PUT /<index>/<type>/<id>
{...}
or without id (The ID, in this case, will be generated by Elasticsearch)
POST /<index>/<type>{...}
```
#### Get API
```
GET /<index>/<type>/<id>
```
#### Update API
```
POST /o_systems/_update/1 
{ "doc":
  {
    "codename": "squeeze",
    "version": 6
  }
}
```
#### Delete API
```
DELETE /o_systems/_doc/1
```
#### Creating indexes and taking control of mapping
* Creating an index
```
PUT /friends
{
  "settings": {
    "index": {
      "number_of_shards": 5,
      "number_of_replicas": 2
    }
  },
  "mappings": {
    "properties": {
      "first_name": {
        "type": "text"
      },
      "last_name": {
        "type": "keyword"
      }
    }
  }
}
```
* Updating a mapping
```
PUT /friends/_mapping
{
  "properties": {
    "age": {
      "type": "long"
    }
  }
}
```
> Except for supported mapping parameters, you can’t change the mapping or field type of an existing field. Changing an existing field 
> could invalidate data that’s already indexed.
> If you need to change the mapping of a field, create a new index with the correct mapping and reindex your data into that index.



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
server.host: "localhost"
server.host: "0.0.0.0"
```

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
