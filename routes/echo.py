import json

def handle(conn, method, headers, recv_body, send_response):
    """
    POST ile /api/echo isteğini işler ve JSON’u echo’lar.
    recv_body(length) → bytes
    send_response(status_code, content_type, body_bytes, send_body=True)
    """
    length = int(headers.get('Content-Length', 0))
    body = recv_body(length) if length else b''
    try:
        data = json.loads(body.decode())
        out = json.dumps({'echo': data}).encode()
    except:
        out = b'{}'
    send_response(200, 'application/json', out, send_body=True)
