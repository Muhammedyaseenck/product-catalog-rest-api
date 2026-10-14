from app.validators.common import is_blank, is_number, is_positive_integer


def validate_product(body):
    errors = []
    name = body.get("name")
    if is_blank(name):
        errors.append("name is required and must be a non-empty string")
    elif len(name) > 150:
        errors.append("name must not exceed 150 characters")

    description = body.get("description")
    if description is not None and not isinstance(description, str):
        errors.append("description must be a string")

    price = body.get("price")
    if not is_number(price) or price < 0:
        errors.append("price is required and must be a non-negative number")

    if "stock" in body:
        stock = body["stock"]
        if not isinstance(stock, int) or isinstance(stock, bool) or stock < 0:
            errors.append("stock must be a non-negative integer")

    if not is_positive_integer(body.get("category_id")):
        errors.append("category_id is required and must be a positive integer")
    if not is_positive_integer(body.get("brand_id")):
        errors.append("brand_id is required and must be a positive integer")
    return errors