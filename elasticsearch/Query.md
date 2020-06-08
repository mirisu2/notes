> By default, you cannot page through more than 10,000 documents using the `from` and `size` parameters. This limit is set using the [`index.max_result_window`](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules.html#index-max-result-window) index setting.

> By default, Elasticsearch sorts matching search results by *relevance score*, which measures how well each document matches a query. Score calculation also depends on whether the query clause is run in a *query* or *filter* context.

> By default, a [cross-cluster](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cross-cluster-search.html) search returns an error if any cluster in the request is unavailable. To skip an unavailable cluster during a cross-cluster search, set the `skip_unavailable` cluster setting to true.

> Query clauses behave differently depending on whether they are used in `query` context or `filter` context.

### Chapter 3
```
DELETE authors
PUT authors
{
  "mappings": {
    "properties": { "name": {"type": "keyword"}, "job": {"type": "integer"} }
  }
}
POST authors/_bulk
{ "index":{ "_index": "authors" } }
{ "name":"Alice","job":7 }
{ "index":{ "_index": "authors" } }
{ "name":"Alice","job":3 }
{ "index":{ "_index": "authors" } }
{ "name":"Alice","job":5 }
{ "index":{ "_index": "authors" } }
{ "name":"Alice","job":4 }
GET /authors/_search
GET /authors/_search
{
  "_source": {
    "includes": ["job"],
    "excludes": ["name"]
  }, 
  "query": {
    "term": {
      "name": {
        "value": "Alice"
      }
    }
  },
  "sort": [
    {
      "job": {
        "order": "desc"
      }
    }
  ]
}





GET syslog_sshd_2020.05.31/_search
{
  "_source": ["host", "UserName", "FromHost", "method"], 
  "query": {
    "match_all": {}
  }
}
GET syslog_sshd_2020.05.31/_search
{
  "_source": ["host", "UserName", "FromHost", "method"], 
  "query": {
    "match": {
      "UserName": "ast"
    }
  }
}
GET syslog_sshd_2020.05.31/_search
{
  "_source": ["host", "UserName", "FromHost", "method"], 
  "query": {
    "term": {
      "UserName": "ast"
    }
  }
}
GET syslog_sshd_2020.05.31/_search
{
  "_source": ["host", "UserName", "FromHost", "method"], 
  "query": {
    "prefix": {
      "UserName": "as"
    }
  }
}





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
{ "name":"Paul", "age":35 }

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
### Chapter 4
```
GET /mybooks/_search
{
  "query": {
    "match_all": {}
  }
}

GET /test/_search?q=age:35&explain=true

GET /test/_search?pretty=true
{
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "age": {
        "order": "desc",
      }
    }
  ]
}

# Highlighting results
# подсветка найденного слова в большом выводе

# scrolling query
# пагинация

# Count result
GET /filebeat-7.7.0-*/_count?q=destination.ip:1.1.1.1
GET /test/_count?q=age:35
{
  "count" : 2,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  }
}

DELETE /mybooks,test/_delete_by_query
POST /test/_delete_by_query?q=age:35

POST /test/_update_by_query
{
  "query": {
    "match": {
      "name": "Paul"
    }
  },
  "script": {
    "source": "ctx._source.age=25"
  }
}

POST /test/_update_by_query
{
  "query": {
    "match_all": {}
  },
  "script": {
    "source": "ctx._source.age=17"
  }
}
{
  "took" : 30,
  "timed_out" : false,
  "total" : 3,
  "updated" : 3,
  "deleted" : 0,
  "batches" : 1,
  "version_conflicts" : 0,
  "noops" : 0,
  "retries" : {
    "bulk" : 0,
    "search" : 0
  },
  "throttled_millis" : 0,
  "requests_per_second" : -1.0,
  "throttled_until_millis" : 0,
  "failures" : [ ]
}

# For executing a term query as a filter, we need to use it wrapped in a Boolean query. 
# Using a Boolean query
# must, must_not, should, filter
POST /test/_search
{
  "query": {
    "bool": {
      "must": [
        {"term": {
          "age": {
            "value": 25
          }
        }}
      ]
    }
  }
}

POST /test/_search
{
  "query": {
    "bool": {
      "must": [
        {"term": {
          "age": {
            "value": 25
          }
        }}
      ],
      "must_not": [
        {
          "term": {
            "name": {
              "value": "Alice"
            }
          }
        }
      ]
    }
  }
}

POST /test/_search
{
  "query": {
    "bool": {
    
      "must": [
        { "term": { "age": 25 } },
        { "term": { "name": "Jeck" } }
      ],
      
      "must_not": [ 
        { "term": { "name": { "value": "Alice" } } } 
      ]
      
    }
  }
}
```
### Chapter 5
```
POST /test/_search
{
  "query": {
    "term": { "age": 25 }
  }
}
# OR (кмк c фильтром быстрее идет поиск)
POST /test/_search
{
  "query": {
    "bool": {
      "filter": {
        "term": { "age": 25 }
      }
    }
  }
}

