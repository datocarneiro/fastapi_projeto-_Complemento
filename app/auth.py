from datetime import datetime, timedelta
import pytz
import jwt 
from passlib.context import CryptContext
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer # "OAuth2PasswordBearer" é para auth 2.0
from dotenv import load_dotenv
import os

load_dotenv()

# Configuração de segurança
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 300

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de segurança por Bearer Token
security = HTTPBearer()

# # Esquema de segurança por AUTH 2.0
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

# Usuários fictícios (substitua por um banco de dados)
fake_users_db = {
    "admin": {
        "username": os.getenv("ADMIN_USERNAME"),
        "full_name": os.getenv("ADMIN_FULL_NAME"),
        "email": os.getenv("ADMIN_EMAIL"),
        "hashed_password": pwd_context.hash(os.getenv("ADMIN_PASSWORD")),
        "disabled": False,
    },
    "user1": {
        "username": os.getenv("USERNAME"),
        "full_name": os.getenv("FULL_NAME"),
        "email": os.getenv("EMAIL"),
        "hashed_password": pwd_context.hash(os.getenv("PASSWORD")),
        "disabled": False,
    },
}


# Função para verificar senha
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Função para obter hash da senha
def get_password_hash(password):
    return pwd_context.hash(password)

# Função para obter usuário pelo nome
def get_user(db, username: str):
    return db.get(username)

# Função para autenticar o usuário
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
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
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials  # Obtém o token Bearer
    try:
        # Decodificar o token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401, detail="Não foi possível validar as credenciais."
            )
        return get_user(fake_users_db, username)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail="Token expirado, faça login novamente."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401, detail="Token inválido, realize a autenticação."
        )


# # Função para obter o usuário autenticado por AUTH 2.0
# def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         # Decodificando o token com PyJWT
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise HTTPException(
#                 status_code=401, detail="Não foi possível validar as credenciais, realize a autenticação."
#             )
#         return get_user(fake_users_db, username)
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(
#             status_code=401, detail="Token expirado, faça login novamente."
#         )
#     except jwt.InvalidTokenError:
#         raise HTTPException(
#             status_code=401, detail="Token inválido, realize a autenticação."
#         )
