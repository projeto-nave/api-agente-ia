
from pydantic import BaseModel
from typing import Optional,List

class Usuarioschema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True


class LoguinSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True
# ══════════════════════════════════════════════════════════════════════════════
# COLE ESTES SCHEMAS no seu schemas.py existente (após os schemas já existentes)
# Adicione também este import no topo: from datetime import datetime
# ══════════════════════════════════════════════════════════════════════════════

from datetime import datetime


# ─── Consent ─────────────────────────────────────────────────────────────────

class ConsentCreateSchema(BaseModel):
    permissao: str   # ex: "web_search", "send_email", "read_calendar"

    class Config:
        from_attributes = True


class ConsentResponseSchema(ConsentCreateSchema):
    id:         int
    id_usuario: int
    ativo:      bool
    criado_em:  datetime

    class Config:
        from_attributes = True


# ─── Message ─────────────────────────────────────────────────────────────────

class MessageSchema(BaseModel):
    role: str  # "user" ou "assistant"
    conteudo: str
    enviado_em: datetime = datetime.now()

class ConversaSchema(BaseModel):
    id_usuario: int
    conversa: str

    class Config:
        from_attributes = True
