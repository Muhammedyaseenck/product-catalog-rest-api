def is_blank(value):
    return not isinstance(value, str) or not value.strip()


def is_positive_integer(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)