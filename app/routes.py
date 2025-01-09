from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Tarefa, AtualizarTarefa
from app.db import (
    adicionar_tarefa,
    listar_tarefas,
    buscar_tarefa_por_id,
    atualizar_tarefa_por_id,
    deletar_tarefa_por_id,
)
from app.database import SessionLocal

# Criação do roteador
router = APIRouter()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para listar todas as tarefas
@router.get("/tarefas", response_model=list[Tarefa])
def obter_tarefas(db: Session = Depends(get_db)):
    tarefas = listar_tarefas(db)
    return tarefas

# Endpoint para criar uma nova tarefa
@router.post("/tarefas", response_model=Tarefa)
def criar_tarefa(titulo: str, descricao: str, db: Session = Depends(get_db)):
    nova_tarefa = Tarefa(titulo=titulo, descricao=descricao, status="pendente")
    tarefa_criada = adicionar_tarefa(db, nova_tarefa)
    return tarefa_criada

# Endpoint para obter uma tarefa por ID
@router.get("/tarefas/{tarefa_id}", response_model=Tarefa)
def obter_tarefa_por_id(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = buscar_tarefa_por_id(db, tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

# Endpoint para atualizar uma tarefa por ID
@router.put("/tarefas/{tarefa_id}", response_model=Tarefa)
def atualizar_tarefa(tarefa_id: int, dados_tarefa: AtualizarTarefa, db: Session = Depends(get_db)):
    tarefa = buscar_tarefa_por_id(db, tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    tarefa_atualizada = atualizar_tarefa_por_id(db, tarefa, dados_tarefa)
    return tarefa_atualizada

# Endpoint para deletar uma tarefa por ID
@router.delete("/tarefas/{tarefa_id}")
def deletar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = buscar_tarefa_por_id(db, tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    deletar_tarefa_por_id(db, tarefa)
    return {"message": f"Tarefa {tarefa_id} deletada com sucesso"}
