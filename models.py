import os
from dotenv import load_dotenv
from sqlalchemy import Column, create_engine, Integer, String, Boolean,Float, ForeignKey, Text, DateTime,JSON,Date, text, inspect
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone
# ══════════════════════════════════════════════════════════════════════════════
# COLE ESTES IMPORTS no topo do seu models.py (substitua os existentes se já
# houver DateTime ou Text):
#
# ══════════════════════════════════════════════════════════════════════════════


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
#Novo-BD-Nicole:mysql-anfitriao-prod-001.mysql.database.azure.com
DB = create_engine(DATABASE_URL,echo=True)
#DB = create_engine(url_conexao, echo=True)
# Testando a conexão
""" with DB.connect() as conn:
    resultado = conn.execute(text("SHOW TABLES"))
    tabelas = resultado.fetchall()
    print("\nTabelas (via SQL SHOW TABLES):")
    for (tabela_nome,) in tabelas:
        print(f"- {tabela_nome}")

with DB.connect() as conn:
    inspector = inspect(conn)
    
    # Lista todas as tabelas e suas colunas
    for tabela in inspector.get_table_names():
        print(f"\n📋 Tabela: {tabela}")
        colunas = inspector.get_columns(tabela)
        for coluna in colunas:
            print(f"  ├─ {coluna['name']} ({coluna['type']})")
 
 """
print(f"DATABASE_URL carregada: {DATABASE_URL}")
Base = declarative_base()

#criar as classes/tabelas do banco de dado
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id",Integer, primary_key=True,autoincrement=True)
    nome = Column("nome",String(100),nullable=False)
    email = Column("email",String(100),nullable=False, unique=True)
    senha = Column("senha",String(100),nullable=False)
    nascimento = Column("nascimento",Date,nullable=False)
    status = Column("status",String(50), default="ativo")
    criado_em  = Column("criado_em",  DateTime, default= datetime.now(timezone.utc))

    def __init__(self,nome,email,senha,criado_em,nascimento = None,status="ativo"):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.nascimento = nascimento
        self.status = status
        self.criado_em = criado_em
        

# ─── Message ──────────────────────────────────────────────────────────────────
class Message(Base):
    """Histórico de mensagens entre o usuário e o agente de IA."""
    __tablename__ = "messages"

    id         = Column("id",         Integer, primary_key=True, autoincrement=True)
    id_usuario = Column("id_usuario", ForeignKey("usuarios.id"), nullable=True)
    id_session = Column("id_visitante",String(36), nullable=True )
    conversa   = Column("conversa",   JSON,    nullable=False)
    criado_em  = Column("criado_em",  DateTime, default= datetime.now(timezone.utc))

    def __init__(self, id_usuario, conversa,id_session,criado_em):
        self.id_usuario = id_usuario
        self.id_session = id_session
        self.conversa   = conversa
        self.criado_em  = criado_em


Base.metadata.create_all(DB, checkfirst=True)
print("✅ Tabelas verificadas/criadas com sucesso!")