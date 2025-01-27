
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
from app.models import Base
import os
from alembic import command
from alembic.config import Config

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# essa função cria uma nova instância de sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        '''A função usa yield em vez de return para gerar a sessão do banco de dados.
        O uso de yield transforma a função em um "gerador" que permite ao FastAPI usar esta função como uma dependência. 
        O FastAPI usará a sessão gerada (db) e a injetará em qualquer função que dependa dela.'''
        yield db
    finally:
        db.close()

credenciais = {
    'USUARIO': os.getenv('DB_USER'),
    'SENHA': os.getenv('DB_PASSWORD'),
    'HOST': os.getenv('DB_HOST'),
    'PORT': os.getenv('DB_PORT'),
    'BANCO': os.getenv('DB_NAME'),
}

DATABASE_URL = f"mysql+pymysql://{credenciais.get('USUARIO')}:{credenciais.get('SENHA')}@{credenciais.get('HOST')}:{credenciais.get('PORT')}/{credenciais.get('BANCO')}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Verificar se o banco de dados existe e criá-lo se não existir
if not database_exists(engine.url):
    create_database(engine.url)

# Configuração do Alembic para aplicar as migrações
alembic_cfg = Config("alembic.ini")
command.upgrade(alembic_cfg, "head")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



