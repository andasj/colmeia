# colmeia

> Projeto que recebe como entrada uma imagem e informa se há alguma face presente nesta imagem.

## Instalação

No diretório que desejar baixe os arquivos do projeto:

```sh
git clone https://github.com/andasj/colmeia.git
```

Crie um ambiente virtual Python:

```sh
pip install virtualenv
```

```sh
virtualenv colmeia
```

Ative o ambiente virtual

```sh
source colmeia/bin/activate
```

Entre no diretório do projeto

```sh
cd colmeia/
```

Instale os frameworks necessários:

```sh
pip install -r requirements.txt
```

Agora para rodar o projeto basta:

```sh
python app.py
```

## Utilização

Acesse pelo web browser a url do projeto: http://localhost:5000/

Na rota http://localhost:5000/upload adicione a imagem que deseja avaliar a presença de faces.

Na rota http://localhost:5000/json verifique o resultado em forma de json da avaliação da presença de faces na imagem de entrada.

Na rota http://localhost:5000/image verifique o resultado visual da avaliação da presença de faces na imagem de entrada.