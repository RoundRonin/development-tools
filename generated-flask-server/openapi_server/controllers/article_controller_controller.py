import connexion
from typing import Dict, List, Tuple, Union
from datetime import datetime

from openapi_server.models.article import Article  # noqa: E501
from openapi_server.models.article_create import ArticleCreate  # noqa: E501
from openapi_server.models.article_update import ArticleUpdate  # noqa: E501
from openapi_server import util

def create_article():  # noqa: E501
    """create_article

    Create a new article # noqa: E501

    :param article_create: 
    :type article_create: dict | bytes

    :rtype: Union[Article, Tuple[Article, int], Tuple[Article, int, Dict[str, str]]]
    """
    if connexion.request.is_json:
        article_create = ArticleCreate.from_dict(connexion.request.get_json())  # noqa: E501
        if connexion.request.is_json: article_create = ArticleCreate.from_dict(connexion.request.get_json()) # noqa: E501 
        else: 
            return {"message": "Invalid input"}, 400 

        if not article_create.title or not article_create.content or not article_create.author:
            return {"message": "Invalid input"}, 400

        new_article = Article(
            id="12345",
            title=article_create.title,
            content=article_create.content,
            author=article_create.author,
            tags=article_create.tags,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        return new_article, 201


def delete_article(id_):  # noqa: E501
    """delete_article

    Delete an article by its ID # noqa: E501

    :param id: 
    :type id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]]
    """
    print(f"Received ID: {id_}")
    return id_, 200


def get_article_by_id(id_):  # noqa: E501
    """get_article_by_id

    Retrieve a specific article by its ID # noqa: E501

    :param id: 
    :type id: str

    :rtype: Union[Article, Tuple[Article, int], Tuple[Article, int, Dict[str, str]]]
    """
    article = Article(
        id=id_,
        title="The Evolution of Special Effects in Sci-Fi",
        content="Special effects have transformed the way we experience movies...",
        author="Ridley Scott",
        tags=["special effects", "sci-fi"],
        created_at="2024-01-01T03:54:00Z",
        updated_at="2024-01-01T03:54:00Z"
    )
    return article, 200


def get_article_names(author=None, tag=None, _date=None):  # noqa: E501
    """get_article_names

    Retrieve a list of article names # noqa: E501

    :param author: 
    :type author: str
    :param tag: 
    :type tag: str
    :param _date: 
    :type _date: str

    :rtype: Union[List[str], Tuple[List[str], int], Tuple[List[str], int, Dict[str, str]]]
    """
    articles = [
        "The Art of Storytelling in 'Inception'",
        "Directing Masterpieces: The Nolan Method",
        "Revolutionizing Cinema: The Impact of 'Interstellar'"
    ]
    return articles, 200


def get_popular_articles(_date=None, tag=None):  # noqa: E501
    """get_popular_articles

    Retrieve popular articles # noqa: E501

    :param _date: 
    :type _date: str
    :param tag: 
    :type tag: str

    :rtype: Union[List[Article], Tuple[List[Article], int], Tuple[List[Article], int, Dict[str, str]]]
    """
    popular_articles = [
        Article(
            id="12345",
            title="The Evolution of Special Effects in Sci-Fi",
            content="Special effects have transformed the way we experience movies...",
            author="Ridley Scott",
            tags=["special effects", "sci-fi"],
            created_at="2024-01-01T03:54:00Z",
            updated_at="2024-01-01T03:54:00Z"
        )
    ]
    return popular_articles, 200


def search_articles(query):  # noqa: E501
    """search_articles

    Search articles based on a query # noqa: E501

    :param query: 
    :type query: str

    :rtype: Union[List[Article], Tuple[List[Article], int], Tuple[List[Article], int, Dict[str, str]]]
    """
    searched_articles = [
        Article(
            id="12345",
            title="The Evolution of Special Effects in Sci-Fi",
            content="Special effects have transformed the way we experience movies...",
            author="Ridley Scott",
            tags=["special effects", "sci-fi"],
            created_at="2024-01-01T03:54:00Z",
            updated_at="2024-01-01T03:54:00Z"
        )
    ]
    return searched_articles, 200


def update_article(id_, article_update):  # noqa: E501
    """update_article

    Update an article by its ID # noqa: E501

    :param id: 
    :type id: str
    :param article_update: 
    :type article_update: dict | bytes

    :rtype: Union[Article, Tuple[Article, int], Tuple[Article, int, Dict[str, str]]]
    """
    if connexion.request.is_json:
        article_update = ArticleUpdate.from_dict(connexion.request.get_json())  # noqa: E501
    updated_article = Article(
        id=id_,
        title=article_update.title,
        content=article_update.content,
        author="Ridley Scott",
        tags=article_update.tags,
        created_at="2024-01-01T03:54:00Z",
        updated_at=datetime.now().isoformat()
    )
    return updated_article, 200

