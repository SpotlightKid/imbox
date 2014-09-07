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

# Gets all messages
all_messages = imbox.messages()

# Unread messages
unread_messages = imbox.messages(unread=True)

# Messages sent FROM
messages_from = imbox.messages(from_='martin@amon.cx')

# Messages sent TO
messages_from = imbox.messages(to='martin@amon.cx')

# Messages received before specific date
messages_from = imbox.messages(before='31-July-2013')

# Messages received after specific date
messages_from = imbox.messages(since='30-July-2013')

# Messages from a specific folder
messages_folder = imbox.messages(folder='Social')


for uid, message in all_messages:
    ........
    # Every message is an object with the following keys

    message.sent_from
    message.sent_to
    message.subject
    message.headers
    message.message_id
    message.date
    message.body.plain
    message.body.html
    message.attachments

    # To check all available keys
    print message.keys()


    # To check the whole object, just write
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
    'date': u 'Fri, 26 Jul 2013 10:56:26 +0300',
    'message_id': u '51F22BAA.1040606',
    'sent_from': [{
        'name': u 'Martin Rusev',
        'email': 'martin@amon.cx'
    }],
    'sent_to': [{
        'name': u 'John Doe',
        'email': 'john@gmail.com'
    }],
    'subject': u 'Hello John, How are you today'
    }
```

Roadmap
=======

* Lazy email fetching
* Improved attachement handling
* Search mailboxes
* Manage labels
* Compose emails
