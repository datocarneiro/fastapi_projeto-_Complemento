# API de Gerenciamento de Tarefas - dato®

## Visão Geral
Esta é uma API para gerenciamento de tarefas, desenvolvida em Python utilizando o framework FastAPI. Ela oferece funcionalidades como criar, listar, buscar, atualizar e deletar tarefas. Além disso, a API inclui autenticação baseada em JWT (JSON Web Tokens).

---

## Configuração do Ambiente Local

### 1. Requisitos
- Python 3.10+
- Git

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

## Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto com as seguintes configurações:
```env
SECRET_KEY=<sua_secret_key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=ajustar conforme a necessidade

ADMIN_USERNAME= Insiras a informação correta
ADMIN_FULL_NAME= Insiras a informação correta
ADMIN_EMAIL= Insiras a informação correta
ADMIN_PASSWORD= Insiras a informação correta

USERNAME=Insiras a informação correta
FULL_NAME=Insiras a informação correta
EMAIL=Insiras a informação correta
PASSWORD=Insiras a informação correta

DB_USER=Insiras a informação correta
DB_PASSWORD=Insiras a informação correta
DB_HOST=Insiras a informação correta
DB_NAME=Insiras a informação correta
DB_PORT=Insiras a informação correta
```
Substitua os valores com as configurações adequadas ao seu ambiente.

---

## Executar a API
Siga os passos abaixo para iniciar o servidor da API:

### 1. Iniciar o Servidor
Execute o seguinte comando no terminal:
```bash
$ uvicorn app.main:app --reload
```

### 2. Acessar a Documentação
Acesse a documentação interativa da API no navegador:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Testar a API

### 1. Executar Testes Automatizados
Os testes automatizados, pode executá-los com o seguinte comando:
```bash
$ pytest
```
Certifique-se de que o ambiente virtual esteja ativo.

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
├── pytest.ini
├── README.md
├── alembic.ini       
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