from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from typing import List
import pytz

# Declarative Base para os modelos SQLAlchemy
Base = declarative_base()

# Definindo o fuso horário
TZ = pytz.timezone("America/Sao_Paulo")

# Função para ajustar a data ao fuso horário
def now_tz():
    return datetime.now(TZ)

class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    titulo = Column(String(255), nullable=False, index=True)
    descricao = Column(String(500), nullable=True)
    status = Column(String(50), nullable=False, default="pendente", index=True)
    data_criacao = Column(DateTime, default=now_tz)  # Ajustando para o fuso horário
    data_atualizacao = Column(DateTime, default=now_tz, onupdate=now_tz)

# Modelos Pydantic para validação e serialização
class CriarTarefa(BaseModel):
    titulo: str
    descricao: Optional[str]
    status: Optional[str] = "pendente"

    model_config = ConfigDict(from_attributes=True)

class AtualizarTarefa(BaseModel):
    status: Optional[str]
    # titulo: Optional[str]
    # descricao: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class TarefaSchema(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str]
    status: str
    data_criacao: datetime
    data_atualizacao: datetime

    model_config = ConfigDict(from_attributes=True)

class TarefaListResponse(BaseModel):
    message: str = "Lista de tarefas"
    data: List[TarefaSchema] = []






