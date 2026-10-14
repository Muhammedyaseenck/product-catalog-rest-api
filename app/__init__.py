from flask import Flask

from app import db
from app.config import Config
from app.errors import register_error_handlers
from app.json_provider import CustomJSONProvider
from app.routes import register_blueprints


def create_app(config_class=Config):
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.json = CustomJSONProvider(app)
    app.url_map.strict_slashes = False

    db.init_pool(
        app.config["DATABASE_URL"],
        app.config["DB_POOL_MIN"],
        app.config["DB_POOL_MAX"],
    )

    register_error_handlers(app)
    register_blueprints(app)
    return app