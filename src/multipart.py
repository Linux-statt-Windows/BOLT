#!/bin/env python3

import mimetypes
import uuid

def encode_multipart(files, fields):
    LIMIT, CRLF, content = '----------' + uuid.uuid4().hex, b'\r\n', []
    for (key, value) in fields:
        content.append(('--' + LIMIT).encode('utf-8'))
        content.append(('Content-Disposition: form-data; name="' + key + '"').encode('utf-8'))
        content.append(b'')
        content.append(value.encode('utf-8'))
    for (key, name, value) in files:
        content.append(('--' + LIMIT).encode('utf-8'))
        content.append(('Content-Disposition: form-data; name="{0}"; filename="{1}"'.format(key, name)).encode('utf-8'))
        content.append(('Content-Type: ' + get_content_type(name)).encode('utf-8'))
        content.append(b'')
        pic = open(value, 'rb').read()
        content.append(pic)
    content.append(('--' + LIMIT + '--').encode('utf-8'))
    content.append(b'')
    body = CRLF.join(content)
    content_type = 'multipart/form-data; boundary=' + LIMIT
    return content_type, body


def get_content_type(name):
    return mimetypes.guess_type(name)[0] or 'application/octect-stream'
