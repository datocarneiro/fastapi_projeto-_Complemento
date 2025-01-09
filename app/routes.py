from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models import Tarefa as ModelTarefa, AtualizarTarefa, CriarTarefa, TarefaSchema, TarefaListResponse
from app.db import (adicionar_tarefa, listar_tarefas, buscar_tarefa_por_id, atualizar_tarefa_por_id, deletar_tarefa_por_id)
from app.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_user, fake_users_db
from app.database import SessionLocal
from typing import List


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/tarefas", response_model=TarefaListResponse)
def obter_tarefas(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    tarefas = listar_tarefas(db)
    if not tarefas:
        return TarefaListResponse(message="Não há tarefas criadas")
    return TarefaListResponse(data=tarefas)

@router.post("/tarefas", response_model=TarefaSchema)
def criar_tarefa(tarefa: CriarTarefa, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if tarefa.status not in ["pendente", "em andamento", "concluída"]:
        raise HTTPException(status_code=400, detail="status inválido. Deve ser 'pendente', 'em andamento' ou 'concluída'")
    nova_tarefa = ModelTarefa(titulo=tarefa.titulo, descricao=tarefa.descricao, status=tarefa.status)
    tarefa_criada = adicionar_tarefa(db, nova_tarefa)
    return tarefa_criada

@router.get("/tarefas/{tarefa_id}", response_model=TarefaSchema)
def obter_tarefa_por_id(tarefa_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    tarefa = buscar_tarefa_por_id(db, tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

@router.put("/tarefas/{tarefa_id}", response_model=TarefaSchema)
def atualizar_tarefa(tarefa_id: int, dados_tarefa: AtualizarTarefa, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    tarefa = buscar_tarefa_por_id(db, tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    if dados_tarefa.status and dados_tarefa.status not in ["pendente", "em andamento", "concluída"]:
        raise HTTPException(status_code=400, detail="status inválido. Deve ser 'pendente', 'em andamento' ou 'concluída'")
    
    tarefa_atualizada = atualizar_tarefa_por_id(db, tarefa, dados_tarefa)
    return tarefa_atualizada

@router.delete("/tarefas/{tarefa_id}")
def deletar_tarefa(tarefa_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    tarefa = buscar_tarefa_por_id(db, tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    deletar_tarefa_por_id(db, tarefa)
    return {"message": f"Tarefa {tarefa_id} deletada com sucesso"}

class LoginInput(BaseModel):
    username: str
    password: str

@router.post("/auth")
def login(login_data: LoginInput):
    user = authenticate_user(fake_users_db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
