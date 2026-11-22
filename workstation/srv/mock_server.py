#!/usr/bin/env python3
"""
mock_server.py - Web server nội bộ phục vụ kịch bản phòng thủ browser hijacker.
Lắng nghe tại 0.0.0.0:8080.
- Host ads.local:8080 -> Trang quảng cáo độc hại của hijacker.
- Host novacorp.local:8080 -> Cổng thông tin nội bộ an toàn của NovaCorp.
Tương thích hoàn toàn với Python 3.5+.
"""

import os
from http.server import HTTPServer, BaseHTTPRequestHandler

WWW_DIR = "/home/ubuntu/srv/www"

class MockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        host = self.headers.get("Host", "").lower()
        path = self.path.split("?")[0]

        if "ads.local" in host:
            target_file = os.path.join(WWW_DIR, "ads", "index.html")
            site_name = "ads.local"
        elif "novacorp.local" in host:
            target_file = os.path.join(WWW_DIR, "novacorp", "index.html")
            site_name = "novacorp.local"
        else:
            target_file = os.path.join(WWW_DIR, "novacorp", "index.html")
            site_name = "default"

        if os.path.exists(target_file):
            with open(target_file, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            msg = "Server " + site_name + ":8080 running."
            self.wfile.write(msg.encode("utf-8"))

    def log_message(self, format, *args):
        # Không in rác log ra terminal
        pass

def run():
    server_address = ("0.0.0.0", 8080)
    httpd = HTTPServer(server_address, MockHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
