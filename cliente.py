import http.server
import socketserver

PORT = 8000
DIRETORIO = "frontend"  # Serve a pasta "frontend" como raiz
#
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRETORIO, **kwargs)
#
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Servidor rodando na porta {PORT}...")
    print(f"Acesse: http://localhost:{PORT}/homepage.html")
    httpd.serve_forever()