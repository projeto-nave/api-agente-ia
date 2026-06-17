from fastapi import APIRouter, Depends, HTTPException
from dependencies import verificar_token, pegar_sessao,verificar_token_opcional
from schemas import MessageSchema,ConversaSchema
from models import Message, DB, Usuario
from sqlalchemy.orm import Session
from datetime import datetime
import requests

chat_router = APIRouter(prefix="/chat", tags=["chat"], dependencies=[Depends(verificar_token_opcional)])

@chat_router.get("/")
async def chat():
    return {"menssagem": "rota de chat","autenticacao": False}

@chat_router.post("/chat")
async def mostrar_chat(usuario_ou_visitante:str = Depends(verificar_token_opcional)):
     
    if isinstance(usuario_ou_visitante, Usuario):
        # Comportamento autenticado
        return {"msg": f"Olá {usuario_ou_visitante.nome}"}
    else:
        # é a string "visitante"
        return {"msg": "Olá visitante"}