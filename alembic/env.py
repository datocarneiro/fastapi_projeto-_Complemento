import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Adicionar o diretório raiz do projeto ao caminho de importação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar a Base e os modelos
from app.database import Base
from app.models import Tarefa

# Esta linha carrega a configuração do arquivo de configuração.
config = context.config

# Esta linha carrega a configuração de log do arquivo de configuração.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Este é o alvo do metadata para 'autogenerate'
target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(url=config.get_main_option("sqlalchemy.url"))
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
