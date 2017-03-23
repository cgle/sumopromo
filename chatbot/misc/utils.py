import ujson
from tornado import httpclient

def to_http_request(url, data, method='POST', **kwargs):
    return httpclient.HTTPRequest(
        url,
        headers={'Content-type': 'application/json'},
        method=method,
        body=ujson.dumps(data),
        **kwargs
    )
