from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import database_exists, create_database
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

print(DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




# Criação do engine para o MySQL
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Verificar se o banco de dados existe e criá-lo se não existir
if not database_exists(engine.url):
    create_database(engine.url)

# Configuração da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para os modelos
Base = declarative_base()

# Definição dos modelos
class Tarefa(Base):
    __tablename__ = "tarefas"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    titulo = Column(String(255), nullable=False, index=True)
    descricao = Column(String(500), nullable=True)
    status = Column(String(50), nullable=False, default="pendente", index=True)
    data_criacao = Column(DateTime, server_default=func.now())
    data_atualizacao = Column(DateTime, server_default=func.now(), onupdate=func.now())


# Criar todas as tabelas no banco de dados
Base.metadata.create_all(bind=engine)
