# -*- coding: utf-8 -*-

__all__ = ('build_search_query',)

from datetime import date, datetime
from itertools import chain

DATE_FMT = "{0}-{1}-{2:04}"
MONTH_NAMES = "Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec".split(',')
SEARCH_KEYS = ("BCC,BEFORE,BODY,CC,FROM,LARGER,ON,SENTBEFORE,SENTON,SENTSINCE,"
    "SINCE,SMALLER,SUBJECT,TEXT,TO,UID").split(',')
SEARCH_FLAGS = "ANSWERED,DELETED,DRAFT,FLAGGED,SEEN".split(',')
SEARCH_STATES = "ALL,NEW,OLD,RECENT".split(',')


def format_rfc2822_date(d):
    """Format date or datetime as a date string according to RFC2822.

    Unlike ``strftime`` this is not affected by the current locale.

    """
    return DATE_FMT.format(d.day, MONTH_NAMES[d.month-1], d.year)

# TODO - Validate query arguments
def build_search_query(*filters, **kwargs):
    """Return IMAP search query string built from arguments."""
    query = []

    if filters and hasattr(filters[0], 'items'):
        filters = chain(filters[0].items(), filters[1:])

    filters = ((f, True) if isinstance(f, str) else f for f in filters)

    for key, value in chain(filters or [], sorted(kwargs.items())):
        search_key = key.rstrip('_').upper()

        if search_key in SEARCH_FLAGS:
            query.append(("" if value else "UN") + search_key)
        elif search_key in SEARCH_STATES and value:
            query.append(search_key)
        elif search_key in SEARCH_KEYS and value not in (True, False, None):
            if isinstance(value, (tuple, list)):
                # for UID sequences
                value = ",".join(str(v) for v in value)
            elif isinstance(value, str):
                value = '"{0}"'.format(value.replace('"', r'\"'))
            elif isinstance(value, (date, datetime)):
                value = format_rfc2822_date(value)

            query.append("{0} {1}".format(search_key, value))
        elif key == 'header':
            if isinstance(value, dict):
                value = value.items()

            for k, v in value:
                query.append('{0} {1} "{2}"'.format(search_key,
                    k.replace('_', '-').upper(), v.replace('"', r'\"')))

    query = " ".join(query) or "ALL"

    encoding = kwargs.get('encoding')

    if encoding:
        query = "CHARSET {0} {1}".format(encoding, query)

    return query.encode(encoding or 'ascii')
