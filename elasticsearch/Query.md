```
PUT test
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "test"
}

PUT /myindex
{
  "settings": {
    "index": {
      "number_of_shards": 2,
      "number_of_replicas": 1
    }
  },
  "mappings": {
    "properties": {
    ...
    }
  }
}

PUT test/_doc/1
{
  "name":"Paul", 
  "age":35
}
{
  "_index" : "test",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 1,
  "result" : "created",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 0,
  "_primary_term" : 1
}

# The pretty argument in the URL is optional, but very handy to print the response output prettily.
GET /myindex/_mapping?pretty
GET test/_mapping
{
  "test" : {
    "mappings" : {
      "properties" : {
        "age" : {
          "type" : "long"
        },
        "name" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        }
      }
    }
  }
}

GET index_1,index_2/_search

GET test/_search
{
  "took" : 0,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "test",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 1.0,
        "_source" : {
          "name" : "Paul",
          "age" : 35
        }
      }
    ]
  }
}

GET test/_doc/1
{
  "_index" : "test",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 1,
  "_seq_no" : 0,
  "_primary_term" : 1,
  "found" : true,
  "_source" : {
    "name" : "Paul",
    "age" : 35
  }
}

DELETE test
{
  "acknowledged" : true
}

PUT test
PUT test/_mapping
{
  "properties" : {
    "id" : {"type" : "keyword"},
    "date" : {"type" : "date"},
    "customer_id" : {"type" : "keyword"},
    "sent" : {"type" : "boolean"},
    "name" : {"type" : "keyword"},
    "quantity" : {"type" : "integer"},
    "price" : {"type" : "double"},
    "vat" : {"type" : "double", "index":"false"}
  }
}

POST /_reindex?pretty=true
{
  "source": {
    "index": "myindex"
  },
  "dest": {
    "index": "myindex2"
  }
}

POST /myindex/_refresh
{
  "_shards" : {
    "total" : 4,
    "successful" : 2,
    "failed" : 0
  }
}

POST /myindex/_doc/2qLrAfPVQvCRMe7Ku8r0Tw?refresh=true
{
  ...
}

POST /myindex/_flush
{
  "_shards" : {
    "total" : 4,
    "successful" : 2,
    "failed" : 0
  }
}

# In Elasticsearch, the deleted document is not removed from disk, but is marked as deleted (and referred to as a tombstone).
# To free up space, you need to forcemerge to purge deleted documents.
POST /myindex/_forcemerge
{
  "_shards" : {
    "total" : 4,
    "successful" : 2,
    "failed" : 0
  }
}

Shrinking an index
# Reducing the number of shards to reduce memory and resource usage.
# Reducing the number of shards to speed up searching.
GET /_nodes?pretty
GET /_cluster/health?pretty
...

HEAD /myindex/
200 - OK
HEAD /myindex1/
{"statusCode":404,"error":"Not Found","message":"404 - Not Found"}

GET /myindex/_settings?pretty=true
{
  "myindex" : {
    "settings" : {
      "index" : {
        "creation_date" : "1591538948999",
        "number_of_shards" : "2",
        "number_of_replicas" : "1",
        "uuid" : "gemRFLymRjGsvXeWzYUP9w",
        "version" : {
          "created" : "7070099"
        },
        "provided_name" : "myindex"
      }
    }
  }
}

PUT /myindex/_settings
{
  "index": { 
    "number_of_replicas": "2"
  }
}

GET /_aliases
GET /myindex/_alias
{
  "myindex" : {
    "aliases" : { }
  }
}
PUT /myindex/_alias/myalias1
DELETE /myindex/_alias/myalias1

GET /myindex/_doc/2qLrAfPVQvCRMe7Ku8r0Tw
GET /myindex/_doc/2qLrAfPVQvCRMe7Ku8r0Tw?_source=date,sent

# refresh allows us to refresh the current shard before performing the get operation 
# (it must be used with care because it slows down indexing and introduces some overhead)
GET /myindex/_doc/2qLrAfPVQvCRMe7Ku8r0Tw?refresh=true

# Elasticsearch chooses a random shard for the GET call.
# _primary - use for the primary shard
# _local - first trying the local shard and then falling back to a random choice
GET /myindex/_doc/2qLrAfPVQvCRMe7Ku8r0Tw?preference=_primary or _local

DELETE /myindex/_doc/2qLrAfPVQvCRMe7Ku8r0Tw
POST /filebeat-7.7.0-2020.06.04-000042/_delete_by_query
{
  "query": {
    "match_all": {}
  }
}

# Update
PUT test
PUT test/_doc/1
{
  "name":"Paul", 
  "age":35
}
GET test/_doc/1
POST /test/_update/1
{
  "script": { 
    "source": "ctx._source.name += params.name", # result: PaulJohn
    # "source": "ctx._source.name = params.name", # result: John
    "params": {
      "name" : "John"
    }
  }
}
# output:
{
  "_index" : "test",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 2,
  "result" : "updated",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 1,
  "_primary_term" : 1
}
OR
POST /test/_update/1
{
  "doc": {
    "name": "Alice"
  }
}


```
