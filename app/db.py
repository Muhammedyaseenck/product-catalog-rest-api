from contextlib import contextmanager

from psycopg2 import pool
from psycopg2.extras import RealDictCursor

_connection_pool = None


def init_pool(database_url, min_connections=1, max_connections=10):
    """Create the shared PostgreSQL connection pool."""
    global _connection_pool
    _connection_pool = pool.ThreadedConnectionPool(
        min_connections, max_connections, dsn=database_url
    )


@contextmanager
def get_cursor():
    """Yield a dict cursor; commit on success, roll back on any error."""
    connection = _connection_pool.getconn()
    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            yield cursor
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        _connection_pool.putconn(connection)