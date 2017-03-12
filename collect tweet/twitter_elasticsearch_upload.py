from elasticsearch import Elasticsearch

esclient = Elasticsearch(
    [{'host': 'search-twittmap-wf-tos22nd6jgkyhdhvbptnb4pv7a.us-east-1.es.amazonaws.com', 'port': 80}])

response = esclient.search(
    index='social-*',
    body={
        "query": {
            "match": {
                "message": "myProduct"
            }
        },
        "aggs": {
            "top_10_states": {
                "terms": {
                    "field": "state",
                    "size": 10
                }
            }
        }
    })
