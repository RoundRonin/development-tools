import connexion
from typing import Dict, List, Tuple, Union
from datetime import datetime
from opentelemetry import trace
from flask_sqlalchemy import SQLAlchemy

from openapi_server.models.article import Article as ApiArticle  # noqa: E501
from openapi_server.models.article_create import ArticleCreate as ApiArticleCreate  # noqa: E501
from openapi_server.models.article_update import ArticleUpdate as ApiArticleUpdate  # noqa: E501
from openapi_server.DAL.models import Article, ArticleCreate, ArticleUpdate
from openapi_server.DAL.database import db
from openapi_server.services.prometheus_service import ACTIVE_ARTICLE_COUNT, PRODUCT_COUNT

tracer = trace.get_tracer(__name__)

def create_article():  # noqa: E501
    """create_article

    Create a new article # noqa: E501

    :param article_create: 
    :type article_create: dict | bytes

    :rtype: Union[ApiArticle, Tuple[ApiArticle, int], Tuple[ApiArticle, int, Dict[str, str]]]
    """
    with tracer.start_as_current_span("create_article") as span:
        if connexion.request.is_json:
            with tracer.start_as_current_span("parse_request"):
                api_article_create = ApiArticleCreate.from_dict(connexion.request.get_json())  # noqa: E501

            if not api_article_create.title or not api_article_create.content or not api_article_create.author:
                span.set_attribute("error", True)
                span.set_attribute("error.message", "Invalid input")
                return {"message": "Invalid input"}, 400

            with tracer.start_as_current_span("add_article_to_db"):
                new_article = Article(
                    title=api_article_create.title,
                    content=api_article_create.content,
                    author=api_article_create.author,
                    tags=api_article_create.tags,
                )
                db.session.add(new_article)
                db.session.commit()
                db.session.refresh(new_article)
                span.set_attribute("article.id", new_article.id)

                PRODUCT_COUNT.labels(product_type=new_article.tags[0] if new_article.tags else 'unknown').inc()
                ACTIVE_ARTICLE_COUNT.inc()

            with tracer.start_as_current_span("build_response"):
                response_article = ApiArticle(
                    id=new_article.id,
                    title=new_article.title,
                    content=new_article.content,
                    author=new_article.author,
                    tags=new_article.tags,
                )
            return response_article, 201


def delete_article(id_):  # noqa: E501
    """delete_article

    Delete an article by its ID # noqa: E501

    :param id: 
    :type id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]]
    """
    with tracer.start_as_current_span("delete_article") as span:
        with tracer.start_as_current_span("get_article_from_db"):
            db_article = Article.query.filter(Article.id == id_).first()
            if not db_article:
                span.set_attribute("error", True)
                span.set_attribute("error.message", "Article not found")
                return {"message": "Article not found"}, 404

        with tracer.start_as_current_span("delete_article_from_db"):
            db.session.delete(db_article)
            db.session.commit()
            span.set_attribute("article.id", id_)

            ACTIVE_ARTICLE_COUNT.inc()
        return {"message": "Article deleted"}, 200

def get_article_by_id(id_):  # noqa: E501
    """get_article_by_id

    Retrieve a specific article by its ID # noqa: E501

    :param id: 
    :type id: str

    :rtype: Union[ApiArticle, Tuple[ApiArticle, int], Tuple[ApiArticle, int, Dict[str, str]]]
    """
    with tracer.start_as_current_span("get_article_by_id") as span:
        with tracer.start_as_current_span("get_article_from_db"):
            db_article = Article.query.filter(Article.id == id_).first()
            if not db_article:
                span.set_attribute("error", True)
                span.set_attribute("error.message", "Article not found")
                return {"message": "Article not found"}, 404
            span.set_attribute("article.id", id_)

        with tracer.start_as_current_span("build_response"):
            response_article = ApiArticle(
                id=db_article.id,
                title=db_article.title,
                content=db_article.content,
                author=db_article.author,
                tags=db_article.tags,
            )
        return response_article, 200

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
    with tracer.start_as_current_span("get_article_names") as span:
        with tracer.start_as_current_span("query_articles_from_db"):
            query = Article.query.with_entities(Article.title)
            if author:
                query = query.filter(Article.author == author)
            if tag:
                query = query.filter(Article.tags.contains([tag]))
            if _date:
                query = query.filter(Article.created_at == _date)
            articles = query.all()
            span.set_attribute("author", author or "unknown")
            span.set_attribute("tag", tag or "unknown")
            span.set_attribute("_date", _date or "unknown")
        return [article.title for article in articles], 200

