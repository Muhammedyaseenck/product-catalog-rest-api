from app.repositories import BrandRepository, CategoryRepository, ProductRepository
from app.routes.crud_blueprint import create_crud_blueprint
from app.validators import validate_name_description, validate_product


def register_blueprints(app):
    app.register_blueprint(
        create_crud_blueprint(
            "products", ProductRepository(), validate_product, "Product"
        )
    )
    app.register_blueprint(
        create_crud_blueprint(
            "categories", CategoryRepository(), validate_name_description, "Category"
        )
    )
    app.register_blueprint(
        create_crud_blueprint(
            "brands", BrandRepository(), validate_name_description, "Brand"
        )
    )