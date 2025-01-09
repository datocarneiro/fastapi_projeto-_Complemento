from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Variáveis de ambiente individuais para a configuração do banco de dados
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

# Construir a URL do banco de dados
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Criação do engine para o MySQL
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Configuração da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para os modelos
Base = declarative_base()

# Definição dos modelos
class Tarefa(Base):
    __tablename__ = "tarefas"
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, index=True)
    concluida = Column(Integer, default=0)

# Criar todas as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

