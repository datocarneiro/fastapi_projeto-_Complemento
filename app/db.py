from typing import List, Union
from app.models import TarefaCreate, Tarefa  # importando de models as classes TarefaCreate e Tarefa
from datetime import datetime
import pytz
from fastapi import HTTPException

tarefas_db: List[Tarefa] = []
id_counter = 1  # Contador para o campo id (autoincremento)
fuso_horario_brasilia = pytz.timezone('America/Sao_Paulo')

# Função para adicionar uma nova tarefa
def adicionar_tarefa(tarefa: TarefaCreate) -> Tarefa:
    global id_counter
    # Obtendo a data atual com o fuso horário de Brasília
    data_atual = datetime.now(fuso_horario_brasilia)
    
    nova_tarefa = Tarefa(
        id=id_counter,
        titulo=tarefa.titulo,
        descricao=tarefa.descricao,
        status=tarefa.status,
        data_criacao=data_atual,  # Data de criação com timezone
        data_atualizacao=data_atual  # Data de atualização com timezone
    )
    
    tarefas_db.append(nova_tarefa)
    id_counter += 1 
    return nova_tarefa

# Função para listar todas as tarefas
def listar_tarefas() -> Union[str, List[Tarefa]]:
    if not tarefas_db:
        raise HTTPException(status_code=404, detail="Não há tarefas criadas.")
    return tarefas_db

# Função para buscar uma tarefa pelo id
def buscar_tarefa_por_id(id_tarefa: int) -> Tarefa:
    for tarefa in tarefas_db:
        if tarefa.id == id_tarefa:
            return tarefa
    return None

# Função para atualizar uma tarefa
def atualizar_tarefa(id_tarefa: int, tarefa: TarefaCreate) -> Tarefa:
    for t in tarefas_db:
        if t.id == id_tarefa:
            t.status = tarefa.status
            t.data_atualizacao = datetime.now(fuso_horario_brasilia)

            # t.titulo = tarefa.titulo            # habilitar se quiser alterar tambem
            # t.descricao = tarefa.descricao      # habilitar se quiser alterar tambem
            
            return t
    return None

# Função para deletar uma tarefa
def deletar_tarefa(id_tarefa: int) -> bool:
    global tarefas_db
    tarefas_db = [t for t in tarefas_db if t.id != id_tarefa]
    return True
