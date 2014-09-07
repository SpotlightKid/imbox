#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from datetime import date, datetime

try:
    from collections import OrderedDict as odict
except ImportError:
    try:
        from ordereddict import OrderedDict as odict
    except ImportError:
        print("This test needs an implementation of the OrderedDict object.")
        print("It seems your Python installation does not have one.")
        print("Please install https://pypi.python.org/pypi/ordereddict")
        raise

from imbox.query import *


def test_all():
    query = build_search_query()
    assert query == b'ALL'

def test_filters_args():
    query = build_search_query('seen', ('to', "joe@doe.com"))
    assert query == b'SEEN TO "joe@doe.com"'
    query = build_search_query(('to', "joe@doe.com"), 'seen')
    assert query == b'TO "joe@doe.com" SEEN'

def test_filters_dict():
    query = build_search_query(dict(to="joe@doe.com", seen=True))
    assert query in (b'SEEN TO "joe@doe.com"', b'TO "joe@doe.com" SEEN')
    query = build_search_query(dict(to="joe@doe.com", deleted=False))
    assert query in (b'UNDELETED TO "joe@doe.com"', b'TO "joe@doe.com" UNDELETED')

def test_filters_odict():
    filters = odict()
    filters['seen'] = True
    filters['to'] = "joe@doe.com"
    query = build_search_query(filters)
    assert query == b'SEEN TO "joe@doe.com"'
    filters = odict()
    filters['to'] = "joe@doe.com"
    filters['seen'] = True
    query = build_search_query(filters)
    assert query == b'TO "joe@doe.com" SEEN'
    query = build_search_query(filters, 'deleted')
    assert query == b'TO "joe@doe.com" SEEN DELETED'
    query = build_search_query(filters, deleted=False)
    assert query == b'TO "joe@doe.com" SEEN UNDELETED'

def test_kwargs():
    query = build_search_query(seen=True, to="joe@doe.com")
    assert query == b'SEEN TO "joe@doe.com"'
    query = build_search_query(to="joe@doe.com", seen=True)
    assert query == b'SEEN TO "joe@doe.com"'
    query = build_search_query(seen=False, to="joe@doe.com")
    assert query == b'UNSEEN TO "joe@doe.com"'
    query = build_search_query(to="joe@doe.com", seen=False)
    assert query == b'UNSEEN TO "joe@doe.com"'

def test_encoding():
    query = build_search_query(encoding="UTF-8")
    assert isinstance(query, bytes)
    assert query.startswith(b'CHARSET UTF-8 ')
    query = build_search_query(encoding=None)
    assert not query.startswith(b'CHARSET')
    assert isinstance(query, bytes)

def test_unseen():
    query = build_search_query(seen=False)
    assert query == b'UNSEEN'

def test_from():
    query = build_search_query(from_='joe@doe.com')
    assert query == b'FROM "joe@doe.com"'
    query = build_search_query(from_='joe@doe.com', seen=False)
    assert query == b'FROM "joe@doe.com" UNSEEN'

def test_to():
    query = build_search_query(to='joe@doe.com')
    assert query == b'TO "joe@doe.com"'
    query = build_search_query(to='joe@doe.com', seen=False)
    assert query == b'UNSEEN TO "joe@doe.com"'

def test_since():
    query = build_search_query(since='6-Aug-2014')
    assert query == b'SINCE "6-Aug-2014"'
    query = build_search_query(since=date(2014, 8, 6))
    assert query == b'SINCE 6-Aug-2014'
    query = build_search_query(since=datetime(2014, 5, 24, 11, 11, 11))
    assert query == b'SINCE 24-May-2014'

def test_before():
    query = build_search_query(before='6-Aug-2014')
    assert query == b'BEFORE "6-Aug-2014"'
    query = build_search_query(before=date(2014, 8, 6))
    assert query == b'BEFORE 6-Aug-2014'
    query = build_search_query(before=datetime(2014, 5, 24, 11, 11, 11))
    assert query == b'BEFORE 24-May-2014'

def test_larger():
    query = build_search_query(('larger', 1024))
    assert query == b'LARGER 1024'
    query = build_search_query(larger=1024)
    assert query == b'LARGER 1024'

def test_uid():
    query = build_search_query(uid=23)
    assert query == b'UID 23'
    query = build_search_query(uid=(23,42,314))
    assert query == b'UID 23,42,314'
    query = build_search_query(uid=('23','42','314'))
    assert query == b'UID 23,42,314'

def test_header():
    query = build_search_query(header=dict(x_spam_flag='NO'))
    assert query == b'HEADER X-SPAM-FLAG "NO"'
