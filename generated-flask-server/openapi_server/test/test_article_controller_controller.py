import unittest

from flask import json

from openapi_server.models.article import Article  # noqa: E501
from openapi_server.models.article_create import ArticleCreate  # noqa: E501
from openapi_server.models.article_update import ArticleUpdate  # noqa: E501
from openapi_server.test import BaseTestCase


class TestArticleControllerController(BaseTestCase):
    """ArticleControllerController integration test stubs"""

    def test_create_article(self):
        """Test case for create_article

        
        """
        article_create = {"title":"The Evolution of Special Effects in Sci-Fi","content":"Special effects have transformed the way we experience movies, with advancements bringing unimaginable worlds to life...","author":"Ridley Scott","tags":["special effects","sci-fi"]}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/articles',
            method='POST',
            headers=headers,
            data=json.dumps(article_create),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_article(self):
        """Test case for delete_article

        
        """
        headers = { 
        }
        response = self.client.open(
            '/articles/{id}'.format(id='12345'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_article_by_id(self):
        """Test case for get_article_by_id

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/articles/{id}'.format(id='12345'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_article_names(self):
        """Test case for get_article_names

        
        """
        query_string = [('author', 'Christopher Nolan'),
                        ('tag', 'blockbuster'),
                        ('date', '2024-01-01')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/articles',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_popular_articles(self):
        """Test case for get_popular_articles

        
        """
        query_string = [('date', '2024-01-01'),
                        ('tag', 'blockbuster')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/articles/popular',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search_articles(self):
        """Test case for search_articles

        
        """
        query_string = [('query', 'cinematography in Blade Runner')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/articles/search',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_article(self):
        """Test case for update_article

        
        """
        article_update = {"title":"The Evolution of Special Effects in Sci-Fi (Updated)","content":"Special effects have transformed the way we experience movies, with advancements bringing unimaginable worlds to life. This update explores the latest technologies...","tags":["special effects","sci-fi","technology"]}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/articles/{id}'.format(id='12345'),
            method='PUT',
            headers=headers,
            data=json.dumps(article_update),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
