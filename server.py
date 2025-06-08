#!/usr/bin/env python3
import socket
import threading
import os
import json
import datetime
import mimetypes
from urllib.parse import urlparse, unquote

# Modüler route’ları import ediyoruz
from routes import hello, echo

# Sunucu ayarları
HOST = '0.0.0.0'
PORT = 8080
STATIC_DIR = 'static'
LOG_FILE = 'server.log'

# MIME tipi tanımları
MIME_TYPES = mimetypes.types_map.copy()

def log_request(method, path, code):
    with open(LOG_FILE, 'a') as f:
        ts = datetime.datetime.now().isoformat()
        f.write(f"{ts} | {method} {path} -> {code}\n")

def handle_client(conn, addr):
    try:
        raw = conn.recv(2048).decode('utf-8')
        lines = raw.split('\r\n')
        method, raw_path, _ = lines[0].split()
        path = urlparse(raw_path).path

        # Header okuma
        headers = {}
        i = 1
        while lines[i]:
            k, v = lines[i].split(': ', 1)
            headers[k] = v
            i += 1

        # Yardımcılar
        def send_response(status, content_type, body=b'', send_body=True):
            header = (
                f"HTTP/1.1 {status} {'OK' if status==200 else 'Error'}\r\n"
                f"Content-Type: {content_type}\r\n"
                f"Content-Length: {len(body)}\r\n\r\n"
            )
            conn.sendall(header.encode())
            if send_body and body:
                conn.sendall(body)

        def recv_body(length):
            return conn.recv(length) if length else b''

        # ROUTER
        code = 404
        if method in ('GET', 'HEAD'):
            # 1) Statik dosyalar
            if path.startswith(f'/{STATIC_DIR}/'):
                fp = os.path.join('.', unquote(path.lstrip('/')))
                if os.path.isfile(fp):
                    ctype = MIME_TYPES.get(os.path.splitext(fp)[1], 'application/octet-stream')
                    body = open(fp, 'rb').read()
                    code = 200
                    send_response(200, ctype, body, send_body=(method=='GET'))
                else:
                    send_response(404, 'text/plain', b'404 Not Found')
            # 2) /api/hello
            elif path == '/api/hello':
                hello.handle(conn, method, headers, send_response)
                code = 200
            else:
                send_response(404, 'text/plain', b'404 Not Found')

        elif method == 'POST':
            # 3) /api/echo
            if path == '/api/echo':
                # echo.handle signature: (conn, method, headers, recv_body, send_response)
                echo.handle(conn, method, headers, recv_body, send_response)
                code = 200
            else:
                send_response(404, 'text/plain', b'404 Not Found')
        else:
            # Desteklenmeyen metot
            send_response(501, 'text/plain', b'501 Not Implemented')
            code = 501

        log_request(method, path, code)

    except Exception as e:
        send_response(500, 'text/plain', b'500 Internal Server Error')
        log_request('ERR', str(e), 500)
    finally:
        conn.close()

def run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Sunucu dinleniyor: http://{HOST}:{PORT}")
        while True:
            client, addr = s.accept()
            threading.Thread(target=handle_client, args=(client, addr), daemon=True).start()

if __name__ == '__main__':
    run()
