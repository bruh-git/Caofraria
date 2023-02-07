import json
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer


class LSBHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/image":
            # Obtem os dados do corpo da requisição
            content_length = int(self.headers["Content-Length"])
            image = self.rfile.read(content_length)
            # cria um id unico e um arquivo temporário e escreva a imagem nele
            id = str(uuid.uuid4())
            with open(f"images/{id}.bmp", "wb") as f:
                f.write(image)
            # Envia uma resposta com o ID da imagem
            response = {"id": id}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        elif self.path == "/encode":
            content_length = int(self.headers["Content-Length"])
            request_body = self.rfile.read(content_length)
            # Carregue os dados da requisição como um objeto JSON
            request = json.loads(request_body)
            id = request["id"]
            message = request["message"] + "."
            # algoritmo de Esteganografia
            with open(f"images/{id}.bmp", "rb") as f:
                image = bytearray(f.read())
            for i, b in enumerate(message.encode()):
                image[i] = (image[i] & ~1) | (b & 1)
            new_id = str(uuid.uuid4())
            with open(f"images/{new_id}", "wb") as f:
                f.write(image)
            response = {"id": new_id}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path.startswith("/image?"):
            id = self.path.split("=")[1]
            with open(f"images/{id}.bmp", "rb") as f:
                image = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "image/bmp")
            self.send_header(
                "Content-Disposition", f"attachment; filename={id}.bmp"
            )
            self.end_headers()
            self.wfile.write(image)
        elif self.path.startswith("/decode?"):
            id = self.path.split("=")[1]
            with open(f"images/{id}", "rb") as f:
                image = bytearray(f.read())
            message = bytearray()
            for b in image:
                message.append(b & 1)
            decoded_message = message.decode("utf-8")
            decoded_message = decoded_message.rstrip(".")
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"message": decoded_message}
            self.wfile.write(json.dumps(response).encode("utf-8"))


# Inicializa o servidor


httpd = HTTPServer(("localhost", 8080), LSBHandler)
print("Servidor inicializado em http://localhost:8080")
httpd.serve_forever()
