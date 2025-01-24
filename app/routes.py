from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import (AtualizarTarefa, CriarTarefa, TarefaID, TarefaListResponse, BaseUsuarioAuth,\
    BaseUsuarioAuthResponse, BaseUsuarioCadastro, UsuarioListResponse, BaseUsuarioSimples, UsuarioID)
from app.db import insert_tarefa, get_all_tarefas, get_task_id, update_task_id, delete_task_id
from app.usuario_db import insert_usuario, read_usuario_cpf, read_usuarios, read_usuario_id
from app.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_user, get_password_hash
from app.validador_cpf import validar_cpf
from app.conn_database import get_db

router = APIRouter()

@router.get("/tarefas", response_model=TarefaListResponse)
def get_tarefas(session_db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    
    try:
        tarefas = get_all_tarefas(session_db)  # Função que busca as tarefas no banco
        if not tarefas:
            return TarefaListResponse(message="Não há tarefas criadas")
        return TarefaListResponse(data=tarefas)
    except Exception as e:
        # Mensagem genérica de erro ou detalhada conforme necessidade
        return TarefaListResponse(message=f"Erro ao buscar tarefas: {str(e)}")

@router.post("/tarefa", response_model=TarefaListResponse)
def push_tarefa(tarefa: CriarTarefa, session_db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    usuario_id = current_user
    if not usuario_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado.")

    try:
        # Passa o usuário autenticado para a tarefa
        tarefa_criada = insert_tarefa(session_db, tarefa, usuario_id)
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

@router.post("/sinup",response_model=BaseUsuarioSimples)
def sinup(usuario: BaseUsuarioCadastro, session_db: Session = Depends(get_db)):
    valida_cpf = validar_cpf(usuario.cpf)
    encontrar_usuario = read_usuario_cpf(session_db, valida_cpf)
    if encontrar_usuario:
        raise HTTPException(status_code=404, detail=f"Ja existe um usuario cadastrado com o CPF: {valida_cpf}.")

    # gera  um hash para asenha do usuario
    usuario.password = get_password_hash(usuario.password)
    try:       
        usuario_criado = insert_usuario(session_db, usuario)
        return usuario_criado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/login', response_model=BaseUsuarioAuthResponse)
def login(login_data: BaseUsuarioAuth, session_db: Session = Depends(get_db)):
    valida_cpf = validar_cpf(login_data.cpf)
    verifica_usuario = read_usuario_cpf(session_db, valida_cpf)
    if not verifica_usuario:
        raise HTTPException(status_code=404, detail="Usuário não cadastrado, registre-se.")
    
    # Autentica o usuário
    user = authenticate_user(session_db, valida_cpf, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    
    # Cria o token JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.cpf}, expires_delta=access_token_expires)
    
    usuario_data = {
        "nome": user.nome,
        "cpf": user.cpf,
        "active": user.active,
        "access_token": access_token,
        "token_type": "bearer"
    }
    
    return  {"data":usuario_data}
        
