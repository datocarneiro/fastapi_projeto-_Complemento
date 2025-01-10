# API de Gerenciamento de Tarefas - dato®

## Visão Geral
Esta é uma API para gerenciamento de tarefas, desenvolvida em Python utilizando o framework FastAPI. Ela oferece funcionalidades como criar, listar, buscar, atualizar e deletar tarefas. Além disso, a API inclui autenticação baseada em JWT (JSON Web Tokens).

---

## Configuração do Ambiente Local

### 1. Requisitos
- Python 3.12.1
- Git
- Docker
- Docker Compose

### 2. Clonar o Repositório
```bash
$ git clone <URL_DO_REPOSITORIO>
$ cd <NOME_DO_REPOSITORIO>
```

### 3. Criar Ambiente Virtual
Crie um ambiente virtual utilizando o comando abaixo:
```bash
$ python -m venv venv
```
Ative o ambiente virtual:
- **Windows**:
  ```bash
  $ venv\Scripts\activate
  ```
- **Linux/macOS**:
  ```bash
  $ source venv/bin/activate
  ```

### 4. Instalar Dependências
Instale todas as dependências do projeto presentes no arquivo `requirements.txt`:
```bash
$ pip install -r requirements.txt
```

### 5. Configurar o Banco de Dados
Certifique-se de que o banco de dados está configurado corretamente. Execute as migrações necessárias:
```bash
$ alembic upgrade head
```

---

## Dockerização da API

### Executar o Projeto com Docker Compose

Certifique-se de que o Docker esteja instalado e configurado corretamente. Para construir a imagem e iniciar os containers configurados no `docker-compose.yml`, execute:

```bash
$ docker-compose up --build
```

Isso irá iniciar os containers da API e do banco de dados automaticamente.


### 3. Parar os Containers
Para parar os containers, utilize:
```bash
$ docker-compose down
```

---

## Migrações do Banco de Dados

As migrações são gerenciadas pelo Alembic. Abaixo estão os principais comandos para lidar com migrações:

### 1. Criar uma Nova Migração
Ao alterar os modelos, crie uma nova migração:
```bash
$ alembic revision --autogenerate -m "Descrição da migração"
```

### 2. Aplicar Migrações
Para aplicar as migrações ao banco de dados:
```bash
$ alembic upgrade head
```

### 3. Reverter Migrações
Para reverter a última migração:
```bash
$ alembic downgrade -1
```

### 4. Configurar Alembic
O arquivo `alembic.ini` contém as configurações principais. Certifique-se de que o caminho do banco de dados está correto no campo `sqlalchemy.url`.

---

## Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto com as seguintes configurações:
```env
SECRET_KEY=<sua_secret_key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=<valor>

ADMIN_USERNAME=<valor>
ADMIN_FULL_NAME=<valor>
ADMIN_EMAIL=<valor>
ADMIN_PASSWORD=<valor>

USERNAME=<valor>
FULL_NAME=<valor>
EMAIL=<valor>
PASSWORD=<valor>

DB_USER=<valor>
DB_PASSWORD=<valor>
DB_HOST=<valor>
DB_NAME=<valor>
DB_PORT=<valor>
```
<h4 style="color:#ff6900">Substitua os valores com as configurações adequadas ao seu ambiente.</h4>


---

## Executar a API

### 1. Iniciar o Servidor Local
Execute o seguinte comando no terminal:
```bash
$ uvicorn app.main:app --reload
```

### 2. Acessar a Documentação
<h3 style="color:#ff6900">Acesse a documentação interativa da API no navegador:</h3>

- **Swagger UI**: [http://localhost:8000/docs](http://127.0.0.1:8000/docs)


- **Redoc**: [http://localhost:8000/redoc](http://127.0.0.1:8000/redoc)


---

## Testar a API

### 1. Executar Testes Automatizados
Os testes automatizados podem ser executados com o seguinte comando:
```bash
$ pytest
```


---

## Estrutura do Projeto

```plaintext
.
├── alembic
│   ├── versions
│       ├── <hash>_create_tarefas_table.py
│   ├── env.py
│   ├── README.md
├── app
│   ├── auth.py
│   ├── database.py
│   ├── db.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
├── tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_routes.py
├── requirements.txt
├── .env
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── pytest.ini
├── README.md
├── alembic.ini       
├── wait-for-it.sh      
```

### Descrição dos Arquivos
- **`main.py`**: Arquivo principal para inicialização da API.
- **`auth.py`**: Implementação da autenticação JWT.
- **`db.py`**: Funções relacionadas ao banco de dados em memória.
- **`routes.py`**: Rotas da API para gerenciamento de tarefas.
- **`models.py`**: Modelos de dados (Pydantic).
- **`requirements.txt`**: Dependências do projeto.
- **`.env`**: Configurações sensíveis como chave secreta.

---

## Recursos da API

### Endpoints Principais

#### Tarefas
- **POST `/tarefas/`**: Criar uma nova tarefa.
- **GET `/tarefas/`**: Listar todas as tarefas.
- **GET `/tarefas/{id}`**: Buscar uma tarefa pelo ID.
- **PUT `/tarefas/{id}`**: Atualizar uma tarefa.
- **DELETE `/tarefas/{id}`**: Deletar uma tarefa.

#### Autenticação
- **POST `/auth`**: Obter token de autenticação.

---

## Exemplos de Uso

### Criar uma Tarefa
```bash
curl -X POST "http://127.0.0.1:8000/tarefas/" -H "accept: application/json" -H "Content-Type: application/json" -d '{"titulo": "Nova Tarefa", "descricao": "Descrição da tarefa"}'
```

### Listar Tarefas
```bash
curl -X GET "http://127.0.0.1:8000/tarefas/" -H "accept: application/json"
```

---

## Contribuição
Sinta-se à vontade para contribuir com melhorias para este projeto. Por favor, crie um pull request ou abra uma issue no repositório.

---

## Licença - [Dato®]

Este projeto é licenciado sob a [MIT License](https://opensource.org/licenses/MIT).  
Você pode usar, modificar e distribuir o código, desde que mantenha o aviso de copyright.

Este projeto utiliza bibliotecas de terceiros. Consulte o arquivo `LICENSE-THIRD-PARTY` para mais detalhes.

---

## Autor
- [Dato®]

