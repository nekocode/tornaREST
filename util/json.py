# coding:utf-8

import calendar
import datetime
import bson
from bson.objectid import ObjectId
from bson import SON
from bson.py3compat import string_type

json_lib = True
try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        json_lib = False


def _json_convert(obj):
    """Recursive helper method that converts BSON types so they can be
    converted into json.
    """
    if hasattr(obj, 'iteritems') or hasattr(obj, 'items'):  # PY3 support
        return SON(((k, _json_convert(v)) for k, v in obj.items()))
    elif hasattr(obj, '__iter__') and not isinstance(obj, string_type):
        return list((_json_convert(v) for v in obj))
    try:
        return default(obj)
    except TypeError:
        return obj


def default(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime.datetime):
        # TODO share this code w/ bson.py?
        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()
        millis = int(calendar.timegm(obj.timetuple()) * 1000 +
                     obj.microsecond / 1000)
        return millis
    if bson.uuid and isinstance(obj, bson.uuid.UUID):
        return obj.hex
    raise TypeError("%r is not JSON serializable" % obj)


def dumps(obj, *args, **kwargs):
    """Helper function that wraps :class:`json.dumps`.

    Recursive function that handles all BSON types including
    :class:`~bson.binary.Binary` and :class:`~bson.code.Code`.

    .. versionchanged:: 2.7
       Preserves order when rendering SON, Timestamp, Code, Binary, and DBRef
       instances. (But not in Python 2.4.)
    """
    if not json_lib:
        raise Exception("No json library available")
    return json.dumps(_json_convert(obj), *args, **kwargs)

