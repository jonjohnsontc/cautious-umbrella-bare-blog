"""
Simple dev server for building blog site
"""
import socketserver
import http.server
import os

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

    def translate_path(self, path):
        # Strip off the extension if it exists
        if ".html" in os.path.basename(path):
            path = path[: path.rfind(".")]
            breakpoint()
        # Call the superclass method to get the translated path
        return super().translate_path(path)

    def do_GET(self) -> None:
        return super().do_GET()


if __name__ == "__main__":
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"Serving from './public/' on {PORT}")
            httpd.serve_forever()

    # don't serve an exception when i exit with CTRL-C
    except KeyboardInterrupt:
        pass

    httpd.server_close()
