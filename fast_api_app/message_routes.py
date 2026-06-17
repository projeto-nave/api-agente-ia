# message_routes.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from dependencies import verificar_token, pegar_sessao
from schemas import MessageSchema, ConversaSchema
from models import Message, DB, Usuario
from sqlalchemy.orm import Session
from datetime import datetime
from azure_agent import AzureFoundryLLM # Importa a função do agente


message_router = APIRouter(prefix="/messages", tags=["messages"], dependencies=[Depends(verificar_token)])

agente_resp = str


def atualizar_conversa(nova_mensagem: dict, current_user: Usuario, session: Session) -> list:
    """Gera o histórico de mensagens para um usuário específico."""
    registro = session.query(Message).filter_by(id_usuario=current_user.id).first()
    registro.conversa = registro.conversa + [nova_mensagem]
    return registro


async def menssagen_resposta(
    Menssagem_schema: str, 
    session: Session = Depends(pegar_sessao), 
    current_user: Usuario = Depends(verificar_token)
):
    # Esta rota continua funcionando separadamente se precisar
    nova_mensagem = {
        "role": "assistant", 
        "contudo": Menssagem_schema,
        "enviado_em": datetime.now().isoformat()
    } 
    print(f"Mensagem da IA: {nova_mensagem}")

    registro_conversa = session.query(Message).filter_by(id_usuario=current_user.id).first()
    
    if registro_conversa:
        atualizar_conversa(nova_mensagem, current_user, session)
    else:
        novo_registro = Message(
            id_usuario=current_user.id,
            conversa=[nova_mensagem]
        )
        session.add(novo_registro)
    
    session.commit()

    return {
        "message": "Mensagem recebida e armazenada com sucesso!",
        "role": "assistant", 
        "conteudo": nova_mensagem["contudo"]
    }

@message_router.get("/")
async def menssagens():
    return {"message": "Rota de autenticação", "autenticado": False}


@message_router.post("/menssagens")
async def menssagen_envio(
    Menssagem_schema: MessageSchema, 
    session: Session = Depends(pegar_sessao), 
    current_user: Usuario = Depends(verificar_token)
):
    # 1. Salva a mensagem do usuário
    nova_mensagem = {
        "role": "user", 
        "contudo": Menssagem_schema.conteudo,
        "enviado_em": datetime.now().isoformat()
    } 
    print(f"Mensagem do usuário: {nova_mensagem}")

    registro_conversa = session.query(Message).filter_by(id_usuario=current_user.id).first()
    
    if registro_conversa:
        atualizar_conversa(nova_mensagem, current_user, session)
    else:
        novo_registro = Message(
            id_usuario=current_user.id,
            conversa=[nova_mensagem]
        )
        session.add(novo_registro)
    
    session.commit()

    agente_resp = AzureFoundryLLM()._call(prompt=Menssagem_schema.conteudo)

    # 3. Atualiza conversa com resposta da IA
    resposta = await menssagen_resposta(
        Menssagem_schema=agente_resp,
        session=session,
        current_user=current_user
    )
    return resposta
    
    
