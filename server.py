"""
Simple dev server for building blog site
"""
import socketserver
import http.server

PORT = 8989


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(
        self,
        request,
        client_address,
        server: socketserver.BaseServer,
        *,
        directory=None,
    ) -> None:
        # We'll serve from the public directory, even though this server is top-level
        super().__init__(request, client_address, server, directory="./public/")

    def do_GET(self):
        # I want to serve the about.html page from /about
        if self.path.endswith("/about"):
            self.send_response(302)
            self.send_header("Location", "/about.html")
            self.end_headers()
        else:
            super(Handler, self).do_GET()


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving from './public/' on {PORT}")
        httpd.socket()
        httpd.serve_forever()
