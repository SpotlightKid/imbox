# -*- coding: utf-8 -*-

__all__ = (
    'MessageStruct',
    'decode_mail_header',
    'decode_param',
    'get_mail_addresses',
    'parse_attachment',
    'parse_email'
)

import base64
import email
import quopri
import re
import time

from datetime import datetime
from email.header import decode_header
from io import BytesIO


class MessageStruct(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def keys(self):
        return self.__dict__.keys()

    def __repr__(self):
        return str(self.__dict__)


def decode_mail_header(value, default_charset='us-ascii'):
    """Decode a header value into a unicode string."""
    try:
        headers = decode_header(value)
    except email.errors.HeaderParseError:
        return value.encode(default_charset, 'replace').decode(default_charset)
    else:
        for index, (text, charset) in enumerate(headers):
            if isinstance(text, bytes):
                try:
                    headers[index] = text.decode(
                        charset or default_charset, 'replace')
                except LookupError:
                    # if the charset is unknown, force default
                    headers[index] = text.decode(default_charset, 'replace')
            else:
                headers[index] = text

        return "".join(headers)


def get_mail_addresses(message, header_name):
    """Retrieve all email addresses from one message header."""
    addresses = email.utils.getaddresses(decode_mail_header(header)
        for header in message.get_all(header_name, []))

    for index, (address_name, address_email) in enumerate(addresses):
        addresses[index] = {
            'name': address_name,
            'email': address_email
        }

    return addresses


def decode_param(param):
    name, v = param.split('=', 1)
    values = v.split('\n')
    value_results = []

    for value in values:
        match = re.search(r'=\?(\w+)\?(Q|B)\?(.+)\?=', value)

        if match:
            encoding, type_, code = match.groups()

            if type_ == 'Q':
                value = quopri.decodestring(code)
            elif type_ == 'B':
                value = base64.decodestring(code)

            value = value.decode(encoding)
            value_results.append(value)

    if value_results:
        v = ''.join(value_results)

    return name, v


def parse_attachment(message_part):
    # Check again if this is a valid attachment
    content_disposition = message_part.get("Content-Disposition", None)

    if content_disposition is not None:
        dispositions = content_disposition.strip().split(";")

        if dispositions[0].lower() in ["attachment", "inline"]:
            file_data = message_part.get_payload(decode=True)

            attachment = {
                'content-type': message_part.get_content_type(),
                'size': len(file_data),
                'content': BytesIO(file_data)
            }

            for param in dispositions[1:]:
                name, value = decode_param(param)

                if 'file' in name:
                    attachment['filename'] = value

                if 'create-date' in name:
                    attachment['create-date'] = value

            return attachment

    return None


def parse_email(raw_email, encoding='us-ascii'):
    if isinstance(raw_email, bytes) and not isinstance(raw_email, str):
        raw_email = raw_email.decode(encoding)
    if not isinstance(raw_email, str):
        raw_email = raw_email.encode(encoding)

    parsed_email = {'raw_email': raw_email, 'headers': []}
    parsed_email['message'] = message = email.message_from_string(raw_email)
    maintype = message.get_content_maintype()
    body = {"plain": [], "html": []}
    attachments = []

    if maintype == 'multipart':
        for part in message.walk():
            content = part.get_payload()
            content_type = part.get_content_type()
            content_disposition = part.get('Content-Disposition', None)

            if (content_type == "text/plain" and
                    (content_disposition is None or
                    content_disposition == "inline")):
                body['plain'].append(content)
            elif (content_type == "text/html" and
                    (content_disposition is None or
                    content_disposition == "inline")):
                body['html'].append(content)
            elif content_disposition:
                attachment = parse_attachment(part)

                if attachment:
                    attachments.append(attachment)
    elif maintype == 'text':
        body['plain'].append(message.get_payload(decode=True))

    parsed_email['attachments'] = attachments
    parsed_email['body'] = body
    parsed_email['from_'] = get_mail_addresses(message, 'from')
    parsed_email['sender'] = get_mail_addresses(message, 'sender')
    parsed_email['reply_to'] = get_mail_addresses(message, 'reply-to')
    parsed_email['cc'] = get_mail_addresses(message, 'cc')
    parsed_email['to'] = get_mail_addresses(message, 'to')

    email_dict = dict(message.items())
    value_headers_keys = ['subject', 'date', 'message-id']
    key_value_header_keys = ['received-spf',
                            'mime-version',
                            'x-spam-status',
                            'x-spam-score',
                            'content-type']

    for key, value in email_dict.items():
        if key.lower() in value_headers_keys:
            valid_key_name = key.lower().replace('-', '_')
            parsed_email[valid_key_name] = decode_mail_header(value)

        if key.lower() in key_value_header_keys:
            parsed_email['headers'].append({'name': key, 'value': value})

    if parsed_email.get('date'):
        timetuple = email.utils.parsedate(parsed_email['date'])
        parsed_email['parsed_date'] = datetime.fromtimestamp(
            time.mktime(timetuple)) if timetuple else None

    return MessageStruct(**parsed_email)