def get_popular_articles(_date=None, tag=None):  # noqa: E501
    """get_popular_articles

    Retrieve popular articles # noqa: E501

    :param _date: 
    :type _date: str
    :param tag: 
    :type tag: str

    :rtype: Union[List[ApiArticle], Tuple[List[ApiArticle], int], Tuple[List[ApiArticle], int, Dict[str, str]]]
    """
    with tracer.start_as_current_span("get_popular_articles") as span:
        with tracer.start_as_current_span("query_popular_articles_from_db"):
            query = Article.query
            if tag:
                query = query.filter(Article.tags.contains([tag]))
            if _date:
                query = query.filter(Article.created_at == _date)
            popular_articles = query.all()
            span.set_attribute("_date", _date or "unknown")
            span.set_attribute("tag", tag or "unknown")

        with tracer.start_as_current_span("build_response"):
            response_articles = [ApiArticle(
                id=article.id,
                title=article.title,
                content=article.content,
                author=article.author,
                tags=article.tags,
            ) for article in popular_articles]
        return response_articles, 200

def search_articles(query):  # noqa: E501
    """search_articles

    Search articles based on a query # noqa: E501

    :param query: 
    :type query: str

    :rtype: Union[List[ApiArticle], Tuple[List[ApiArticle], int], Tuple[List[ApiArticle], int, Dict[str, str]]]
    """
    with tracer.start_as_current_span("search_articles") as span:
        with tracer.start_as_current_span("query_search_articles_from_db"):
            searched_articles = Article.query.filter(Article.title.ilike(f"%{query}%")).all()
            span.set_attribute("query", query)

        with tracer.start_as_current_span("build_response"):
            response_articles = [ApiArticle(
                id=article.id,
                title=article.title,
                content=article.content,
                author=article.author,
                tags=article.tags,
            ) for article in searched_articles]

        return response_articles, 200

def update_article(id_):  # noqa: E501
    """update_article

    Update an article by its ID # noqa: E501

    :param id: 
    :type id: str
    :param article_update: 
    :type article_update: dict | bytes

    :rtype: Union[ApiArticle, Tuple[ApiArticle, int], Tuple[ApiArticle, int, Dict[str, str]]]
    """
    with tracer.start_as_current_span("update_article") as span:
        if connexion.request.is_json:
            with tracer.start_as_current_span("parse_request"):
                api_article_update = ApiArticleUpdate.from_dict(connexion.request.get_json())  # noqa: E501
        with tracer.start_as_current_span("get_article_from_db"):
            db_article = Article.query.filter(Article.id == id_).first()
            if not db_article:
                span.set_attribute("error", True)
                span.set_attribute("error.message", "Article not found")
                return {"message": "Article not found"}, 404
        with tracer.start_as_current_span("update_article_in_db"):
            if api_article_update.title:
                db_article.title = api_article_update.title
            if api_article_update.content:
                db_article.content = api_article_update.content
            if api_article_update.tags:
                db_article.tags = api_article_update.tags
            db_article.updated_at = datetime.now()
            db.session.commit()
            db.session.refresh(db_article)
            span.set_attribute("article.id", id_)

        with tracer.start_as_current_span("build_response"):
            response_article = ApiArticle(
                id=db_article.id,
                title=db_article.title,
                content=db_article.content,
                author=db_article.author,
                tags=db_article.tags,
            )
        return response_article, 200