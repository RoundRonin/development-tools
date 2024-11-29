from sqlalchemy import inspect
from openapi_server.DAL.database import Base, engine
from openapi_server.DAL.models import Article, ArticleCreate, ArticleUpdate
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def init_db():
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        if not tables:
            logger.debug("No tables found. Initializing database...")
            Base.metadata.create_all(bind=engine)
            logger.debug("Database initialized successfully.")
        else:
            logger.debug("Tables already exist. Skipping initialization.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")

if __name__ == "__main__":
    init_db()
