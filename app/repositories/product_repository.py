from app.db import get_cursor
from app.repositories.base_repository import BaseRepository

_SELECT_WITH_RELATIONS = """
    SELECT p.id, p.name, p.description, p.price, p.stock,
           p.category_id, c.name AS category_name,
           p.brand_id, b.name AS brand_name,
           p.created_at, p.updated_at
    FROM products p
    JOIN categories c ON c.id = p.category_id
    JOIN brands b ON b.id = p.brand_id
"""


class ProductRepository(BaseRepository):
    def __init__(self):
        super().__init__(
            "products",
            ["name", "description", "price", "stock", "category_id", "brand_id"],
        )

    def find_all(self):
        with get_cursor() as cursor:
            cursor.execute(f"{_SELECT_WITH_RELATIONS} ORDER BY p.id")
            return cursor.fetchall()

    def find_by_id(self, record_id):
        with get_cursor() as cursor:
            cursor.execute(f"{_SELECT_WITH_RELATIONS} WHERE p.id = %s", (record_id,))
            return cursor.fetchone()

    def create(self, data):
        created = super().create(data)
        return self.find_by_id(created["id"])

    def update(self, record_id, data):
        updated = super().update(record_id, data)
        return self.find_by_id(record_id) if updated else None