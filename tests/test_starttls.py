#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import getpass
import sys

import imaplib
from imapclient.imaptls import IMAP4
from imbox.parser import parse_email


IMAP_HOST = "imap.web.de"
IMAP_PORT = 143
USER = b"chris.arndt@web.de"
FOLDER = b"testtls"

def main(args):
    try:
        passwd = args.pop(0)
    except IndexError:
        passwd = getpass.getpass()

    imaplib.Debug  = 4
    imap = IMAP4(IMAP_HOST, IMAP_PORT)
    imap.starttls()
    imap.login(USER, passwd)

    imap.select(FOLDER)
    type_, data = imap.search(None, b'ALL')

    try:
        for msgnum in data[0].split():
            type_, data = imap.fetch(msgnum,
                b'(BODY[HEADER.FIELDS (SUBJECT FROM)])')
            msg = parse_email(data[0][1])
            print('[msg #{}]\nFrom: {}\nSubject: {}\n'.format(
                  int(msgnum), msg.from_[0]['email'], msg.subject))
    finally:
        imap.close()
        imap.logout()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
