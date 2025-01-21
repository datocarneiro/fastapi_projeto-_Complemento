from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import (AtualizarTarefa, CriarTarefa, TarefaID, TarefaListResponse, LoginInput,\
    BaseUsuarioCadastro, UsuarioListResponse, BaseUsuarioSimples, UsuarioID)
from app.db import insert_tarefa, get_all_tarefas, get_task_id, update_task_id, delete_task_id
from app.usuario_db import insert_usuario, read_usuarios, read_usuario_id
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
    tarefas = get_all_tarefas(db)
    if not tarefas:
        return TarefaListResponse(message="Não há tarefas criadas")
    return TarefaListResponse(data=tarefas)

@router.post("/tarefa", response_model=TarefaListResponse)
def push_tarefa(tarefa: CriarTarefa, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        tarefa_criada = insert_tarefa(db, tarefa)
        return TarefaListResponse(data=[tarefa_criada])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tarefa", response_model=TarefaListResponse)
def get_tarefa_id(tarefa_id: TarefaID, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    tarefa = get_task_id(db, tarefa_id.id)
    if not tarefa:
        raise HTTPException(status_code=404, detail=f"Tarefa ID: {tarefa_id.id} não encontrada")
    return TarefaListResponse(data=[tarefa])

@router.put("/tarefa", response_model=TarefaListResponse)
def update_tarefa(dados_tarefa: AtualizarTarefa, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    tarefa = get_task_id(db, dados_tarefa.id)
    if not tarefa:
        raise HTTPException(status_code=404, detail=f'Tarefa ID: {dados_tarefa.id} não encontrada')
    
    update_tarefa = update_task_id(db, tarefa, dados_tarefa)
    return TarefaListResponse(data=[update_tarefa])

@router.delete("/tarefa", response_model=TarefaListResponse)
def delete_tarefa_id(dados_tarefa: TarefaID, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    tarefa = get_task_id(db, dados_tarefa.id)
    if not tarefa:
        raise HTTPException(status_code=404, detail=f'Tarefa ID: {dados_tarefa.id} não encontrada')
    
    delete_task_id(db, tarefa)

    return TarefaListResponse(message=f'Tarefa ID: {dados_tarefa.id} deletada com sucesso. Informações da terefa excluída:',data=[tarefa])


@router.post("/auth")
def login(login_data: LoginInput):
    user = authenticate_user(fake_users_db, login_data.username, login_data.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/sinup", response_model=BaseUsuarioSimples)
def criar_usuario(usuario: BaseUsuarioCadastro, session_db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:       
        usuario_criado = insert_usuario(session_db, usuario)
        return usuario_criado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get('/usuarios', response_model=UsuarioListResponse)
def listar_usuario(sesion_db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    listar_usuario = read_usuarios(sesion_db)
    if not listar_usuario:
        return TarefaListResponse(message="Não há Usuarios cadastrados")
    return UsuarioListResponse(data=listar_usuario)

@router.get('/usuario', response_model= UsuarioListResponse)
def buscar_usuario_id(usuario_id: UsuarioID, sesion_db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    usuario_localizado = read_usuario_id(usuario_id.id, sesion_db)
    if not usuario_localizado:
        raise HTTPException(status_code=404, detail=f"Usuario ID: {usuario_id.id} não encontrado")
    return UsuarioListResponse(data=[usuario_localizado])