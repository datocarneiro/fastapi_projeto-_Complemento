from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Tarefa as ModelTarefa, AtualizarTarefa, CriarTarefa, TarefaSchema
from app.db import (adicionar_tarefa, listar_tarefas, buscar_tarefa_por_id, atualizar_tarefa_por_id, deletar_tarefa_por_id,)
from app.auth import authenticate_user, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, fake_users_db
from app.database import SessionLocal
from typing import List
from pydantic import BaseModel
from datetime import datetime, timedelta

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/tarefas", response_model=List[TarefaSchema])
def obter_tarefas(db: Session = Depends(get_db)):
    tarefas = listar_tarefas(db)
    return tarefas

@router.post("/tarefas", response_model=TarefaSchema)
def criar_tarefa(titulo: str, descricao: str, db: Session = Depends(get_db)):
    nova_tarefa = ModelTarefa(titulo=titulo, descricao=descricao, status="pendente")
    tarefa_criada = adicionar_tarefa(db, nova_tarefa)
    return tarefa_criada

@router.get("/tarefas/{tarefa_id}", response_model=TarefaSchema)
def obter_tarefa_por_id(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = buscar_tarefa_por_id(db, tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

@router.put("/tarefas/{tarefa_id}", response_model=TarefaSchema)
def atualizar_tarefa(tarefa_id: int, dados_tarefa: AtualizarTarefa, db: Session = Depends(get_db)):
    tarefa = buscar_tarefa_por_id(db, tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    tarefa_atualizada = atualizar_tarefa_por_id(db, tarefa, dados_tarefa)
    return tarefa_atualizada

@router.delete("/tarefas/{tarefa_id}")
def deletar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
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