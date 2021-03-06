"""
    Any general purpose utilities useful in the project are defined here.
"""

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
from dateutil.parser import parse as date_parse
from collections import namedtuple, OrderedDict


def format_timestamp(timestamp_repr):
    """
        Convert representation to mediawiki timestamps.  Returns a sring
         timestamp in the MediaWiki Format.

        Parameters
        ~~~~~~~~~~

        timestamp_repr : str|datetime
           Datetime representation to convert.
    """
    if hasattr(timestamp_repr, 'strftime'):
        return timestamp_repr.strftime(TIMESTAMP_FORMAT)
    else:
        return date_parse(timestamp_repr).strftime(
            TIMESTAMP_FORMAT)


def enum(*sequential, **named):
    """
        Implemetents an enumeration::

            >>> Numbers = enum('ZERO', 'ONE', 'TWO')
            >>> Numbers.ZERO
            0
            >>> Numbers.ONE
            1
    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


def build_namedtuple(names, types, values):
    """
        Given a set of types, values, and names builds a named tuple.  This
        method expects three lists all of the same length and returns a
        dynamically built namedtuple object.  Currently, only ``list``,
        ``str``, ``int``, and ``float`` cast methods are accepted as members
        of ``types``.

        Parameters
        ~~~~~~~~~~

        names : list
           Strings representing attribute names.

        types : list
           Typecast methods for each value.

        values : list
           Values of attributes.  These may be string.
    """
    param_type = namedtuple('build_namedtuple', ' '.join(names))
    arg_list = list()
    for t, v in zip(types, values):
        if t == str:
            arg_list.append("'" + str(v) + "'")
        elif t == int or t == list or t == float:
            arg_list.append(str(v))
    return eval('param_type(' + ','.join(arg_list) + ')')


def unpack_fields(obj):
    """
        Unpacks the values from a named tuple into a dict.  This method
        expects the '_fields' or 'todict' attribute to exist.  namedtuples
        expose the fromer interface while recordtypes expose the latter.
    """
    d = OrderedDict()

    if hasattr(obj, '_fields'):
        for field in obj._fields:
            d[field] = getattr(obj, field)
    elif hasattr(obj, 'todict'):
        d = OrderedDict(obj.todict())

    return d


def nested_import(name):
    """
        Using ``__import__`` retrieve nested object/namespace.  Solution_
        couresty of stack overflow user dwestbook_.

        .. _Solution: http://stackoverflow.com/questions/
        211100/pythons-import-doesnt-work-as-expected
        .. _dwestbrook: http://stackoverflow.com/users/3119/dwestbrook
    """
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


# Rudimentary Testing
if __name__ == '__main__':
    t = build_namedtuple(['a', 'b'], [int, str], [1, 's'])
    print t
