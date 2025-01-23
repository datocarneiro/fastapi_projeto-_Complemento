from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.usuario_db import read_usuario_cpf
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from app.conn_database import get_db
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import pytz
import jwt 
import os


load_dotenv()

# Configuração de segurança
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 120

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de segurança por Bearer Token
security = HTTPBearer()

# gerar hash da senha
def get_password_hash(password):
    return pwd_context.hash(password)

# verificar senha
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(session_db, cpf: str, password: str):
    # Busca o usuário no banco pelo CPF
    user = read_usuario_cpf(session_db, cpf)
    if not user:
        return False
    # Verifica a senha fornecida com o hash armazenado
    if not verify_password(password, user.password):
        return False
    return user 

# Função para criar um token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    timezone = pytz.timezone("America/Sao_Paulo")  # Definindo o fuso horário
    current_time = datetime.now(timezone)
    if expires_delta:
        expire = current_time + expires_delta
    else:
        expire = current_time + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    try:
        # Gerando o token com PyJWT
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar o token: {str(e)}")
    
# Função para obter o usuário autenticado a partir do Bearer Token
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), session_db: Session = Depends(get_db)):
    token = credentials.credentials  # Obtém o token Bearer
    try:
        # Decodificar o token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        cpf: str = payload.get("sub")
        if cpf is None:
            raise HTTPException(
                status_code=401, detail="Não foi possível validar as credenciais."
            )
        return read_usuario_cpf(session_db, cpf)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail="Token expirado, faça login novamente."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401, detail="Token inválido, realize a autenticação."
        )

