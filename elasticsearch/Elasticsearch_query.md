### [SQL access](https://www.elastic.co/guide/en/elasticsearch/reference/7.7/xpack-sql.html)
```
POST /_sql?format=txt
{
  "query": """
  SELECT destination.ip, SUM(source.bytes)/1024/1024
  FROM "filebeat-7.7.0" 
  WHERE netflow.exporter.timestamp BETWEEN '2020-05-31T10:47:00' AND '2020-05-31T10:49:00' 
  AND source.ip='92.38.235.189' GROUP BY destination.ip  
  """
}
POST /_sql?format=txt
{
  "query": """
  SELECT source.ip, SUM(source.bytes) as ssb
  FROM "filebeat-7.7.0" 
  WHERE netflow.exporter.timestamp BETWEEN '2020-05-31T10:47:00' AND '2020-05-31T10:49:00' 
  GROUP BY source.ip ORDER BY ssb DESC LIMIT 10
  """
}

POST twitter/_delete_by_query?routing=1
{
  "query": {
    "range" : {
        "age" : {
           "gte" : 10
        }
    }
  }
}
POST /filebeat-7.7.0-2020.05.30-000001/_delete_by_query
{
  "query": {
    "match_all": {}
  }
}
{
  "query": """
  SELECT source.ip, ROUND(SUM(source.bytes)/1024/1024, 3) as ssb
  FROM "filebeat-7.7.0" 
  WHERE netflow.exporter.timestamp BETWEEN '2020-05-31T17:30:00' 
  AND '2020-05-31T21:40:00' 
  AND destination.ip='11.21.13.178' GROUP BY source.ip 
  """
}
```
