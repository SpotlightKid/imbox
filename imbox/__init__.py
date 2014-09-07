# -*- coding: utf-8 -*-

from __future__ import absolute_import

__all__ = ('Imbox', 'build_search_query', 'parse_email')

from imapclient import IMAPClient

from .parser import parse_email
from .query import build_search_query


class Imbox(IMAPClient):
    def query_uids(self, *args, **kwargs):
        query = build_search_query(*args, **kwargs)
        message, data = self._imap.uid('search', None, query)
        return data[0].split()

    def fetch_query(self, **kwargs):
        uids = self.query_uids(**kwargs)

        return ((msgnum, parse_email(data['BODY[]']))
            for msgnum, data in self.fetch(uids, 'BODY.PEEK[]').items())

    def mark_seen(self, uids):
        self.add_flags(uids, SEEN)

    def move(self, uids, destination_folder):
        if self.copy(uid, destination_folder):
            self.delete_messages(uids)

    def messages(self, *args, **kwargs):
        folder = kwargs.get('folder', False)

        if folder:
            self.select_folder(folder)
        elif self._imap.state != 'SELECTED':
            self.select_folder('INBOX')

        return list(self.fetch_query(**kwargs))
