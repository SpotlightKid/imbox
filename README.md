Imbox - Python IMAP for Humans
==============================

[![Build Status](https://travis-ci.org/spotlightkid/imbox.svg?branch=master)](https://travis-ci.org/spotlihghtkid/imbox)


Python library for reading IMAP mailboxes and converting email content to
machine readable data

This is a fork of https://github.com/martinrusev/imbox with extensive
modifications, which uses [imapclient](http://imapclient.freshfoo.com/) under
the hood.


Installation
============

    pip install https://github.com/spotlightkid/imbox/archive/master.zip


Usage
=====

```python
from imbox import Imbox

imbox = Imbox('imap.gmail.com', ssl=True)
imbox.login('username', 'password')
```

Get all messages as a list of tuples `(msg_uid, msg_struct)`:

```python
all_messages = imbox.messages()
```

Get unread messages

```python
unread_messages = imbox.messages(seen=False)
```

Get messages sent *from* given address:

```python
messages_from = imbox.messages(from_='martin@amon.cx')
```

Get messages sent *to* given address:

```python
messages_from = imbox.messages(to='martin@amon.cx')
```

Get messages received before the specified date:

```python
messages_from = imbox.messages(before='31-July-2013')
```

Get messages received after the specified date:

```python
messages_from = imbox.messages(since='30-July-2013')
```

Get messages from specified folder:

```python
messages_folder = imbox.messages(folder='Social')
```

Loop over messages:

```python
for uid, message in all_messages:
    [...]
```

Every message is an `imbox.MessageStruct` instance, which has the following
attributes:

    message.from_
    message.sender
    message.reply_to
    message.to
    message.cc
    message.bcc
    message.subject
    message.headers
    message.message_id
    message.date
    message.parsed_date
    message.body.plain (a list of byte strings)
    message.body.html (a list of byte strings)
    message.attachments (a list of `io.BytesIO` instances)
    message.message (an `email.message.Message` instance)

To check all available keys:

```python
print(message.keys())
```

To check the whole object, just write:

```python
print(message)

{
    'headers':
        [{
            'name': 'Received-SPF',
            'value': 'pass (google.com: domain of ......;'
        },
        {
            'name': 'MIME-Version',
            'value': '1.0'
        }],
    'body': {
        'plain: ['ASCII'],
        'html': ['HTML BODY']
    },
    'attachments': [{
        'content': <io.BytesIO instance at 0x7f8e8445fa70>,
        'filename': "avatar.png",
        'content-type': 'image/png',
        'size': 80264
    }],
    'date': 'Fri, 26 Jul 2013 10:56:26 +0300',
    'parse_date': datetime.datetime(2013, 7, 26, 10, 56, 26),
    'message_id': '51F22BAA.1040606',
    'from_': [{
        'name': 'Martin Rusev',
        'email': 'martin@amon.cx'
    }],
    'to': [{
        'name': 'John Doe',
        'email': 'john@gmail.com'
    }],
    'subject': 'Hello John, How are you today'
}
```

Roadmap
=======

* Lazy email fetching
* Improved attachement handling
* Search mailboxes
* Manage labels
* Compose emails
