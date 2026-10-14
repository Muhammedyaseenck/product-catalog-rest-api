from flask import Blueprint, jsonify, request

from app.errors import ApiError


def create_crud_blueprint(resource_name, repository, validate, label):
    """Build a blueprint exposing the five standard CRUD endpoints.

    GET    /<resource_name>
    GET    /<resource_name>/<id>
    POST   /<resource_name>
    PUT    /<resource_name>/<id>
    DELETE /<resource_name>/<id>
    """
    blueprint = Blueprint(resource_name, __name__, url_prefix=f"/{resource_name}")

    def get_valid_body():
        body = request.get_json(silent=True)
        if not isinstance(body, dict):
            raise ApiError.bad_request("Request body must be a valid JSON object")
        errors = validate(body)
        if errors:
            raise ApiError.bad_request("Validation failed", errors)
        return body

    def get_or_404(record_id):
        record = repository.find_by_id(record_id)
        if record is None:
            raise ApiError.not_found(f"{label} not found")
        return record

    @blueprint.get("")
    def list_records():
        return jsonify(repository.find_all()), 200

    @blueprint.get("/<int:record_id>")
    def get_record(record_id):
        return jsonify(get_or_404(record_id)), 200

    @blueprint.post("")
    def create_record():
        record = repository.create(get_valid_body())
        return jsonify(record), 201

    @blueprint.put("/<int:record_id>")
    def update_record(record_id):
        body = get_valid_body()
        record = repository.update(record_id, body)
        if record is None:
            raise ApiError.not_found(f"{label} not found")
        return jsonify(record), 200

    @blueprint.delete("/<int:record_id>")
    def delete_record(record_id):
        if not repository.delete(record_id):
            raise ApiError.not_found(f"{label} not found")
        return "", 204

    return blueprint