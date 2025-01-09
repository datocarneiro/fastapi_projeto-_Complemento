from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.db import adicionar_tarefa, listar_tarefas, buscar_tarefa_por_id, atualizar_tarefa, deletar_tarefa, tarefas_db
from app.auth import authenticate_user, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, fake_users_db
from app.models import TarefaCreate, Tarefa, BaseModel, TarefaUpdate
from pydantic import BaseModel
from datetime import datetime, timedelta
import  requests


router = APIRouter()

# Endpoint para criar uma tarefa
@router.post("/tarefas/", response_model=Tarefa)
def criar_tarefa(tarefa: TarefaCreate, current_user: dict = Depends(get_current_user)):
        # Validar o status da tarefa
        if tarefa.status not in ["pendente", "em andamento", "concluída"]:
            raise HTTPException(status_code=400, detail="status inválido")
        return adicionar_tarefa(tarefa)


# Endpoint para listar todas as tarefas
@router.get("/tarefas/", response_model=list[Tarefa])
def get_tarefas(current_user: dict = Depends(get_current_user)):
    return listar_tarefas()

########################################################################################################################
# Endpoint para buscar uma tarefa pelo id
@router.get("/tarefas/{id_tarefa}", response_model=Tarefa)
async def get_tarefa(id_tarefa: int, current_user: dict = Depends(get_current_user)):
    tarefa = buscar_tarefa_por_id(id_tarefa)
    if tarefa is None:
        raise HTTPException(status_code=404, detail = f"Tarefa ID:{id_tarefa} não encontrada, verifique se a tarefa existe")
    # return {"id_tarefa": id_tarefa, "details": tarefas_db[id_tarefa]}
    return tarefa

# @router.api_route("/tarefasid", methods=["GET", "POST"])
# async def get_tarefa(id: int = None, request: Tarefa = None):
#     if request:
#         id = Tarefa.id  # Para POST, pega o ID do corpo JSON
#     print(f'ID: {id}')
#     url = f'http://127.0.0.1:8000/{id}'
#     print(url)
#     response = requests.get(url)
#     print(response)
#     return response.json()


#######################################################################################################################
# atualizar 
@router.put("/tarefas/{id_tarefa}", response_model=Tarefa)
def update_tarefa(id_tarefa: int, tarefa: TarefaUpdate):
    updated_tarefa = atualizar_tarefa(id_tarefa, tarefa)
    if updated_tarefa is None:
        raise HTTPException(status_code=404, detail = f"Tarefa ID:{id_tarefa} não encontrada")
    return updated_tarefa

# Endpoint para deletar uma tarefa
@router.delete("/tarefas/{id_tarefa}", response_model=dict)
def delete_tarefa(id_tarefa: int):
    if deletar_tarefa(id_tarefa):
        return {'msg': f'Tarefa com ID:{id_tarefa} deletada com sucesso!'}
    raise HTTPException(status_code=404, detail= f"Tarefa ID:{id_tarefa} não encontrada")

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

# # Endpoint protegido (exemplo)
# @router.get("/tarefas/protegido")
# def read_protected_tarefas(current_user: dict = Depends(get_current_user)):
#     return {"msg": f"Bem-vindo, {current_user['username']}! Você está autenticado."}
