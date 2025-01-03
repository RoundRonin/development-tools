from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class ArticleCreate(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, title=None, content=None, author=None, tags=None):  # noqa: E501
        """ArticleCreate - a model defined in OpenAPI

        :param title: The title of this ArticleCreate.  # noqa: E501
        :type title: str
        :param content: The content of this ArticleCreate.  # noqa: E501
        :type content: str
        :param author: The author of this ArticleCreate.  # noqa: E501
        :type author: str
        :param tags: The tags of this ArticleCreate.  # noqa: E501
        :type tags: List[str]
        """
        self.openapi_types = {
            'title': str,
            'content': str,
            'author': str,
            'tags': List[str]
        }

        self.attribute_map = {
            'title': 'title',
            'content': 'content',
            'author': 'author',
            'tags': 'tags'
        }

        self._title = title
        self._content = content
        self._author = author
        self._tags = tags

    @classmethod
    def from_dict(cls, dikt) -> 'ArticleCreate':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ArticleCreate of this ArticleCreate.  # noqa: E501
        :rtype: ArticleCreate
        """
        return util.deserialize_model(dikt, cls)

    @property
    def title(self) -> str:
        """Gets the title of this ArticleCreate.


        :return: The title of this ArticleCreate.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title: str):
        """Sets the title of this ArticleCreate.


        :param title: The title of this ArticleCreate.
        :type title: str
        """
        if title is None:
            raise ValueError("Invalid value for `title`, must not be `None`")  # noqa: E501

        self._title = title

    @property
    def content(self) -> str:
        """Gets the content of this ArticleCreate.


        :return: The content of this ArticleCreate.
        :rtype: str
        """
        return self._content

    @content.setter
    def content(self, content: str):
        """Sets the content of this ArticleCreate.


        :param content: The content of this ArticleCreate.
        :type content: str
        """
        if content is None:
            raise ValueError("Invalid value for `content`, must not be `None`")  # noqa: E501

        self._content = content

    @property
    def author(self) -> str:
        """Gets the author of this ArticleCreate.


        :return: The author of this ArticleCreate.
        :rtype: str
        """
        return self._author

    @author.setter
    def author(self, author: str):
        """Sets the author of this ArticleCreate.


        :param author: The author of this ArticleCreate.
        :type author: str
        """
        if author is None:
            raise ValueError("Invalid value for `author`, must not be `None`")  # noqa: E501

        self._author = author

    @property
    def tags(self) -> List[str]:
        """Gets the tags of this ArticleCreate.


        :return: The tags of this ArticleCreate.
        :rtype: List[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags: List[str]):
        """Sets the tags of this ArticleCreate.


        :param tags: The tags of this ArticleCreate.
        :type tags: List[str]
        """

        self._tags = tags
