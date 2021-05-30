from elasticsearch import Elasticsearch
from datetime import datetime

from django.conf import settings


class ElasticSearch:
    """
        ElasticSearch: save_notes, get_notes, delete_notes
    """
    def __init__(self):
        self.es = Elasticsearch(hosts=settings.ES_HOST, port=settings.ES_PORT)

    def save_data(self, title, description, user_id):
        """
            This method is used to save notes into elastic search index.
            :param title: It's accept title as parameter.
            :param description: It's accept description as parameter.
            :param user_id: It's accept user_id as parameter.
            :param note_id: It's accept note_id as parameter.
            :return: None
        """
        es_data = {
                'title': title,
                'description': description,
                'user_id': user_id,
                'created_on': datetime.now()
            }
        data = self.sort_data()
        if not data:
            doc_id = 1
        else:
            doc_id = int(data['_id']) + 1
        self.es.index(index='notes', id=doc_id, body=es_data)

    def get_data(self, user_id):
        """
            This method is used to get notes according to that user_id.
            :param user_id: It's accept user_id as parameter.
            :return: It's return search data.
        """
        query = {
            "query":{
                "term" : {"user_id": user_id}
            }
        }
        return self.es.search(index="notes", body=query)

    def delete_data(self, doc_id):
        """
            This method is used to delete notes by doc_id.
            :param doc_id: It's accept doc_id as parameter.
            :return: None
        """
        self.es.delete(index='notes', id=doc_id)

    def update_data(self, doc_id, es_data):
        """
            This method is used to update data by doc_id.
            :param doc_id: It's accept doc_id as parameter.
            :return: None
        """
        self.es.update(index='notes', id=doc_id, body=es_data)

    def sort_data(self):
        """
            This method is used to get notes according to that user_id.
            :param user_id: It's accept user_id as parameter.
            :return: It's return search data.
        """
        query = {
        "sort" : [
            {
                "created_on" : {"order" : "desc"}}
            ]
        }
        es_data = self.es.search(index="notes", body=query)
        return es_data['hits']['hits'][0]
