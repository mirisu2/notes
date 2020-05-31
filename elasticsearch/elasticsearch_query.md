## SQL access
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
  WHERE netflow.exporter.timestamp BETWEEN '2020-05-31T10:47:00'
  AND '2020-05-31T10:49:00' GROUP BY source.ip ORDER BY ssb DESC LIMIT 10
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
```
