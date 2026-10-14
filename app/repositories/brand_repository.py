from app.repositories.base_repository import BaseRepository


class BrandRepository(BaseRepository):
    def __init__(self):
        super().__init__("brands", ["name", "description"])