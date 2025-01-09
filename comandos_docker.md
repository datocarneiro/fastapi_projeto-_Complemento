Claro, aqui estão alguns comandos básicos do Docker que são extremamente úteis para começar:

### Comandos Gerais
- **`docker --version`**: Verifica a versão instalada do Docker.
- **`docker info`**: Exibe informações detalhadas sobre a instalação do Docker.
- **`docker help`**: Lista todos os comandos disponíveis e suas descrições.

### Imagens
- **`docker build -t <nome_da_imagem> .`**: Constrói uma nova imagem Docker a partir do Dockerfile no diretório atual.
- **`docker images`**: Lista todas as imagens Docker armazenadas localmente.
- **`docker rmi <imagem_id>`**: Remove uma imagem Docker especificada pelo ID.

### Contêineres
- **`docker run -d -p <porta_local>:<porta_container> --name <nome_do_container> <nome_da_imagem>`**: Inicia um novo contêiner com a imagem especificada em segundo plano.
- **`docker ps`**: Lista todos os contêineres em execução.
- **`docker ps -a`**: Lista todos os contêineres, incluindo aqueles que estão parados.
- **`docker stop <nome_do_container>`**: Para um contêiner em execução.
- **`docker start <nome_do_container>`**: Inicia um contêiner parado.
- **`docker restart <nome_do_container>`**: Reinicia um contêiner.
- **`docker rm <nome_do_container>`**: Remove um contêiner parado.
- **`docker logs <nome_do_container>`**: Exibe os logs de um contêiner em execução.

### Volumes
- **`docker volume create <nome_do_volume>`**: Cria um novo volume Docker.
- **`docker volume ls`**: Lista todos os volumes Docker.
- **`docker volume rm <nome_do_volume>`**: Remove um volume Docker.

### Redes
- **`docker network create <nome_da_rede>`**: Cria uma nova rede Docker.
- **`docker network ls`**: Lista todas as redes Docker.
- **`docker network rm <nome_da_rede>`**: Remove uma rede Docker.

### Docker Compose
- **`docker-compose up`**: Inicia os serviços definidos no arquivo `docker-compose.yml`.
- **`docker-compose up --build`**: Constrói as imagens antes de iniciar os serviços.
- **`docker-compose down`**: Para e remove os contêineres, redes e volumes definidos no `docker-compose.yml`.
- **`docker-compose ps`**: Lista todos os contêineres em execução gerenciados pelo Docker Compose.

Esses comandos são essenciais para o gerenciamento de imagens, contêineres, volumes e redes no Docker, e também para orquestração de múltiplos serviços usando Docker Compose. Se precisar de mais alguma coisa ou tiver alguma dúvida específica, estarei por aqui! 🚀