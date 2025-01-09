from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# URL do banco de dados configurada para MySQL
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@localhost/tarefas_db")

# Criação do engine para o MySQL
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Configuração da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para os modelos
Base = declarative_base()
