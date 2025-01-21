from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from app.models import Tarefa, AtualizarTarefa

def get_all_tarefas(db: Session):
    tarefas = db.query(Tarefa).all()
    return tarefas

def insert_tarefa(db: Session, tarefa: Tarefa) -> Tarefa:
    nova_tarefa = Tarefa(titulo=tarefa.titulo, 
                         descricao=tarefa.descricao,
                         status=tarefa.status,
                         nivel_prioridade=tarefa.nivel_prioridade,
                         usuario_id=tarefa.usuario_id)
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return nova_tarefa

def get_task_id(db: Session, tarefa_id: int) -> Tarefa:
    query = select(Tarefa).options(joinedload(Tarefa.usuario)).filter(Tarefa.id == tarefa_id)
    return db.scalars(query).first()


def update_task_id(db: Session, tarefa: Tarefa, dados: AtualizarTarefa) -> Tarefa:
    if dados.id:
        tarefa.id= dados.id
    if dados.status:
        tarefa.status = dados.status
    if dados.nivel_prioridade:
        tarefa.nivel_prioridade = dados.nivel_prioridade
    if dados.titulo:
        tarefa.titulo = dados.titulo
    if dados.descricao:
        tarefa.descricao = dados.descricao
    db.commit()
    db.refresh(tarefa)
    return tarefa

def delete_task_id(db: Session, tarefa_id: Tarefa):
    db.delete(tarefa_id)
    db.commit()
