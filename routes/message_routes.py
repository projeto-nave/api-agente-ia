# message_routes.py
from fastapi import APIRouter, Depends, HTTPException
from dependencies import verificar_token_opcional, pegar_sessao, get_session_id
from schemas import MessageSchema
from models import Message, Usuario
from sqlalchemy.orm import Session
from datetime import datetime
from azure_agent import criar_conversa,AzureFoundryLLM
from typing import Optional
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
import os
import requests

message_router = APIRouter(
    prefix="/messages",
    tags=["messages"],
    dependencies=[Depends(verificar_token_opcional)]
)




@message_router.get("/")
async def mensagens():
    return {"message": "Rota de mensagens", "autenticado": False}


@message_router.post("/menssagens")
async def mensagen_envio(
    mensagem: MessageSchema,
    session: Session = Depends(pegar_sessao),
    current_user: Optional[Usuario] = Depends(verificar_token_opcional),
    anon_session_id: str = Depends(get_session_id)
):
    # Determina filtro de busca
    if current_user:
        filtro = {"id_usuario": current_user.id}
    else:
        filtro = {"id_session": anon_session_id}
        

    # Busca conversa existente ou cria nova
    conversa_reg = session.query(Message).filter_by(**filtro).first()
    if current_user:
        apresentacao = f"Olá, {current_user.nome}! Sou Nicole, sua assistente virtual de inteligência artificial. Estou aqui para ajudar você a decolar nos recursos das Naves. Como posso ajudar você hoje?"
    else:
        apresentacao = "Olá! Sou Nicole, sua assistente virtual de inteligência artificial. Estou aqui para ajudar você a encontrar informações sobre os recursos das Naves e esclarecer dúvidas sobre os serviços disponíveis. Como posso ajudar você hoje?"

    if not conversa_reg:
        conversa_reg = Message(
            id_usuario=current_user.id if current_user else None,
            id_session=None if current_user else anon_session_id,
            id_conversa=criar_conversa(current_user if current_user else None),
            conversa=[{"role": "assistant",
            "conteudo": apresentacao,
            "criado_em": datetime.now().isoformat()}],
            criado_em=datetime.now()
        )
        session.add(conversa_reg)
        session.flush()  # garante que o objeto existe antes de modificar

    # Monta os dois turnos do par user/assistant
    novo_par = [
        {
            "role": "user",
            "conteudo": mensagem.conteudo,
            "criado_em": datetime.now().isoformat()
        }
    ]

    # Chama o agente de IA
    print(str(current_user))
    if conversa_reg.id_conversa == None:
        conversa_reg.id_conversa = criar_conversa(current_user if current_user else None) 

    llm = AzureFoundryLLM(conversation_id= str(conversa_reg.id_conversa))
    resposta = llm._call(prompt=mensagem.conteudo)

    novo_par.append({
        "role": "assistant",
        "conteudo": resposta,
        "criado_em": datetime.now().isoformat()
    })

    # ✅ CORRIGIDO: garante que conversa_reg.conversa é lista antes de concatenar
    historico_atual = conversa_reg.conversa if isinstance(conversa_reg.conversa, list) else []
    conversa_reg.conversa = historico_atual + [novo_par]

    session.commit()

    return {"resposta": resposta}


@message_router.get("/historico")
async def obter_historico_simples(
    session: Session = Depends(pegar_sessao),
    current_user: Optional[Usuario] = Depends(verificar_token_opcional),
    anon_session_id: str = Depends(get_session_id)
):
    if current_user:
        conversa = session.query(Message).filter_by(id_usuario=current_user.id).first()
        usuario_nome = current_user.nome
    else:
        conversa = session.query(Message).filter_by(
            id_session=anon_session_id,
            id_usuario=None
        ).first()
        usuario_nome = None

    if not conversa or not conversa.conversa:
        return {
            "mensagens": [],
            "total": 0,
            "autenticado": bool(current_user),
            "usuario": usuario_nome
        }

    # ✅ Achata a lista de pares [[user,assistant], ...] em lista plana [user, assistant, ...]
    # para o frontend não precisar lidar com aninhamento duplo
    mensagens_planas = []
    for par in conversa.conversa:
        if isinstance(par, list):
            mensagens_planas.extend(par)
        else:
            mensagens_planas.append(par)

    return {
        "mensagens": mensagens_planas,
        "total": len(mensagens_planas),
        "autenticado": bool(current_user),
        "usuario": usuario_nome,
        "ultima_atualizacao": conversa.criado_em.isoformat() if conversa.criado_em else None
    }


@message_router.get("/test-cookie")
async def test_cookie(anon_session_id: str = Depends(get_session_id)):
    return {
        "session_id": anon_session_id,
        "cookie_criado": True,
        "mensagem": "Cookie está funcionando!"
    }

load_dotenv()

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_REGION = os.getenv("AZURE_REGION")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")

@message_router.get("/speech-token")
def get_speech_token():
    url = f"{AZURE_ENDPOINT}/sts/v1.0/issueToken"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_SPEECH_KEY,
        "Content-type": "application/x-www-form-urlencoded",
        "Content-Length": "0"
    }
    r = requests.post(url, headers=headers)
    return {"token": r.text, "region": "eastus"}