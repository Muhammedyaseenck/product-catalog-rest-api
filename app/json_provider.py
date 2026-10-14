from datetime import date, datetime
from decimal import Decimal

from flask.json.provider import DefaultJSONProvider


class CustomJSONProvider(DefaultJSONProvider):
    """Serialise NUMERIC as numbers and timestamps as ISO 8601 strings."""

    sort_keys = False

    @staticmethod
    def default(obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return DefaultJSONProvider.default(obj)