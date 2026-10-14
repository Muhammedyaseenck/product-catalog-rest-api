from flask import jsonify
from psycopg2 import errors as pg_errors
from werkzeug.exceptions import HTTPException


class ApiError(Exception):
    """Application error that maps directly to an HTTP response."""

    def __init__(self, status_code, message, details=None):
        super().__init__(message)
        self.status_code = status_code
        self.message = message
        self.details = details

    @classmethod
    def bad_request(cls, message, details=None):
        return cls(400, message, details)

    @classmethod
    def not_found(cls, message="Resource not found"):
        return cls(404, message)

    @classmethod
    def conflict(cls, message):
        return cls(409, message)


def _error_response(status_code, message, details=None):
    body = {"error": message}
    if details:
        body["details"] = details
    return jsonify(body), status_code


def register_error_handlers(app):
    @app.errorhandler(ApiError)
    def handle_api_error(error):
        return _error_response(error.status_code, error.message, error.details)

    @app.errorhandler(pg_errors.UniqueViolation)
    def handle_unique_violation(_error):
        return _error_response(
            409, "A record with the same unique value already exists"
        )

    @app.errorhandler(pg_errors.ForeignKeyViolation)
    def handle_foreign_key_violation(_error):
        return _error_response(
            409,
            "Operation violates a relationship "
            "(referenced record missing or still in use)",
        )

    @app.errorhandler(pg_errors.RestrictViolation)
    def handle_restrict_violation(_error):
        return _error_response(
            409, "Cannot delete: the record is still referenced by other records"
        )

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return _error_response(error.code, error.description)

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        app.logger.exception("Unhandled error: %s", error)
        return _error_response(500, "Internal server error")