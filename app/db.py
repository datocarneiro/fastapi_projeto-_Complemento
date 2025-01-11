from sqlalchemy.orm import Session
from app.models import Tarefa, AtualizarTarefa

def get_tarefas(db: Session):
    tarefas = db.query(Tarefa).all()
    return tarefas

def push_tarefa(db: Session, tarefa: Tarefa) -> Tarefa:
    db.add(tarefa)
    db.commit()
    db.refresh(tarefa)
    return tarefa

def get_tarefa_id(db: Session, tarefa_id: int):
    return db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()

def update_tarefa_id(db: Session, tarefa: Tarefa, dados: AtualizarTarefa) -> Tarefa:
    if dados.status:
        tarefa.status = dados.status
    # if dados.titulo:
    #     tarefa.titulo = dados.titulo
    # if dados.descricao:
    #     tarefa.descricao = dados.descricao
    db.commit()
    db.refresh(tarefa)
    return tarefa

def delete_tarefa_id(db: Session, tarefa: Tarefa):
    db.delete(tarefa)
    db.commit()
