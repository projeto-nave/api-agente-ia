
from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime, date


class Usuarioschema(BaseModel):
    nome: str
    email: str
    senha: str
    nascimento: Optional [date]
    ativo: Optional[bool] = True
    admin: Optional[bool] = False

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



# ─── Message ─────────────────────────────────────────────────────────────────

class MessageSchema(BaseModel):
    conteudo: str #conteudo da mensagem enviada pelo usuario ou pela ia
    enviado_em: datetime=datetime.now()  # Data e hora de envio da mensagem
    class Config:
        from_attributes = True

class ConversaSchema(BaseModel):
    id_usuario: int
    conversa: str  # Armazenar a conversa como uma string JSON ou outro formato adequado

    class Config:
        from_attributes = True