GET /test/_search
{
  "query": {
    "terms": {
      "age": [17, 55]
    }
  }
}

# вложенные селекты стр.217

GET /filebeat-7.7.0-*/_search?size=1
GET /filebeat-7.7.0-*/_search
{
  "size": 2,
  "query": {
    "prefix": { "destination.as.organization.name": "YAND" }
  }
}
# reverse_analyzer стр.222

# The wildcard is very similar to a regular expression, but it has only two special characters
# *: This means match zero or more characters
# ?: This means match one character
POST /test/_search
{
  "query": {
    "wildcard": { "name": "????n" }
  }
}

# To speed up a regexp query, a good approach is to have a regular expression that doesn't start with a wildcard
# To avoid poor performance in a search, don't execute regex starting with .*. Instead, use a prefix query on a 
# string processed with a reverse analyzer.
POST /mybooks/_search
{
  "query": {
    "regexp": {
      "description": {
        "value": "j.*",
        "flags": "INTERSECTION|COMPLEMENT|EMPTY"
      }
    }
  }
}

# match...
POST /mybooks/_search
{
  "query": {
    "match": {
      "description": {
        "query": "nice guy",
        "operator": "and"
      }
    }
  }
}

POST /mybooks/_search
{
  "query": {
    "match_phrase": {
      "description": "nice guy"
    }
  }
}

POST /mybooks/_search
{
  "query": {
    "match_phrase_prefix": {
      "description": "nice gu"
    }
  }
}

# параметры стр. 238
POST /mybooks/_search
{
  "query": {
    "multi_match": {
      "fields": [
        "description",
        "name"
      ],
      "query": "Bill",
      "operator": "and"
    }
  }
}

# query_string

GET /filebeat-7.7.0-*/_count
{
  "query": {
    "bool": {
      "filter": {
        "range": {
          "destination.ip": {
            "gte": "1.1.1.0",
            "lte": "1.1.1.255"
          }
        }
      }
    }
  }
}
GET /filebeat-7.7.0-*/_search
{
  "size": 1,
  "query": {
    "bool": {
      "filter": {
        "range": {
          "destination.ip": {
            "gte": "1.1.1.0",
            "lte": "1.1.1.255"
          }
        }
      }
    }
  }
}

"range": {
  "timestamp": {
    "from": "2014-01-01",
    "to": "2015-01-01",
    "include_lower": true,
    "include_upper": false
  }
}

# common стр.251

# The IDs query allows matching documents by their IDs
POST /mybooks/_search
{
"query": {
  "ids": {
    "type": "test-type",
      "values": [
        "1",
        "2",
        "3"
      ]
    }
  }
}

POST /mybooks/_search
{
  "query": {
    "exists": {
      "field": "description"
    }
  }
}
POST /mybooks/_search
{
  "query": {
    "bool": {
      "must_not": {
        "exists": {
          "field": "description"
        }
      }
    }
  }
}
```
### Chapter 7 (Aggregations)
```
# стр 292
POST filebeat-7.7.0-2020.06.07-000057/_search?size=0
{
  "aggs": {
    "source_bytes_stats": {
      "sum": { "field": "source.bytes" }
    }
  }
}

POST test/_search?size=0
{
  "aggs": {
    "my_age_stats": {
      "extended_stats": {
        "field": "age"
      }
    }
  }
}
{
...
  "aggregations" : {
    "age_stats" : {
      "count" : 7,
      "min" : 17.0,
      "max" : 55.0,
      "avg" : 27.857142857142858,
      "sum" : 195.0,
      "sum_of_squares" : 6439.0,
      "variance" : 143.8367346938776,
      "std_deviation" : 11.993195349608778,
      "std_deviation_bounds" : {
        "upper" : 51.84353355636041,
        "lower" : 3.8707521579253026
      }
    }
  }
}

POST filebeat-7.7.0-2020.06.07-000059/_search?size=0
{
  "aggs": {
    "top10_source": {
      "ip_range": {
        "field": "source.ip",
        "ranges": [
        {
          "to": nnn.nnn.n1.255"
        },
        {
          "from": "nnn.nnn.n6.0"
        }
        ]
      }
    }
  }
}

POST filebeat-7.7.0-2020.06.07-000059/_search?size=0
{
  "aggs": {
    "my_ip_range": {
      "ip_range": {
        "field": "source.ip",
        "ranges": [
        {
          "mask": "nnn.nnn.nnn.0/22"
        } 
        ]
      }
    }
  }
}


```
