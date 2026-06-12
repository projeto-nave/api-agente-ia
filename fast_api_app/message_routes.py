from fastapi import APIRouter, Depends, HTTPException
from dependencias import verificar_token, pegar_sessao
from schemas import MensagemcreateSchema, MensagemSchema
from models import Message, DB
from sqlalchemy.orm import Session

message_router = APIRouter(prefix="/messages", tags=["messages"])

def gerar_historico(id_usuario: int, session: Session = Depends()):
    """ Gera o histórico de mensagens para um usuário específico.
    pegando a conversa atual no banco dedados e adicionando a nova mensagem a ela."""
    historico_atual = Session.query(Message).filter_by(id_usuario=id_usuario).first()
    

def menssagen_envio():
    """ recebera mensagem do usuario e enviara tanto para o banco de dados quanto para o script da ia """


@message_router.get("/")
async def menssagens():
    return {"message": "Rota de autenticação","autenticado": False}

"""treino de rota de menssagem 



 """