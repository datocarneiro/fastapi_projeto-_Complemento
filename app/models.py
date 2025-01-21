from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, validates, relationship, Mapped
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, ClassVar
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

class Usuario(Base):
    __tablename__ = "conta_usuario"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String(255), nullable=False, index=True)
    cpf = Column(String(500), nullable=False)
    password = Column(String(20), nullable=False, index=True)
    active = Column(Boolean(), nullable=True, default=True)
    data_criacao = Column(DateTime, default=now_tz)
    data_atualizacao = Column(DateTime, default=now_tz, onupdate=now_tz)

    tarefas: Mapped[List['Tarefa']] = relationship('Tarefa', back_populates='usuario')

class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    titulo = Column(String(255), nullable=False, index=True)
    descricao = Column(String(500), nullable=True)
    status = Column(String(50), nullable=False, default="pendente", index=True)
    nivel_prioridade = Column(String(50), nullable=True, index=True)
    data_criacao = Column(DateTime, default=now_tz)
    data_atualizacao = Column(DateTime, default=now_tz, onupdate=now_tz)

    usuario_id = Column(Integer, ForeignKey("conta_usuario.id", name='fk_usuario'))
    usuario = relationship('Usuario', back_populates="tarefas")

    # Definindo os valores válidos
    STATUS_VALIDOS = ["pendente", "em andamento", "concluída"]
    NIVEIS_VALIDOS = ["baixo", "médio", "alto", "urgente"]

    @validates("status")
    def validate_status(self, key, value):
        if value not in self.STATUS_VALIDOS and value is not None:
            raise ValueError(f"Status '{value}' inválido. Deve ser um dos {self.STATUS_VALIDOS}.")
        return value

    @validates("nivel_prioridade")
    def validate_nivel_prioridade(self, key, value):
        # if value is None:
        #     return "baixo"
        if value not in self.NIVEIS_VALIDOS and value is not None:
            raise ValueError(f"Nível de prioridade '{value}' inválido. Deve ser um dos {self.NIVEIS_VALIDOS}.")
        return value
    
#################################################################################
#                                   SCHEMAS TAREFAS                     
#################################################################################
# Modelos Pydantic para validação e serialização
class CriarTarefa(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    status: str  # Agora o 'status' é obrigatório
    nivel_prioridade: Optional[str] = None  # 'nivel_prioridade' é opcional
    usuario_id: int

    model_config = ConfigDict(from_attributes=True)

class AtualizarTarefa(BaseModel):
    id: int
    status: str 
    nivel_prioridade: Optional[str] = None
    titulo:  Optional[str] = None
    descricao: Optional[str] = None

    STATUS_VALIDOS: ClassVar[list] = ["pendente", "em andamento", "concluída"]
    NIVEIS_VALIDOS: ClassVar[list] = ["baixo", "médio", "alto", "urgente"]

    @field_validator("status")
    def validar_status(cls, value):
        if value and value not in cls.STATUS_VALIDOS:
            raise ValueError(f"Status '{value}' inválido. Deve ser um dos: {cls.STATUS_VALIDOS}")
        return value

    @field_validator("nivel_prioridade")
    def validar_nivel_prioridade(cls, value):
        if value and value not in cls.NIVEIS_VALIDOS:
            raise ValueError(f"Nível de prioridade '{value}' inválido. Deve ser um dos: {cls.NIVEIS_VALIDOS}")
        return value

    model_config = ConfigDict(from_attributes=True)

class TarefaID(BaseModel):
    id: int 

    model_config = ConfigDict(from_attributes=True)



class TarefaSimples(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str]
    status: str
    nivel_prioridade: Optional[str]
    data_criacao: datetime
    data_atualizacao: datetime
    
    model_config = ConfigDict(from_attributes=True)

class TarefaCompleta(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str]
    status: str
    nivel_prioridade: Optional[str]
    data_criacao: datetime
    data_atualizacao: datetime
    usuario_id: Optional[int]
    usuario: Optional["BaseUsuarioSimples"]
  
    model_config = ConfigDict(from_attributes=True)

class TarefaSchema(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str]
    status: str
    nivel_prioridade: Optional[str]
    data_criacao: datetime
    data_atualizacao: datetime
    usuario_id: Optional[int]
    usuario: Optional["BaseUsuarioSimples"]
  
    model_config = ConfigDict(from_attributes=True)

# base das resposnses
class TarefaListResponse(BaseModel):
    message: str = "Operation completed successfully"
    data: List[TarefaCompleta] = []

#################################################################################
#                                   SCHEMAS USUARIO                     
#################################################################################

class BaseUsuarioCadastro(BaseModel):
    id: Optional[int] = None
    nome: str
    cpf: str
    password: str
    
    model_config = ConfigDict(from_attributes=True)

class BaseUsuarioSimples(BaseModel):
    id: Optional[int] = None
    nome: str
    cpf: str
    active: Optional[bool] = None
    data_criacao: datetime
    data_atualizacao: datetime

    model_config = ConfigDict(from_attributes=True)

class BaseUsuarioCompleto(BaseModel):
    id: Optional[int] = None
    nome: str
    cpf: str
    active: Optional[bool] = None
    data_criacao: datetime
    data_atualizacao: datetime
    tarefas: List[TarefaSimples] = []

    model_config = ConfigDict(from_attributes=True)

class BaseUsuarioSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    cpf: str
    password: Optional[str] = None
    active: Optional[bool] = None
    data_criacao: datetime
    data_atualizacao: datetime
    

    model_config = ConfigDict(from_attributes=True)

# base das resposnses Usuario
class UsuarioListResponse(BaseModel):
    message: str = "Operation completed successfully"
    data: List[BaseUsuarioCompleto] = []


class UsuarioID(BaseModel):
    id: int 

class LoginInput(BaseModel):
    username: str
    password: str
