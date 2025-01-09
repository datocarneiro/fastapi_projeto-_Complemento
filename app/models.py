from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Declarative Base para os modelos SQLAlchemy
Base = declarative_base()

class Tarefa(Base):
    __tablename__ = "tarefas"

    # Definição das colunas com suporte ao MySQL
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    titulo = Column(String(255), nullable=False, index=True)
    descricao = Column(String(500), nullable=True)
    status = Column(String(50), nullable=False, default="pendente", index=True)
    data_criacao = Column(DateTime, server_default=func.now())  # Usando `func.now()` para timestamps no MySQL
    data_atualizacao = Column(DateTime, server_default=func.now(), onupdate=func.now())

# Modelos Pydantic para validação e serialização
class CriarTarefa(BaseModel):
    titulo: str
    descricao: Optional[str]
    status: Optional[str] = "pendente"

    class Config:
        from_attributes = True

class AtualizarTarefa(BaseModel):
    titulo: Optional[str]
    descricao: Optional[str]
    status: Optional[str]

    class Config:
        from_attributes = True

class TarefaSchema(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str]
    status: str
    data_criacao: datetime
    data_atualizacao: datetime

    class Config:
        from_attributes = True
