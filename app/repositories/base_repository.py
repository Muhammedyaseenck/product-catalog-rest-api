from psycopg2 import sql

from app.db import get_cursor


class BaseRepository:
    """Generic data-access class for a single table.

    Subclasses can override methods when they need joins or custom queries.
    """

    def __init__(self, table_name, columns):
        """
        :param table_name: database table name
        :param columns: writable columns, in insert/update order
        """
        self.table_name = table_name
        self.columns = columns

    def find_all(self):
        query = sql.SQL("SELECT * FROM {table} ORDER BY id").format(
            table=sql.Identifier(self.table_name)
        )
        with get_cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def find_by_id(self, record_id):
        query = sql.SQL("SELECT * FROM {table} WHERE id = %s").format(
            table=sql.Identifier(self.table_name)
        )
        with get_cursor() as cursor:
            cursor.execute(query, (record_id,))
            return cursor.fetchone()

    def create(self, data):
        query = sql.SQL(
            "INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING *"
        ).format(
            table=sql.Identifier(self.table_name),
            columns=sql.SQL(", ").join(map(sql.Identifier, self.columns)),
            placeholders=sql.SQL(", ").join([sql.Placeholder()] * len(self.columns)),
        )
        with get_cursor() as cursor:
            cursor.execute(query, self._extract_values(data))
            return cursor.fetchone()

    def update(self, record_id, data):
        assignments = sql.SQL(", ").join(
            sql.SQL("{} = %s").format(sql.Identifier(column))
            for column in self.columns
        )
        query = sql.SQL(
            "UPDATE {table} SET {assignments}, updated_at = NOW() "
            "WHERE id = %s RETURNING *"
        ).format(table=sql.Identifier(self.table_name), assignments=assignments)
        with get_cursor() as cursor:
            cursor.execute(query, [*self._extract_values(data), record_id])
            return cursor.fetchone()

    def delete(self, record_id):
        query = sql.SQL("DELETE FROM {table} WHERE id = %s").format(
            table=sql.Identifier(self.table_name)
        )
        with get_cursor() as cursor:
            cursor.execute(query, (record_id,))
            return cursor.rowcount > 0

    def _extract_values(self, data):
        return [data.get(column) for column in self.columns]