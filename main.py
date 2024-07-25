import http.server
import socketserver
import os

PORT = 8080


class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        # Determine the requested file
        requested_file = ''
        if self.path == '/':
            self.path = '/index.html'
        elif self.path.endswith(".html") and self.path != '/index.html':
            requested_file = self.path.lstrip('/')
        else:
            # If not an HTML file, serve as it is
            return super().do_GET()

        # Read the content of the requested file
        try:
            with open(requested_file, 'r', encoding='utf-8') as f:
                requested_content = f.read()
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")
            return

        # Read the content of the index.html
        with open('index.html', 'r', encoding='utf-8') as f:
            index_content = f.read()

        # Inject the requested file content into the <main></main> section
        updated_content = index_content.replace(
            '<main></main>', f'<main>{requested_content}</main>')

        # Send the response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(updated_content.encode('utf-8'))


with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
