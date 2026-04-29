from http.server import HTTPServer
from server.handler import Handler
from services.search_indexer import start_indexer
if __name__ == "__main__":
    start_indexer()
    print("Server running on http://localhost:8000")
    HTTPServer(("localhost", 8000), Handler).serve_forever()