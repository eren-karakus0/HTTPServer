import json

def handle(conn, method, headers, send_response):
    """
    GET veya HEAD ile /api/hello isteğini işlemeye yarar.
    send_response(status_code, content_type, body_bytes, send_body=True)
    """
    payload = json.dumps({'message': 'Hello, world!'}).encode()
    status = 200
    content_type = 'application/json'
    send_response(status, content_type, payload, send_body=(method=='GET'))
