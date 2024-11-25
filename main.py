from http.server import HTTPServer
from game.web_server import ManipuladorJogo

if __name__ == "__main__":
    servidor = HTTPServer(('localhost', 8000), ManipuladorJogo)
    print("Servidor iniciado em http://localhost:8000")
    servidor.serve_forever()