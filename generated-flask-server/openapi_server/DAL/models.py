from sqlalchemy.dialects.postgresql import ARRAY
from openapi_server.DAL.database import db
from datetime import datetime

class TimestampMixin:
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Article(TimestampMixin, db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String, nullable=False)
    tags = db.Column(ARRAY(db.String))

    def __init__(self, title, content, author, tags):
        self.title = title
        self.content = content
        self.author = author
        self.tags = tags

    def __repr__(self):
        return f"Article(title='{self.title}', content='{self.content}', author='{self.author}', tags={self.tags})"

class ArticleCreate(TimestampMixin, db.Model):
    __tablename__ = 'article_create'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String, nullable=False)
    tags = db.Column(ARRAY(db.String))

class ArticleUpdate(TimestampMixin, db.Model):
    __tablename__ = 'article_update'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    content = db.Column(db.Text)
    tags = db.Column(ARRAY(db.String))
