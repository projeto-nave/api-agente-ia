import os
from dotenv import load_dotenv
from sqlalchemy import Column, create_engine, Integer, String, Boolean,Float, ForeignKey, Text, DateTime,JSON,Date
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone
# ══════════════════════════════════════════════════════════════════════════════
# COLE ESTES IMPORTS no topo do seu models.py (substitua os existentes se já
# houver DateTime ou Text):
#
# ══════════════════════════════════════════════════════════════════════════════

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
DB = create_engine(DATABASE_URL)
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
    ativo = Column("ativo",Boolean, default=True)
    admin = Column("admin",Boolean, default=False)

    def __init__(self,nome,email,senha,ativo=True,admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

# ─── Consent ──────────────────────────────────────────────────────────────────
class Consent(Base):
    """Permissões do agente de IA concedidas por usuário."""
    __tablename__ = "consents"

    id          = Column("id",         Integer, primary_key=True, autoincrement=True)
    id_usuario  = Column("id_usuario", ForeignKey("usuarios.id"), nullable=False)
    permissao   = Column("permissao",  String(100),  nullable=False)   # ex: "web_search", "send_email"
    ativo       = Column("ativo",      Boolean, default=True)
    criado_em   = Column("criado_em",  DateTime, default=lambda: datetime.now(timezone.utc))

    def __init__(self, id_usuario, permissao, ativo=True):
        self.id_usuario = id_usuario
        self.permissao  = permissao
        self.ativo      = ativo


# ─── Message ──────────────────────────────────────────────────────────────────
class Message(Base):
    """Histórico de mensagens entre o usuário e o agente de IA."""
    __tablename__ = "messages"

    id         = Column("id",         Integer, primary_key=True, autoincrement=True)
    id_usuario = Column("id_usuario", ForeignKey("usuarios.id"), nullable=False)
    conversa   = Column("conversa",   JSON,    nullable=False)
    criado_em  = Column("criado_em",  DateTime, default=lambda: datetime.now(timezone.utc))

    def __init__(self, id_usuario, conversa):
        self.id_usuario = id_usuario
        self.conversa   = conversa
