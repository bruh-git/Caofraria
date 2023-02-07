import json
import uuid
import pytest
import requests
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


class LSBHandler(BaseHTTPRequestHandler):
    # O código da classe LSBHandler é o mesmo apresentado na sua pergunta anterior.
    
    
def test_post_image():
    # Inicializa o servidor
    server = HTTPServer(("localhost", 8080), LSBHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    
    # Envia uma requisição POST para o endpoint /image
    image = b"\x01\x02\x03\x04"
    response = requests.post("http://localhost:8080/image", data=image)
    
    # Verifica se a resposta é válida
    assert response.status_code == 200
    response_json = json.loads(response.text)
    assert "id" in response_json
    
    # Verifica se a imagem foi escrita no arquivo correto
    id = response_json["id"]
    with open(f"images/{id}.bmp", "rb") as f:
        written_image = f.read()
    assert written_image == image
    
    # Finaliza o servidor
    server.shutdown()
    server.server_close()
    
    
def test_post_encode():
    # Inicializa o servidor
    server = HTTPServer(("localhost", 8080), LSBHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    
    # Envia uma requisição POST para o endpoint /image para criar a imagem original
    image = b"\x01\x02\x03\x04"
    response = requests.post("http://localhost:8080/image", data=image)
    response_json = json.loads(response.text)
    id = response_json["id"]
    
    # Envia uma requisição POST para o endpoint /encode
    message = "Hello World!"
    request_body = json.dumps({"id": id, "message": message})
    response = requests.post("http://localhost:8080/encode", data=request_body)
    
    # Verifica se a resposta é válida
    assert response.status_code == 200
    response_json = json.loads(response.text)
    assert "id" in response_json


