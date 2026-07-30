#!/usr/bin/env python3
import http.server
import os
import cgi
import json

UPLOAD_DIR = "/workspace"

class UploadHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/upload":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={"REQUEST_METHOD": "POST", "CONTENT_TYPE": self.headers["Content-Type"]}
            )
            fileitem = form["file"]
            if fileitem.filename:
                filename = os.path.basename(fileitem.filename)
                filepath = os.path.join(UPLOAD_DIR, filename)
                with open(filepath, "wb") as f:
                    f.write(fileitem.file.read())
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "filename": filename}).encode())
            else:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        super().do_GET()

if __name__ == "__main__":
    os.chdir("/workspace")
    server = http.server.HTTPServer(("0.0.0.0", 8080), UploadHandler)
    print("Upload server running on port 8080")
    server.serve_forever()
