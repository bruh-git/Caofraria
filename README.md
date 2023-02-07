Documentação do Código
Descrição
Este é um código de servidor HTTP simples que implementa a técnica de Esteganografia de Último Bit (LSB). O servidor aceita requisições POST para codificar e decodificar mensagens em imagens BMP. Ele também aceita requisições GET para recuperar imagens e mensagens decodificadas.

Arquivos
O código consta de um único arquivo, LSBHandler.py. Este arquivo define a classe LSBHandler que herda de BaseHTTPRequestHandler. A classe LSBHandler é responsável por lidar com requisições POST e GET e realizar a codificação e decodificação de mensagens em imagens BMP.

API
POST /image
Espera-se que este endpoint seja chamado com uma imagem BMP no corpo da requisição. O servidor irá gerar um ID único e criar um arquivo temporário para armazenar a imagem. Em seguida, o servidor retornará o ID da imagem codificado como JSON.

Exemplo de resposta:

css
Copy code
HTTP/1.1 200 OK
Content-Type: application/json

{"id": "57e2b2f1-e21e-41b5-b529-80b51dbc15d8"}
POST /encode
Espera-se que este endpoint seja chamado com uma mensagem codificada como JSON no corpo da requisição. O formato da requisição é o seguinte:

json
Copy code
{
    "id": "57e2b2f1-e21e-41b5-b529-80b51dbc15d8",
    "message": "hello world"
}
O servidor irá carregar a imagem BMP com o ID especificado na requisição e codificar a mensagem na imagem. Em seguida, o servidor retornará o ID da imagem codificada como JSON.

Exemplo de resposta:

css
Copy code
HTTP/1.1 200 OK
Content-Type: application/json

{"id": "57e2b2f1-e21e-41b5-b529-80b51dbc15d8"}
GET /image
Espera-se que este endpoint seja chamado com um ID de imagem como query string. O servidor irá retornar a imagem BMP correspondente.

Exemplo de resposta:

css
Copy code
HTTP/1.1 200 OK
Content-Type: image/bmp
Content-Disposition: attachment; filename=57e2b2f1-e21e-41b5-b529-80b51dbc15d8.bmp

[bytes da imagem BMP]
