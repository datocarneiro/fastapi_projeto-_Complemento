
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



