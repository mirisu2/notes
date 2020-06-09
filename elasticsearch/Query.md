> By default, you cannot page through more than 10,000 documents using the `from` and `size` parameters. This limit is set using the [`index.max_result_window`](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules.html#index-max-result-window) index setting.

> By default, Elasticsearch sorts matching search results by *relevance score*, which measures how well each document matches a query. Score calculation also depends on whether the query clause is run in a *query* or *filter* context.
* In the *query* context, a query clause answers the question “How well does this document match this query clause?”
* In a *filter* context, a query clause answers the question “Does this document match this query clause?”

> By default, a [cross-cluster](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cross-cluster-search.html) search returns an error if any cluster in the request is unavailable. To skip an unavailable cluster during a cross-cluster search, set the `skip_unavailable` cluster setting to true.

> Query clauses behave differently depending on whether they are used in `query` context or `filter` context.

> In Elasticsearch, the deleted document is not removed from disk, but is marked as deleted (and referred to as a tombstone). To free up space, you need to `forcemerge` to purge deleted documents.

> `prefix` Can only use prefix queries on `keyword` and `text` fields - not on [netflow.source_ipv4_address] which is of type [ip]

> `wildcard` Can only use wildcard queries on keyword and text fields - not on [netflow.destination_ipv4_address] which is of type [ip]

> To better search `text` fields, the `match query` also analyzes your provided search term before performing a search. This means the `match query` can search `text` fields for analyzed tokens rather than an exact term.

### Compound queries
#### Boolean query 
* `must` - The clause (query) must appear in matching documents and will contribute to the score.
* `filter` - The clause (query) must appear in matching documents. However unlike must the score of the query will be ignored.
* `should` - The clause (query) should appear in the matching document.
* `must_not` - The clause (query) must not appear in the matching documents. 

> the better while the `must_not` and `filter` clauses are executed in filter context.

> The `constant_score` query assigns a score of 1.0 to all documents matched by the filter.

> [Boosting](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-boosting-query.html) query - positive/negative(Query used to decrease the relevance score of matching documents.)

```
# "_score" : 1.0
GET filebeat-7.7.0-*/_search
{
  "query": {
    "term": { "netflow.source_ipv4_address": "nnn.nnn.nnn.178" }
  }
}

# "_score" : 0.0
GET filebeat-7.7.0-*/_search
{
  "query": {
    "bool": {
      "filter": { "term": { "netflow.source_ipv4_address": "nnn.nnn.nnn.178" } }
    }
  }
}

# "_score" : 1.0
GET filebeat-7.7.0-*/_search
{
  "query": {
    "bool": {
      "must": { "term": { "netflow.source_ipv4_address": "nnn.nnn.nnn.178" } }
    }
  }
}

# match_all возвращает все документы и присваивает им по умолчанию "_score" : 1.0
GET filebeat-7.7.0-*/_search
{
  "query": {
    "bool": {
      "must": {
        "match_all": {}
      },
      "filter": { "term": { "netflow.source_ipv4_address": "nnn.nnn.nnn.178" } }
    }
  }
}

# "_score" : 1.0
GET filebeat-7.7.0-*/_search
{
  "query": { 
    "bool": { 
      
      "must": [
        { "term": { "netflow.source_ipv4_address": "nnn.nnn.nnn.178" }}
      ],
      
      "filter": [ 
        { "term":  { "netflow.destination_ipv4_address": "169.254.169.254" }}
      ]
      
    }
  }
}

# "_score" : 1.0
GET filebeat-7.7.0-*/_search
{
  "_source": ["netflow.source_ipv4_address", "netflow.destination_ipv4_address", "source.as.number"],
  "query": { 
    "bool": { 
      "must": [
        { "term": { "netflow.source_ipv4_address": "nnn.nnn.nnn.178" }}
      ],
      "filter": [
        { "term": { "source.as.number": "234234" } }, 
        { "range": { "netflow.destination_ipv4_address": {
            "gte": "192.204.0.0",
            "lte": "192.204.255.255"
          }}}
      ]
    }
  }
}

# "_score" : 1.0
GET filebeat-7.7.0-*/_search
{
  "_source": ["netflow.source_ipv4_address", "netflow.destination_ipv4_address", "source.as.number"],
  "query": { 
    "bool": { 
      "must": [
        { "term": { "netflow.source_ipv4_address": "nnn.nnn.nnn.178" }}
      ],
      "must_not": [
        { "range": { "netflow.destination_ipv4_address": {
            "gte": "192.204.0.0",
            "lte": "192.204.255.255"
          }}}
      ]
    }
  }
}

# "_score" : 1.0
GET filebeat-7.7.0-*/_search
{
  "query": {
    "constant_score": {
      "filter":  {  "term":  { "netflow.destination_ipv4_address": "169.254.169.254" } }
    }
  }
}

# Last 20 ssh logins
GET syslog_sshd_*/_search
{
  "_source": ["timestamp", "host", "UserName", "FromHost", "method"], 
  "size": 20, 
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "@timestamp": {
        "order": "desc"
      }
    }
  ]
}
```
### [Full text](https://stackoverflow.com/questions/26001002/elasticsearch-difference-between-term-match-phrase-and-query-string#:~:text=term%20query%20matches%20a%20single,the%20value%20is%20not%20analyzed.&text=match_phrase%20query%20will%20analyze%20the,order%20as%20the%20input%20value) queries
* [`match_phrase`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query-phrase.html)
* [`match`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html) - Returns documents that match a provided text, number, date or boolean value. The provided text is analyzed before matching.
* [`multi_match`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html)
* [`common`](elastic.co/guide/en/elasticsearch/reference/current/query-dsl-common-terms-query.html#_the_problem)
* [`query_string`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html)
* [`simple_query_string`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-simple-query-string-query.html)


### [Term-level queries](https://www.elastic.co/guide/en/elasticsearch/reference/current/term-level-queries.html)
You can use term-level queries to find documents based on precise values in structured data. Examples of structured data include date **ranges**, **IP addresses**, **prices**, or **product IDs**.
* [`exists`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-exists-query.html) - вернет документы где есть искомое поле! 
```
GET /_search
{
    "query": {
        "exists": { "field": "UserName" }
    }
}
```
* [`ids`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-ids-query.html)
```
GET /_search
{
    "query": {
        "ids" : { "values" : ["1", "4", "100"] }
    }
}
```
* [`prefix`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-prefix-query.html)
* [`range`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-range-query.html)
* [`regexp`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-regexp-query.html) [regular expression syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/regexp-syntax.html)
```
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
```
* [`term`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html)
* [`terms`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-terms-query.html)
```
GET /_search
{
    "query" : {
        "terms" : {
            "user" : ["kimchy", "elasticsearch"],
            "boost" : 1.0
        }
    }
}
```
* [`terms_set `](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-terms-set-query.html)
* [`wildcard`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-wildcard-query.html)
```
# The wildcard is very similar to a regular expression, but it has only two special characters
# *: This means match zero or more characters
# ?: This means match one character
POST /test/_search
{
  "query": {
    "wildcard": { "name": "????n" }
  }
}
```
### [Aggregations](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations.html)
```
"aggregations" : {
    "<aggregation_name>" : {
        "<aggregation_type>" : {
            <aggregation_body>
        }
        [,"meta" : {  [<meta_data_body>] } ]?
        [,"aggregations" : { [<sub_aggregation>]+ } ]?
    }
    [,"<aggregation_name_2>" : { ... } ]*
}
```
* [`Bucket aggregations`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket.html)
> Bucket aggregations, as opposed to metrics aggregations, can hold sub-aggregations. These sub-aggregations will be aggregated for the buckets created by their "parent" bucket aggregation.

[composite aggregation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-composite-aggregation.html)
> The `sources` parameter controls the sources that should be used to build the composite buckets. The order that the `sources` are defined is important because it also controls the order the keys are returned.

There are three different types of values source:
* terms
* histogram 
* date_histogram 
> The `sources` parameter accepts an array of values source. It is possible to mix different values source to create composite buckets.

* [`Metrics aggregations`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics.html)
```
POST filebeat-7.7.0-*/_search
{
  "size" : 0,
  "_source" : false,
  "query" : {
      "constant_score" : {
          "filter" : {
              "match" : { "netflow.source_ipv4_address" : "1.0.0.55" }
          }
      }
  },
  "aggs" : {
      "network_bytes" : { "sum" : { "field" : "network.bytes" } },
      "network_packets" : { "sum" : { "field" : "network.packets" } },
      "flow_count" : { "value_count" : { "field" : "network.bytes" } }
  }
}
```
* [`Pipeline aggregations`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline.html)






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
