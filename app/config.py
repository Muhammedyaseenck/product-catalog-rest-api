import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DATABASE_URL = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/catalog_db"
    )
    DB_POOL_MIN = int(os.getenv("DB_POOL_MIN", "1"))
    DB_POOL_MAX = int(os.getenv("DB_POOL_MAX", "10"))