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

# Copia o wait-for-it.sh para o diretório de trabalho
COPY wait-for-it.sh /wait-for-it.sh

# Garante permissões de execução para wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Comando para iniciar a aplicação (definido no docker-compose.yml)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9000"]
