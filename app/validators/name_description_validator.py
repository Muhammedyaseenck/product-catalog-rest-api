from app.validators.common import is_blank


def validate_name_description(body):
    """Validate the payload shared by categories and brands."""
    errors = []
    name = body.get("name")
    if is_blank(name):
        errors.append("name is required and must be a non-empty string")
    elif len(name) > 100:
        errors.append("name must not exceed 100 characters")

    description = body.get("description")
    if description is not None and not isinstance(description, str):
        errors.append("description must be a string")
    return errors