from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao, verificar_token
from main import CryptContext, SECRET_KEY, ALGORITHM, EXPIRED_TIME_TOKEN
from schemas import Usuarioschema, LoguinSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import os
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])


def criar_token(id_usuario, duracao_tolken=timedelta(minutes=EXPIRED_TIME_TOKEN)):
    expired_time = datetime.now(timezone.utc) + duracao_tolken
    dic_info_token = {"sub": str(id_usuario), "exp": expired_time}
    token = jwt.encode(dic_info_token, SECRET_KEY, algorithm=ALGORITHM)
    return token


def autenticar_usuario(email: str, senha: str, session: Session):
    usuario = session.query(Usuario).filter_by(email=email).first()

    if not usuario:
        return False
    if not CryptContext.verify(senha, usuario.senha):
        return False
    return usuario


@auth_router.get("/")
async def autenticar():
    return {"message": "Rota de autenticação", "autenticado": False}


@auth_router.post("/criar_usuario")
async def criar_usuario(usurio_schemas: Usuarioschema, session: Session = Depends(pegar_sessao)):
    # Verificar se o email já existe
    usuario_existente = session.query(Usuario).filter_by(email=usurio_schemas.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Criar um novo usuário
    senha_criptografada = CryptContext.hash(usurio_schemas.senha)
    # ✅ CORRIGIDO: removido o corte [:72]. Esse corte truncava o HASH já
    # pronto do bcrypt (que tem tamanho fixo, ~60 chars), corrompendo-o e
    # quebrando o login de qualquer usuário criado por essa rota.
    # O limite de 72 bytes do bcrypt é sobre a SENHA de entrada, não sobre
    # o hash de saída — e o passlib já cuida disso internamente.
    novo_usuario = Usuario(
        nome=usurio_schemas.nome,
        email=usurio_schemas.email,
        senha=senha_criptografada,
        nascimento=usurio_schemas.nascimento,
        status=usurio_schemas.status,
        criado_em=usurio_schemas.criado_em,
    )
    session.add(novo_usuario)
    session.commit()

    return {"message": "Usuário criado com sucesso"}


@auth_router.post("/login")
async def login(login_schema: LoguinSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado ou senha incorreta")

    access_token = criar_token(usuario.id)
    refrash_token = criar_token(usuario.id, duracao_tolken=timedelta(days=7))
    return {
        "access_token": access_token,
        "refresh_token": refrash_token,
        "token_type": "bearer"
    }


@auth_router.post("/login-form")
async def login_form(formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(formulario.username, formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado ou senha incorreta")

    access_token = criar_token(usuario.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@auth_router.get("/refresh")
async def refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }