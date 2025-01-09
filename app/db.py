from sqlalchemy.orm import Session
from app.models import Tarefa, AtualizarTarefa
from app.database import SessionLocal

def adicionar_tarefa(session: Session, tarefa: Tarefa) -> Tarefa:
    session.add(tarefa)
    session.commit()
    session.refresh(tarefa)
    return tarefa

def listar_tarefas(session: Session):
    return session.query(Tarefa).all()

def buscar_tarefa_por_id(session: Session, tarefa_id: int):
    return session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()

def atualizar_tarefa_por_id(db: Session, tarefa: Tarefa, dados: AtualizarTarefa) -> Tarefa:
    if dados.titulo:
        tarefa.titulo = dados.titulo
    if dados.descricao:
        tarefa.descricao = dados.descricao
    if dados.status:
        tarefa.status = dados.status
    db.commit()
    db.refresh(tarefa)
    return tarefa

def deletar_tarefa_por_id(db: Session, tarefa: Tarefa):
    db.delete(tarefa)
    db.commit()
