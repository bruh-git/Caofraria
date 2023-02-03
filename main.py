import json
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer


def encode_message(image_id, message):
    # Código para codificar a mensagem na imagem
    encoded_image = image_id + "_encoded"
    try:
        with open(image_id, "rb") as image_file:
            image_data = image_file.read()
    except FileNotFoundError:
        print(f"Arquivo {image_id} não encontrado.")
        return None
    image_data = bytearray(image_data)
    message_bytes = bytearray(message.encode("utf-8")) + bytearray([26])
    message_index = 0
    for i in range(len(image_data)):
        if message_index >= len(message_bytes):
            break

        # Colocar o menos significativo
        # do byte da mensagem no menos significativo do byte da imagem
        image_data[i] = (image_data[i] & ~1) | (
            message_bytes[message_index] & 1
        )
        message_bytes[message_index] >>= 1

        # Passar para o próximo byte
        # da mensagem quando o bit mais significativo for 0
        if message_bytes[message_index] == 0:
            message_index += 1

    with open(encoded_image, "wb") as encoded_image:
        encoded_image.write(image_data)
    return encoded_image.name


def decode_message(image_id):
    try:
        with open(image_id, "rb") as image_file:
            image_data = bytearray(image_file.read())
    except FileNotFoundError:
        print(f"Arquivo {image_id} não encontrado.")
        return None
    if len(image_data) % 8 != 0:
        print("Tamanho do arquivo de imagem inválido para decodificação.")
        return None
    message_bytes = bytearray('')
    current_byte = 0
    message_length = 0
    for byte in image_data:
        # Adicionar o menos significativo do byte da imagem
        # ao menos significativo do byte da mensagem
        current_byte = (current_byte << 1) | (byte & 1)
        message_length += 1

        # Se o bit mais significativo do byte da mensagem for 1,
        # adicionar o byte da mensagem aos bytes da mensagem
        if (current_byte & 128) != 0:
            message_bytes.append(current_byte)
            current_byte = 0
            message_length = 0

        # Se a mensagem tiver mais de 8 bytes,
        # e o último byte for 26, considerar a mensagem decodificada
        if message_length >= 8 and message_bytes[-1] == 26:
            break

    return message_bytes[:-1].decode("utf-8")


class ServerHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/image":
            # Obtenha os dados do corpo da requisição
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)

            # Crie um arquivo temporário e escreva a imagem nele
            temp_file = str(uuid.uuid4())
            with open(temp_file, "wb") as f:
                f.write(body)

            # Envie uma resposta com o ID da imagem
            response = {"id": temp_file}
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
        elif self.path == "/encode":
            # Obtenha os dados do corpo da requisição
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)

            # Carregue os dados da requisição como um objeto JSON
            request_data = json.loads(body)
            image_id = request_data["id"]
            message = request_data["message"]

            # Verifique se a mensagem termina com um ponto
            if not message.endswith("."):
                self.send_response(400)
                self.end_headers()
                response = {"error": "A mensagem deve terminar com um ponto."}
                self.wfile.write(json.dumps(response).encode("utf-8"))
                return

            # Aplique o algoritmo de Esteganografia
            encoded_file = encode_message(image_id, message)

            # Envie uma resposta com o ID da imagem codificada
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"id": encoded_file}
            self.wfile.write(json.dumps(response).encode("utf-8"))

    def do_GET(self):
        if self.path.startswith("/image?"):
            # Obtenha o ID da imagem
            image_id = self.path.split("=")[1]

            # Ler o arquivo de imagem e enviá-lo como resposta
            with open(image_id, "rb") as image_file:
                image_data = image_file.read()
            self.send_response(200)
            self.send_header("Content-type", "image/jpeg")
            self.send_header("Content-length", len(image_data))
            self.end_headers()
            self.wfile.write(image_data)

        elif self.path.startswith("/decode?"):
            # Obtenha o ID da imagem
            image_id = self.path.split("=")[1]

            # Decodifique a mensagem
            message = decode_message(image_id)

            # Envie uma resposta com a mensagem decodificada
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"message": message}
            self.wfile.write(json.dumps(response).encode("utf-8"))


# Inicialize o servidor


httpd = HTTPServer(("localhost", 8080), ServerHandler)
print("Servidor inicializado em http://localhost:8080")
httpd.serve_forever()
