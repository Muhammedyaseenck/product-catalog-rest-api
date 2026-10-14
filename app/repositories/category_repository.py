from app.repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository):
    def __init__(self):
        super().__init__("categories", ["name", "description"])