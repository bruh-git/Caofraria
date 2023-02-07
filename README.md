# Documentação da API

# Descrição
Este é um código de servidor HTTP simples que implementa a técnica de Esteganografia de Último Bit (LSB). O servidor aceita requisições POST para codificar e decodificar mensagens em imagens BMP. Ele também aceita requisições GET para recuperar imagens e mensagens decodificadas.

# Arquivos
O código consta de um único arquivo, main.py. Este arquivo define a classe LSBHandler que herda de BaseHTTPRequestHandler. A classe LSBHandler é responsável por lidar com requisições POST e GET e realizar a codificação e decodificação de mensagens em imagens BMP.

# API

# POST /image
Espera-se que este endpoint seja chamado com uma imagem BMP no corpo da requisição. O servidor irá gerar um ID único e criar um arquivo temporário para armazenar a imagem. Em seguida, o servidor retornará o ID da imagem codificado como JSON.

Exemplo de resposta:


```python
HTTP/1.1 200 OK
Content-Type: application/json

{

    "id": "57e2b2f1-e21e-41b5-b529-80b51dbc15d8"

}

```

# POST /encode
Espera-se que este endpoint seja chamado com uma mensagem codificada como JSON no corpo da requisição. O formato da requisição é o seguinte:

```python
json

{
    "id": "57e2b2f1-e21e-41b5-b529-80b51dbc15d8",
    "message": "hello world"
}

```
O servidor irá carregar a imagem BMP com o ID especificado na requisição e codificar a mensagem na imagem. Em seguida, o servidor retornará o ID da imagem codificada como JSON.

Exemplo de resposta:

```python
HTTP/1.1 200 OK
Content-Type: application/json

{

    "id": "57e2b2f1-e21e-41b5-b529-80b51dbc15d8"

}
```
# GET /image
Espera-se que este endpoint seja chamado com um ID de imagem como query string. O servidor irá retornar a imagem BMP correspondente.

Exemplo de resposta:

```python
HTTP/1.1 200 OK
Content-Type: image/bmp
Content-Disposition: attachment; filename=57e2b2f1-e21e-41b5-b529-80b51dbc15d8.bmp
```

# GET /decode
Essa rota é usada para decodificar a mensagem escondida na imagem.

Requisição
Método: GET
URL: /decode?id=<ID_DA_IMAGEM>
Onde <ID_DA_IMAGEM> é o ID da imagem a ser decodificada.

Exemplo de resposta:

Código de status: 200 OK
Corpo da resposta: JSON

O corpo da resposta é um objeto JSON com a seguinte estrutura:

```python
json

{
    "message": "<MENSAGEM_DECODIFICADA>"
}
```

Onde <MENSAGEM_DECODIFICADA> é a mensagem decodificada da imagem.

# Requisitos
Este projeto foi desenvolvido utilizando Python 3. Para utilizá-lo, é necessário ter o Python e o pip instalados na máquina.

# Ambiente virtual
Recomendo a utilização de um ambiente virtual para garantir a integridade do projeto e evitar possíveis conflitos com outras dependências instaladas na máquina. Para criar um ambiente virtual, execute o seguinte comando:

python3 -m venv .venv && source .venv/bin/activate
esse comando irá criar, renomear e ativar o ambiente

# Instalação
Clone o projeto para a sua máquina com o seguinte comando:

git clone com SSH: git@github.com:bruh-git/Caofraria.git

git clone com HTTPS: https://github.com/bruh-git/Caofraria.git


Em seguida, navegue até a pasta do projeto e instale as dependências com o seguinte comando:

pip install -r requirements.txt

#  Utilização
Para iniciar o servidor, execute o arquivo main.py com o seguinte comando:

python main.py
