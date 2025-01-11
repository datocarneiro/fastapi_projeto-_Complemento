from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models import Tarefa as ModelTarefa, AtualizarTarefa, CriarTarefa, TarefaSchema, TarefaListResponse
from app.db import push_tarefa, get_tarefas, get_tarefa_id, update_tarefa_id, delete_tarefa_id
from app.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_user, fake_users_db
from app.conn_database import SessionLocal

router = APIRouter()

# essa função cria uma nova instância de sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        '''A função usa yield em vez de return para gerar a sessão do banco de dados.
        O uso de yield transforma a função em um "gerador" que permite ao FastAPI usar esta função como uma dependência. 
        O FastAPI usará a sessão gerada (db) e a injetará em qualquer função que dependa dela.'''
        yield db
    finally:
        db.close()


@router.get("/tarefas", response_model=TarefaListResponse)
def get_tarefas(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    tarefas = get_tarefas(db)
    if not tarefas:
        return TarefaListResponse(message="Não há tarefas criadas")
    return TarefaListResponse(data=tarefas)

@router.post("/tarefas", response_model=TarefaSchema)
def push_tarefa(tarefa: CriarTarefa, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if tarefa.status not in ["pendente", "em andamento", "concluída"]:
        raise HTTPException(status_code=400, detail="status inválido. Deve ser 'pendente', 'em andamento' ou 'concluída'")
    nova_tarefa = ModelTarefa(titulo=tarefa.titulo, descricao=tarefa.descricao, status=tarefa.status)
    tarefa_criada = push_tarefa(db, nova_tarefa)
    return tarefa_criada

@router.get("/tarefas/{tarefa_id}", response_model=TarefaSchema)
def get_tarefa_id(tarefa_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    tarefa = get_tarefa_id(db, tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

@router.put("/tarefas/{tarefa_id}", response_model=TarefaSchema)
def update_tarefa(tarefa_id: int, dados_tarefa: AtualizarTarefa, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    tarefa = get_tarefa_id(db, tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    if dados_tarefa.status and dados_tarefa.status not in ["pendente", "em andamento", "concluída"]:
        raise HTTPException(status_code=400, detail="status inválido. Deve ser 'pendente', 'em andamento' ou 'concluída'")
    
    update_tarefa = update_tarefa_id(db, tarefa, dados_tarefa)
    return update_tarefa

@router.delete("/tarefas/{tarefa_id}")
def delete_tarefa_id(tarefa_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    tarefa = get_tarefa_id(db, tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    delete_tarefa_id(db, tarefa)
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
