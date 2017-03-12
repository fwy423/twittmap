from elasticsearch import Elasticsearch

def upload(elastic_host, json_data, index='tweet', doc_type='tweet_data'):
    esclient = Elasticsearch([{'host': elastic_host, 'port': 80}])
    response = esclient.index(index=index,
                   doc_type=doc_type,
                   body=json_data)
    print(response["created"])


def search(elastic_host, key_word, index='tweet', doc_type='tweet_data'):
    esclient = Elasticsearch([{'host': elastic_host, 'port': 80}])
    response = esclient.search(index=index,
                   doc_type=doc_type,
                   body={"query": {"match":{"text": key_word}}})
    print("Got %d Hits:" % response['hits']['total'])
    for hit in response['hits']['hits']:
        print("%(location)s \n%(timestamp)s \n%(user_name)s \n%(text)s" % hit["_source"])


# elastic_host = "search-twittmap-wf-tos22nd6jgkyhdhvbptnb4pv7a.us-east-1.es.amazonaws.com"
#
# esclient = Elasticsearch([{'host': elastic_host, 'port': 80}])
#
# response = esclient.search(
#     index='social-*',
#     body={
#         "query": {
#             "match": {
#                 "message": "myProduct"
#             }
#         },
#         "aggs": {
#             "top_10_states": {
#                 "terms": {
#                     "field": "state",
#                     "size": 10
#                 }
#             }
#         }
#     })
