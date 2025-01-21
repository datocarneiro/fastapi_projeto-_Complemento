from sqlalchemy import select
from app.models import Usuario, UsuarioListResponse, BaseUsuarioSimples


def insert_usuario(session_db, usuario: Usuario ) -> Usuario:
    usuario_db = Usuario(nome = usuario.nome,
                         cpf = usuario.cpf,
                         password = usuario.password)              
    session_db.add(usuario_db)
    session_db.commit()
    session_db.refresh(usuario_db)
    return usuario_db

def read_usuarios(session_db) -> BaseUsuarioSimples:
    usuarios = session_db.scalars(select(Usuario).order_by(Usuario.id)).all()
    return usuarios

def read_usuario_id(usuario_id: int, session_db) -> BaseUsuarioSimples:
    query = select(Usuario).filter(Usuario.id == usuario_id)
    usuario_encontrado = session_db.scalars(query).first()
    return usuario_encontrado


def update_usuario():
    pass

def delete_usuario():
    pass

