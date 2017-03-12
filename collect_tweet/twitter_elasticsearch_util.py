from elasticsearch import Elasticsearch


def upload(elastic_host, json_data, index='tweet', doc_type='tweet_data'):
    """
    :param elastic_host: the host name of your Elasticsearch

    :param json_data: the ready-to-upload data

    :param index: the index of your data

    :param doc_type: document type of your data

    :return: True for success
    """

    esclient = Elasticsearch([{'host': elastic_host, 'port': 80}])
    response = esclient.index(index=index,
                              doc_type=doc_type,
                              body=json_data)
    if response["created"] == "True":
        return True
    return False


def search(elastic_host, key_word, index='tweet', doc_type='tweet_data'):
    """
    :param elastic_host: the host name of your Elasticsearch

    :param key_word: what feature of ready-to-delete data that contains

    :param index: the index of your data

    :param doc_type: document type of your data

    :return: the search result, presenting in json
    """

    esclient = Elasticsearch([{'host': elastic_host, 'port': 80}])
    response = esclient.search(index=index,
                               doc_type=doc_type,
                               body={"query": {"match": {"text": key_word}}})
    print("Got %d Hits:" % response['hits']['total'])
    result = []
    for hit in response['hits']['hits']:
        print("%(location)s \n%(timestamp)s \n%(user_name)s \n%(text)s\n" % hit["_source"])
        result.append(hit["_source"])
    output = json.dumps({"result": result})

    return output


def clear(elastic_host, key_word="All", index='tweet', doc_type='tweet_data'):
    """
    :param elastic_host: the host name of your Elasticsearch

    :param key_word: what feature of ready-to-delete data that contains

    :param index: the index of your data

    :param doc_type: document type of your data

    :return: the numbers that deleted
    """
    esclient = Elasticsearch([{'host': elastic_host, 'port': 80}])

    if key_word == "All":
        query = {"match_all": {}}
    else:
        query = {"match": {"text": key_word}}

    response = esclient.delete_by_query(index=index,
                                        doc_type='tweet_data',
                                        body={"query": query})
    return response["deleted"]

# elastic_host = "search-twittmap-wf-tos22nd6jgkyhdhvbptnb4pv7a.us-east-1.es.amazonaws.com"
