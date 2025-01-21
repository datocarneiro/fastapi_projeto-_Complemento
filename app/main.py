from fastapi import FastAPI
from app.routes import router as tarefa_router

descrição = '''
    ## Visão Geral
    Esta é uma API para gerenciamento de tarefas. 
    Ela oferece funcionalidades como criar, listar, buscar, atualizar e deletar tarefas. Além disso,\n
    a API inclui autenticação baseada em JWT (JSON Web Tokens).
'''

app = FastAPI(title='API de Gerenciamento de Tarefas - dato®',
              version='2.0',
              description=descrição,
              debug=True
              )

# Incluir os endpoints no FastAPI
app.include_router(tarefa_router)   # tarefa_router é o alias da instancia router (importada acima)

@app.get("/")
def home():
    return {"message": "API de gerenciamento de tarefas - DATO®"}



