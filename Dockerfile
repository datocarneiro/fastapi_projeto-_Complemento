# Dockerfile
FROM python:3.12-slim

# Diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do diretório atual para o diretório de trabalho
COPY . .


# # Comando para iniciar a aplicação 
  # sh: É o shell básico do Unix. Permite interpretar comandos em sequência e usar operadores como &&, ||, ;, etc.
    # -c: Flag para o shell sh que indica que você vai passar um comando como string.
    # "sleep 20 && uvicorn app.main:app --host 0.0.0.0 --port 9000":
    #     sleep 20: Aguarda 10 segundos antes de executar o próximo comando. 
    #     Isso é útil para garantir que o serviço de banco de dados (MySQL, no caso) esteja completamente inicializado.
        
CMD ["sh", "-c", "sleep 20 && uvicorn app.main:app --host 0.0.0.0 --port 9000"]